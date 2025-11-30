from sqlalchemy import text

from app.db.session import engine


def run_migration() -> None:
    """
    Voegt kolommen toe aan de tabel 'sellers' voor wachtwoordbeheer.

    - password_hash: versleuteld wachtwoord van de verkoper
    - reset_token: een tijdelijke token voor wachtwoord-reset
    - reset_token_expires_at: tot wanneer de token geldig is

    De migratie is idempotent: als de kolom al bestaat, gebeurt er niets.
    Bestaande data in 'sellers' blijft volledig behouden.
    """
    statements = [
        """
        ALTER TABLE IF EXISTS sellers
        ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);
        """,
        """
        ALTER TABLE IF EXISTS sellers
        ADD COLUMN IF NOT EXISTS reset_token VARCHAR(255);
        """,
        """
        ALTER TABLE IF EXISTS sellers
        ADD COLUMN IF NOT EXISTS reset_token_expires_at TIMESTAMPTZ;
        """,
    ]

    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))


def main() -> None:
    print("[migration] Start: add seller auth fields")
    run_migration()
    print("[migration] Klaar: kolommen password_hash, reset_token, reset_token_expires_at zijn aanwezig (of bestonden al).")


if __name__ == "__main__":
    main()
