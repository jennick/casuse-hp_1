from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.base import Base  # noqa: F401
from app.db.session import engine, SessionLocal
from app.models.seller import Seller


def ensure_internal_number_column() -> None:
    """
    Zorg dat de kolom 'internal_number' bestaat op de tabel 'sellers'.

    - Als de tabel nog niet bestaat, wordt die eerst aangemaakt via Base.metadata.create_all().
    - Als de kolom al bestaat, doet 'IF NOT EXISTS' niets.
    """
    db = SessionLocal()
    try:
        db.execute(
            text(
                """
                ALTER TABLE IF EXISTS sellers
                ADD COLUMN IF NOT EXISTS internal_number VARCHAR(50);
                """
            )
        )
        db.commit()
    except Exception as exc:
        # In dev willen we niet crashen op dit script, enkel een waarschuwing tonen.
        print("[init_db] Warning: kon internal_number niet garanderen:", exc)
        db.rollback()
    finally:
        db.close()


def seed_sellers(db: Session) -> None:
    # als er al verkopers zijn, doe niets
    if db.query(Seller).count() > 0:
        return

    demo = [
        Seller(
            seller_code="S-0001",
            first_name="Jennick",
            last_name="Demo",
            email_work="jennick.demo@example.com",
            phone_mobile="+32 470 000 001",
            phone_internal="2001",
            address_line1="Demo straat 1",
            address_line2=None,
            postal_code="9000",
            city="Gent",
            country="BE",
            region_code="BE-VOV",
            employment_type="employee",
            max_discount_percent=15,
            default_margin_target_percent=30,
            is_active=True,
            role="manager",
        ),
        Seller(
            seller_code="S-0002",
            first_name="Ana",
            last_name="Martínez",
            email_work="ana.martinez@example.com",
            phone_mobile="+52 55 0000 0002",
            phone_internal="2102",
            address_line1="Calle Ejemplo 123",
            address_line2=None,
            postal_code="01000",
            city="Ciudad de México",
            country="MX",
            region_code="MX-CMX",
            employment_type="employee",
            max_discount_percent=10,
            default_margin_target_percent=25,
            is_active=True,
            role="seller",
        ),
    ]

    db.add_all(demo)
    db.commit()


def main() -> None:
    # 1. registreer modellen en maak tabellen aan als ze nog niet bestaan
    from app.db import base  # noqa: F401

    Base.metadata.create_all(bind=engine)  # type: ignore[name-defined]

    # 2. zorg dat de kolom 'internal_number' zeker aanwezig is
    ensure_internal_number_column()

    # 3. seed demo-data als er nog geen verkopers zijn
    db = SessionLocal()
    try:
        seed_sellers(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
