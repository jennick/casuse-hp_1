from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Customer


# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

# Tijd waarna een onvoltooide registratie mag verwijderd worden
REGISTRATION_TTL = timedelta(hours=1)


# ─────────────────────────────────────────────
# Cleanup logic
# ─────────────────────────────────────────────

def cleanup_unfinished_customers() -> int:
    """
    Verwijdert klanten die:
    - geen wachtwoord hebben ingesteld
    - ouder zijn dan REGISTRATION_TTL

    Returns:
        int: aantal verwijderde klanten
    """
    db: Session = SessionLocal()
    deleted_count = 0

    try:
        cutoff = datetime.now(timezone.utc) - REGISTRATION_TTL

        stale_customers = (
            db.query(Customer)
            .filter(Customer.hashed_password.is_(None))
            .filter(Customer.created_at < cutoff)
            .all()
        )

        for customer in stale_customers:
            db.delete(customer)
            deleted_count += 1

        if deleted_count > 0:
            db.commit()

        return deleted_count

    finally:
        db.close()


# ─────────────────────────────────────────────
# Standalone execution (optioneel, maar handig)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    removed = cleanup_unfinished_customers()
    print(f"[cleanup] removed {removed} unfinished customers")
