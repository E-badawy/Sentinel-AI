from sqlalchemy.orm import Session

from app.database.models import ProcessedMessage


def is_duplicate(message_id: str, db: Session) -> bool:

    exists = (
        db.query(ProcessedMessage)
        .filter(
            ProcessedMessage.message_id == message_id
        )
        .first()
    )

    if exists:
        return True

    db.add(
        ProcessedMessage(
            message_id=message_id
        )
    )

    db.commit()

    return False