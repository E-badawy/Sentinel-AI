import re

from sqlalchemy.orm import Session

from app.database.models import User, Memory


# ---------------------------------------
# Patterns worth remembering
# ---------------------------------------

MEMORY_PATTERNS = [
    r"\bmy name is\b",
    r"\bi am\b",
    r"\bi'm\b",
    r"\bi work\b",
    r"\bi study\b",
    r"\bi live\b",
    r"\bi prefer\b",
    r"\bi like\b",
    r"\bi created\b",
    r"\bi built\b",
    r"\bi developed\b",
    r"\bmy favourite\b",
    r"\bmy favorite\b",
]


def should_save_memory(text: str) -> bool:

    text = text.lower().strip()

    for pattern in MEMORY_PATTERNS:

        if re.search(pattern, text):
            return True

    return False


def save_memory(phone: str, memory: str):

    if not should_save_memory(memory):
        return

    from app.database.database import SessionLocal

    db: Session = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(User.phone == phone)
            .first()
        )

        if user is None:

            user = User(phone=phone)

            db.add(user)

            db.commit()

            db.refresh(user)

        duplicate = (
            db.query(Memory)
            .filter(
                Memory.user_id == user.id,
                Memory.content == memory
            )
            .first()
        )

        if duplicate:

            return

        db.add(

            Memory(
                user_id=user.id,
                content=memory
            )

        )

        db.commit()

    finally:

        db.close()


def get_memories(phone: str):

    from app.database.database import SessionLocal

    db: Session = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(User.phone == phone)
            .first()
        )

        if user is None:

            return ""

        memories = (
            db.query(Memory)
            .filter(Memory.user_id == user.id)
            .all()
        )

        return "\n".join(

            memory.content

            for memory in memories

        )

    finally:

        db.close()