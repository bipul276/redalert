from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.user import User
from app.core.config import settings
from jose import jwt, JWTError
from passlib.context import CryptContext
import pyotp
import os
import json
from cryptography.fernet import Fernet as FernetCrypto

router = APIRouter()

# --- CONFIG ---
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
TOTP_ENC_KEY_PATH = ".totp_key"

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def load_enc_key():
    if os.path.exists(TOTP_ENC_KEY_PATH):
        with open(TOTP_ENC_KEY_PATH, "rb") as f:
            return f.read()
    return None

cipher = FernetCrypto(load_enc_key()) if load_enc_key() else None

# --- HELPERS ---
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = session.exec(select(User).where(User.email == email)).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not an admin")
    return current_user

# --- ROUTES ---

from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str
    totp_code: str # 6 digits or recovery code

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
def login(form_data: LoginRequest, session: Session = Depends(get_session)):
    # 1. Rate Limiting Check (Basic DB Logic)
    user = session.exec(select(User).where(User.email == form_data.email)).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if user.locked_until and user.locked_until > datetime.utcnow():
        raise HTTPException(status_code=400, detail="Account locked. Try again later.")

    # 2. Password Check
    if not verify_password(form_data.password, user.hashed_password):
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(minutes=10)
            user.failed_login_attempts = 0
        session.add(user)
        session.commit()
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # 3. 2FA Check
    code_input = form_data.totp_code.replace(" ", "").replace("-", "")
    
    is_valid_totp = False
    
    # Decrypt Secret
    if user.totp_secret_enc and cipher:
        try:
            secret = cipher.decrypt(user.totp_secret_enc.encode()).decode()
            totp = pyotp.TOTP(secret)
            if totp.verify(code_input, valid_window=1):
                is_valid_totp = True
        except Exception:
            pass
    
    # Check Recovery Codes
    if not is_valid_totp and user.recovery_codes:
        try:
            codes = json.loads(user.recovery_codes)
            for i, hashed_code in enumerate(codes):
                if pwd_context.verify(code_input, hashed_code):
                    is_valid_totp = True
                    codes.pop(i)
                    user.recovery_codes = json.dumps(codes)
                    session.add(user)
                    break
        except Exception:
            pass

    if not is_valid_totp:
        user.failed_login_attempts += 1
        session.add(user)
        session.commit()
        raise HTTPException(status_code=400, detail="Invalid 2FA Code")

    # 4. Success -> Reset Limits
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_failed_login = None
    session.add(user)
    session.commit()

    # 5. Issue Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "is_superuser": user.is_superuser},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
