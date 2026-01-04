
import uuid
from sqlalchemy.orm import Session
from .models import AuditEvent

def log_event(db: Session, *, customer_id: str, actor: str, action: str, description: str | None = None):
    event = AuditEvent(
        id=str(uuid.uuid4()),
        customer_id=customer_id,
        actor=actor,
        action=action,
        description=description,
    )
    db.add(event)
    db.commit()
    return event
