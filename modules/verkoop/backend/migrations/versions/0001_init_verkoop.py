from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '0001_init_verkoop'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # regions & cities
    op.create_table('regions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
    )
    op.create_table('cities',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('region_id', sa.Integer, sa.ForeignKey('regions.id', ondelete='CASCADE'), nullable=False),
    )
    op.create_index('ix_cities_region', 'cities', ['region_id'])

    # sellers
    op.create_table('sellers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('code', sa.String(32), unique=True, nullable=False),
        sa.Column('name', sa.String(120), nullable=False),
        sa.Column('email', sa.String(200), nullable=False),
        sa.Column('avatar_url', sa.String(500)),
        sa.Column('max_discount_percent', sa.Numeric(5,2), nullable=False, server_default='10.00'),
        sa.Column('active', sa.Boolean, nullable=False, server_default=sa.text('true'))
    )

    # number series
    op.create_table('number_series',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('pattern', sa.String(50), nullable=False),
        sa.Column('current_no', sa.Integer, nullable=False, server_default='0'),
        sa.Column('year', sa.Integer, nullable=False)
    )

    # product catalog + price rules
    op.create_table('product_catalog',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('sku', sa.String(64), unique=True, nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('base_price', sa.Numeric(12,2), nullable=False),
        sa.Column('vat_rate', sa.Numeric(5,2), nullable=False, server_default='16.00')
    )
    op.create_table('price_rules',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('product_catalog.id', ondelete='CASCADE'), nullable=False),
        sa.Column('min_qty', sa.Integer, nullable=False, server_default='1'),
        sa.Column('discount_percent', sa.Numeric(5,2), nullable=False, server_default='0.00')
    )
    op.create_index('ix_price_rules_pid', 'price_rules', ['product_id'])

    # customer shadow (import from website-db)
    op.create_table('customer_shadow',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('website_customer_id', sa.Integer, nullable=False, unique=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('email', sa.String(200)),
        sa.Column('city_id', sa.Integer, sa.ForeignKey('cities.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('ix_customer_shadow_city', 'customer_shadow', ['city_id'])

    # assignments
    op.create_table('customer_assignments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customer_id', sa.Integer, sa.ForeignKey('customer_shadow.id', ondelete='CASCADE'), nullable=False),
        sa.Column('seller_id', sa.Integer, sa.ForeignKey('sellers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='active'),
        sa.Column('auto_assigned', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.UniqueConstraint('customer_id', name='uq_assignment_customer')
    )
    op.create_index('ix_assignments_seller', 'customer_assignments', ['seller_id'])
    op.create_index('ix_assignments_status', 'customer_assignments', ['status'])

    # quotes
    op.create_table('quotes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('quote_no', sa.String(30), unique=True),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        sa.Column('customer_id', sa.Integer, sa.ForeignKey('customer_shadow.id', ondelete='SET NULL'), nullable=True),
        sa.Column('seller_id', sa.Integer, sa.ForeignKey('sellers.id', ondelete='SET NULL'), nullable=True),
        sa.Column('currency', sa.String(10), nullable=False, server_default='MXN'),
        sa.Column('subtotal', sa.Numeric(14,2), nullable=False, server_default='0.00'),
        sa.Column('vat', sa.Numeric(14,2), nullable=False, server_default='0.00'),
        sa.Column('total', sa.Numeric(14,2), nullable=False, server_default='0.00'),
        sa.Column('status', sa.String(20), nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('ix_quotes_customer', 'quotes', ['customer_id'])
    op.create_index('ix_quotes_seller', 'quotes', ['seller_id'])
    op.create_index('ix_quotes_status', 'quotes', ['status'])

    op.create_table('quote_lines',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('quote_id', sa.Integer, sa.ForeignKey('quotes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('product_catalog.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('qty', sa.Integer, nullable=False),
        sa.Column('unit_price', sa.Numeric(12,2), nullable=False),
        sa.Column('discount_percent', sa.Numeric(5,2), nullable=False, server_default='0.00'),
        sa.Column('line_total', sa.Numeric(14,2), nullable=False)
    )
    op.create_index('ix_quote_lines_quote', 'quote_lines', ['quote_id'])

    # feasibility
    op.create_table('feasibility_checks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('quote_id', sa.Integer, sa.ForeignKey('quotes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('notes', sa.Text),
        sa.Column('attachments', sa.JSON, nullable=False, server_default='[]'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    # orders
    op.create_table('sales_orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_no', sa.String(30), unique=True),
        sa.Column('customer_id', sa.Integer, sa.ForeignKey('customer_shadow.id', ondelete='SET NULL'), nullable=True),
        sa.Column('seller_id', sa.Integer, sa.ForeignKey('sellers.id', ondelete='SET NULL'), nullable=True),
        sa.Column('seller_book_no', sa.String(30)),
        sa.Column('currency', sa.String(10), nullable=False, server_default='MXN'),
        sa.Column('subtotal', sa.Numeric(14,2), nullable=False, server_default='0.00'),
        sa.Column('vat', sa.Numeric(14,2), nullable=False, server_default='0.00'),
        sa.Column('total', sa.Numeric(14,2), nullable=False, server_default='0.00'),
        sa.Column('status', sa.String(20), nullable=False, server_default='created'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('ix_sales_orders_status', 'sales_orders', ['status'])

    op.create_table('sales_order_lines',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('sales_orders.id', ondelete='CASCADE'), nullable=False),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('product_catalog.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('qty', sa.Integer, nullable=False),
        sa.Column('unit_price', sa.Numeric(12,2), nullable=False),
        sa.Column('discount_percent', sa.Numeric(5,2), nullable=False, server_default='0.00'),
        sa.Column('line_total', sa.Numeric(14,2), nullable=False)
    )
    op.create_index('ix_sales_order_lines_order', 'sales_order_lines', ['order_id'])

    # payments
    op.create_table('payment_intents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('sales_orders.id', ondelete='CASCADE'), nullable=False),
        sa.Column('provider', sa.String(50), nullable=False),
        sa.Column('intent_id', sa.String(100), nullable=False, unique=True),
        sa.Column('amount', sa.Numeric(14,2), nullable=False),
        sa.Column('currency', sa.String(10), nullable=False, server_default='MXN'),
        sa.Column('status', sa.String(20), nullable=False, server_default='requires_payment_method'),
        sa.Column('metadata', sa.JSON, nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('ix_payment_intents_order', 'payment_intents', ['order_id'])

    # audit
    op.create_table('audit_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('when', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('actor', sa.String(100)),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('entity', sa.String(50)),
        sa.Column('entity_id', sa.Integer),
        sa.Column('details', sa.JSON, nullable=False, server_default='{}')
    )

def downgrade():
    op.drop_table('audit_log')
    op.drop_index('ix_payment_intents_order', table_name='payment_intents')
    op.drop_table('payment_intents')
    op.drop_index('ix_sales_order_lines_order', table_name='sales_order_lines')
    op.drop_table('sales_order_lines')
    op.drop_index('ix_sales_orders_status', table_name='sales_orders')
    op.drop_table('sales_orders')
    op.drop_table('feasibility_checks')
    op.drop_index('ix_quote_lines_quote', table_name='quote_lines')
    op.drop_table('quote_lines')
    op.drop_index('ix_quotes_status', table_name='quotes')
    op.drop_index('ix_quotes_seller', table_name='quotes')
    op.drop_index('ix_quotes_customer', table_name='quotes')
    op.drop_table('quotes')
    op.drop_index('ix_assignments_status', table_name='customer_assignments')
    op.drop_index('ix_assignments_seller', table_name='customer_assignments')
    op.drop_table('customer_assignments')
    op.drop_index('ix_customer_shadow_city', table_name='customer_shadow')
    op.drop_table('customer_shadow')
    op.drop_index('ix_price_rules_pid', table_name='price_rules')
    op.drop_table('price_rules')
    op.drop_table('product_catalog')
    op.drop_table('number_series')
    op.drop_table('sellers')
    op.drop_index('ix_cities_region', table_name='cities')
    op.drop_table('cities')
    op.drop_table('regions')
