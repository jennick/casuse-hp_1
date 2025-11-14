
from sqlalchemy.orm import Session
from app.models.number_series import NumberSeries
from datetime import datetime

def _format(pattern: str, number: int, year: int) -> str:
    out = pattern.replace("{YYYY}", str(year))
    hashes = out.count("#")
    if hashes:
        out = out.replace("{" + "#"*hashes + "}", str(number).zfill(hashes))
    # support mixed #### / ######
    out = out.replace("{####}", str(number).zfill(4))
    out = out.replace("{######}", str(number).zfill(6))
    return out

def reserve_number(db: Session, series_name: str) -> str:
    year = datetime.utcnow().year
    series = db.query(NumberSeries).filter(NumberSeries.name == series_name, NumberSeries.year == year).first()
    if not series:
        raise ValueError("Series not configured for current year")
    series.current_no += 1
    db.add(series)
    db.flush()
    return _format(series.pattern, series.current_no, series.year)
