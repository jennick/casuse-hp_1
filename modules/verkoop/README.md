
# Verkoop-module (NL)

Deze map bevat de volledige Verkoop-module (backend + frontend) voor Casuse-HP, plus Docker en documentatie.

## Start
- Maak `.env` vanuit `.env.template`.
- `docker compose -f docker-compose.verkoop.yml up -d --build`

## Back-end
- Addr: `http://localhost:20030`
- API: `http://localhost:20030/api/v1/...`
- Health: `/healthz`, `/readyz`, metrics op `/metrics`

## Front-end (manager)
- Nginx op `http://localhost:20040`
- UI-talen: EN/ES

## Tabellen (verkort)
Seller, CustomerShadow, CustomerAssignment, Region, City, NumberSeries, ProductCatalog, PriceRule, Quote, QuoteLine, FeasibilityCheck, SalesOrder, SalesOrderLine, PaymentIntent, AuditLog.

## Nummerreeksen
- Quotes: `QT-HP-{YYYY}-{####}`
- Orders: `SO-HP-{YYYY}-{######}`

## Seeds
- 2 regio’s: North, South
- 4 cities: GDL, CDMX, MTY, QRO
- 5 sellers met verschillende max_discount_percent
- Dummy catalogus & rules
