"""
Seed admin user voor de verkoopmodule.

Uitvoeren met:

    docker compose -f docker-compose.verkoop.yml run --rm verkoop-backend ^
        python -m app.scripts.ensure_admin_user
"""

from sqlalchemy.orm import Session
from sqlalchemy import inspect

from app.db.session import Base, get_engine, get_session
from app.models.admin_user import AdminUser
from app.core.admin_auth import hash_password


def main():
    # 1. Engine initialiseren (maakt SessionLocal aan)
    engine = get_engine()

    # 2. Controleren of admin_users tabel al bestaat
    inspector = inspect(engine)
    if "admin_users" not in inspector.get_table_names():
        Base.metadata.create_all(
            bind=engine,
            tables=[AdminUser.__table__]
        )

    # 3. DB-session openen volgens jouw projectlogica
    db: Session = get_session()

    try:
        # 4. Bestaat de admin al?
        existing = (
            db.query(AdminUser)
            .filter(AdminUser.email == "admin@verkoop.local")
            .first()
        )

        if existing:
            print("admin@verkoop.local bestaat al, niets te doen.")
            return

        # 5. Aanmaken admin user
        admin = AdminUser(
            email="admin@verkoop.local",
            full_name="Sales Admin",
            password_hash=hash_password("Admin!2025"),
            is_active=True,
        )

        db.add(admin)
        db.commit()
        print("Admin gebruiker succesvol aangemaakt:")
        print("E-mail: admin@verkoop.local")
        print("Wachtwoord: Admin!2025")

    finally:
        db.close()


if __name__ == "__main__":
    main()
