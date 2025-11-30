# app/core/seller_auth.py
"""
Hulpfuncties voor het hashen en verifiëren van verkoperswachtwoorden.

Dit staat los van de globale core-auth van Casuse-HP en is enkel
voor de verkoopmodule / verkopersaccounts bedoeld.
"""

from __future__ import annotations

import bcrypt


def hash_seller_password(plain_password: str) -> str:
    """
    Maak een veilig bcrypt-hash van een wachtwoord.

    - plain_password mag niet leeg zijn
    - het resultaat is een UTF-8 string die in de database kan opgeslagen worden
    """
    if not plain_password or not plain_password.strip():
        raise ValueError("Password must not be empty")

    # 12 rounds is een goede balans tussen veiligheid en performance
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_seller_password(plain_password: str, password_hash: str | None) -> bool:
    """
    Controleer of een plain wachtwoord overeenkomt met een bestaande hash.

    - Geeft False terug als er geen hash is
    - Geeft False terug bij eender welke fout (corrupt formaat, enz.)
    """
    if not password_hash:
        return False

    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except Exception:
        # Bij een ongeldige hash/format: niet crashen, gewoon False
        return False
