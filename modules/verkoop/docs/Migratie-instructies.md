
# Migraties & Seeds (NL)
- Alembic draait automatisch bij containerstart (`alembic upgrade head`)
- Seeds: 2 regio’s, 4 steden, 5 verkopers, catalogus en rules, nummerreeksen
- Optionele klant-sync: stel `WEBSITE_DB_URL` in en draai `/scripts/sync_customers.py` (nog te automatiseren per cron/k8s job)
