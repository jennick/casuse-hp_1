from sqlalchemy.orm import declarative_base, declared_attr


class CustomBase:
    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[misc]
        return cls.__name__.lower()

    def __repr__(self) -> str:
        cols = ", ".join(
            f"{c.name}={getattr(self, c.name)!r}"
            for c in self.__table__.columns  # type: ignore[attr-defined]
        )
        return f"{self.__class__.__name__}({cols})"


Base = declarative_base(cls=CustomBase)
