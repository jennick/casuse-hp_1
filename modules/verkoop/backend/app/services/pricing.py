
from sqlalchemy.orm import Session
from app.models.catalog import ProductCatalog, PriceRule

def price_quote(db: Session, lines: list[dict]) -> dict:
    subtotal = 0.0
    breakdown = []
    for line in lines:
        prod = db.query(ProductCatalog).get(line['product_id'])
        if not prod:
            raise ValueError("Product not found")
        # find best rule
        rules = db.query(PriceRule).filter(PriceRule.product_id == prod.id).all()
        discount = 0.0
        for r in rules:
            if line['qty'] >= r.min_qty and float(r.discount_percent) > discount:
                discount = float(r.discount_percent)
        unit = float(prod.base_price)
        line_total = (unit * line['qty']) * (1 - discount/100.0) * (1 + float(prod.vat_rate)/100.0)
        subtotal += line_total
        breakdown.append({"sku": prod.sku, "qty": line['qty'], "unit": unit, "discount": discount, "vat": float(prod.vat_rate), "line_total": round(line_total,2)})
    vat_part = subtotal * 0.0  # included in calc above; set 0 for clarity
    total = subtotal
    return {"subtotal": round(subtotal,2), "vat": round(vat_part,2), "total": round(total,2), "lines": breakdown}
