
# Functioneel/Technisch Overzicht (NL)
- Endpoints per domein (sellers, assignments, quotes, feasibility, orders, payments, number_series, ai)
- Rollen/scopes: verkoop:read, verkoop:write, verkoop:admin
- Nummerreeksen atomaire reservering met `number_series` service
- Pricing: basisprijs + staffel (PriceRule) + btw; breakdown beschikbaar in backend service
- Payments: abstractie; intents + webhook; reconciliatie (stub)
- Observability: JSON logs, correlation id, Prometheus metrics
