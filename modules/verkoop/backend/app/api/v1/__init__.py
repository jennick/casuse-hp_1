"""
API v1 package voor de verkoop-module.

Let op:
- We doen hier GEEN side-effect imports (zoals `from . import feasibility`)
- Routers worden rechtstreeks in `app.main` geïmporteerd, om circular imports te vermijden.
"""

# bewust leeg: alleen een "normaal" Python package
