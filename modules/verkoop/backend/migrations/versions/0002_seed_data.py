from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '0002_seed_data'
down_revision = '0001_init_verkoop'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    # regions
    conn.execute(sa.text("INSERT INTO regions (name) VALUES ('North'), ('South') ON CONFLICT DO NOTHING"))
    # cities
    conn.execute(sa.text("INSERT INTO cities (name, region_id) VALUES ('Guadalajara', 1), ('CDMX', 1), ('Monterrey', 2), ('Querétaro', 2)"))
    # sellers (5)
    sellers = [
        ('SEL001','Ana López','ana.lopez@example.com','', 10.00, True),
        ('SEL002','Bruno Díaz','bruno.diaz@example.com','', 12.50, True),
        ('SEL003','Carla Ruiz','carla.ruiz@example.com','', 8.00, True),
        ('SEL004','Diego Reyes','diego.reyes@example.com','', 15.00, True),
        ('SEL005','Elena Márquez','elena.marquez@example.com','', 5.00, True),
    ]
    for s in sellers:
        conn.execute(sa.text("INSERT INTO sellers (code,name,email,avatar_url,max_discount_percent,active) VALUES (:c,:n,:e,:a,:m,:ac) ON CONFLICT DO NOTHING"),
                     {"c":s[0],"n":s[1],"e":s[2],"a":s[3],"m":s[4],"ac":s[5]})
    # number series
    year = datetime.utcnow().year
    conn.execute(sa.text("INSERT INTO number_series (name, pattern, current_no, year) VALUES ('QUOTE','QT-HP-{YYYY}-{####}',0,:y) ON CONFLICT DO NOTHING"), {"y":year})
    conn.execute(sa.text("INSERT INTO number_series (name, pattern, current_no, year) VALUES ('ORDER','SO-HP-{YYYY}-{######}',0,:y) ON CONFLICT DO NOTHING"), {"y":year})
    # products
    conn.execute(sa.text("INSERT INTO product_catalog (sku,name,base_price,vat_rate) VALUES "
                         "('SKU-001','Widget A', 100.00, 16.00),"
                         "('SKU-002','Widget B', 250.00, 16.00),"
                         "('SKU-003','Service C', 500.00, 16.00)"
                         ))
    # price rules
    conn.execute(sa.text("INSERT INTO price_rules (product_id,min_qty,discount_percent) VALUES (1,10,5.00),(2,5,3.00),(3,3,2.50)"))

def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM price_rules"))
    conn.execute(sa.text("DELETE FROM product_catalog"))
    conn.execute(sa.text("DELETE FROM number_series"))
    conn.execute(sa.text("DELETE FROM sellers"))
    conn.execute(sa.text("DELETE FROM cities"))
    conn.execute(sa.text("DELETE FROM regions"))
