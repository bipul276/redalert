import sys
import os
import json
import secrets
import qrcode
import pyotp
import io
# from email_validator import validate_email, EmailNotValidError 
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from datetime import datetime

# Setup Paths
if os.path.exists('backend'):
    os.chdir('backend')
    sys.path.append(os.getcwd())
else:
    sys.path.append(os.getcwd())

from sqlmodel import Session, select
from app.core.database import engine
from app.models.user import User

# Security Contexts
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Key for encrypting TOTP secrets in DB
# In prod, this should be env var. For this script, we'll generate one if missing or use a placeholder.
# WARNING: If you lose this key, you lose access to all TOTP secrets.
ENCRYPTION_KEY_PATH = ".totp_key"

def load_or_create_key():
    if os.path.exists(ENCRYPTION_KEY_PATH):
        with open(ENCRYPTION_KEY_PATH, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_PATH, "wb") as f:
            f.write(key)
        print(f"🔑 Generated new TOTP Encryption Key at {ENCRYPTION_KEY_PATH}")
        print("KEEP THIS FILE SAFE. If lost, 2FA breaks.")
        return key

cipher_suite = Fernet(load_or_create_key())

def get_hash(secret: str) -> str:
    return pwd_context.hash(secret)

def create_admin():
    print("🛡️  RedAlert Admin Setup")
    print("=========================")
    
    # 1. Full Name
    full_name = input("Enter Admin Name [RedAlert Admin]: ").strip() or "RedAlert Admin"

    # 2. Email input
    while True:
        email = input("Enter Admin Email: ").strip()
        if "@" in email and "." in email:
            break
        print("Invalid email format.")

    # 3. Password input
    while True:
        password = input("Enter Admin Password: ").strip()
        if len(password) >= 8:
            break
        print("Password must be at least 8 chars.")
    
    # 3. TOTP Generation
    totp_secret_plain = pyotp.random_base32()
    totp_secret_enc = cipher_suite.encrypt(totp_secret_plain.encode()).decode()
    
    totp_uri = pyotp.totp.TOTP(totp_secret_plain).provisioning_uri(name=email, issuer_name="RedAlert")
    
    # 4. Recovery Codes (8 codes, 10 chars hex)
    recovery_plain = [secrets.token_hex(5) for _ in range(8)]
    recovery_hashed = [get_hash(code) for code in recovery_plain]

    # 5. DB Operation
    with Session(engine) as session:
        # Check existing
        existing = session.exec(select(User).where(User.email == email)).first()
        if existing:
            print(f"⚠️  User {email} already exists. Updating credentials...")
            user = existing
        else:
            user = User(email=email, hashed_password="")

        user.full_name = full_name
        user.hashed_password = get_hash(password)
        user.is_superuser = True
        user.totp_secret_enc = totp_secret_enc
        user.recovery_codes = json.dumps(recovery_hashed)
        user.failed_login_attempts = 0
        user.locked_until = None
        
        session.add(user)
        session.commit()
    
    # 6. Output
    print("\n✅ Admin User Created Successfully!")
    print("\n---------------------------------------------------")
    print("📲  Scan this QR Code in Google Authenticator / Authy:")
    
    # Generate QR to terminal
    qr = qrcode.QRCode()
    qr.add_data(totp_uri)
    qr.make(fit=True)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())
    
    print("\nIf QR fails, use this Key:", totp_secret_plain)
    print("Or URI:", totp_uri)
    
    print("\n---------------------------------------------------")
    print("🆘  SAVE THESE RECOVERY CODES (One-time use):")
    for i, code in enumerate(recovery_plain):
        print(f"  {i+1}. {code}")
    print("---------------------------------------------------")

if __name__ == "__main__":
    create_admin()
