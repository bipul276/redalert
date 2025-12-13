from sqlmodel import Session, select
from app.core.database import engine
from app.models.recall import Recall, RawRecall

def check():
    with Session(engine) as session:
        raw_count = session.exec(select(RawRecall)).all()
        recalls = session.exec(select(Recall)).all()
        print(f"Total RawRecalls: {len(raw_count)}")
        print(f"Total Canonical Recalls: {len(recalls)}")
        for r in recalls:
            print(f"- [{r.id}] {r.title} (URL: {r.url})")

if __name__ == "__main__":
    check()
