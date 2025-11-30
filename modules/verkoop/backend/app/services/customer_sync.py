@router.post("/sync/customers")
def sync_customers(
    db: Session = Depends(get_db),
):
    """
    Haalt alle klanten op uit de website-module en slaat ze lokaal op.
    """
    try:
        # API URL van Website-module
        url = "http://host.docker.internal:20052/api/customers/all"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        customers = response.json()

        for c in customers:
            existing = db.query(Customer).filter_by(external_id=c["id"]).first()
            if not existing:
                db.add(Customer(
                    external_id=c["id"],
                    first_name=c["first_name"],
                    last_name=c["last_name"],
                    email=c["email"],
                    company_name=c.get("company_name"),
                    type=c.get("type"),
                    active=True,
                ))
        db.commit()

        return {"success": True, "count": len(customers)}

    except Exception as e:
        return {"success": False, "error": str(e)}
