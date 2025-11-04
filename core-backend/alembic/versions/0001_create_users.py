from alembic import op
import sqlalchemy as sa

# NIEUW: we gebruiken hier geen bcrypt maar pbkdf2_sha256
from passlib.hash import pbkdf2_sha256

revision = "0001_create_users"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("full_name", sa.String(255)),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(50), nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.sql.expression.true()),
        sa.Column("twofa_enabled", sa.Boolean, nullable=False, server_default=sa.sql.expression.false()),
        sa.Column("twofa_secret", sa.String(32), nullable=True),
    )

    conn = op.get_bind()

    # 5 users, allemaal zelfde wachtwoord
    password_plain = "Casuse!2025"
    password_hash = pbkdf2_sha256.hash(password_plain)

    seed_users = [
        ("admin@casuse-hp.local", "admin", "admin"),
        ("manager@casuse-hp.local", "manager", "manager"),
        ("sales@casuse-hp.local", "sales", "seller"),
        ("website@casuse-hp.local", "website", "website"),
        ("logistics@casuse-hp.local", "logistics", "warehouse"),
    ]

    for email, name, role in seed_users:
        conn.execute(
            sa.text(
                """
                INSERT INTO users (email, full_name, hashed_password, role, is_active, twofa_enabled)
                VALUES (:email, :full_name, :hashed_password, :role, true, false)
                """
            ),
            {
                "email": email,
                "full_name": name,
                "hashed_password": password_hash,
                "role": role,
            },
        )


def downgrade():
    op.drop_table("users")
