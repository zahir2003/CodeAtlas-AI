from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


# Import models so Alembic can discover them
import app.models.repository  # noqa: E402,F401
import app.models.chat_session  # noqa: E402,F401
import app.models.chat_message  # noqa: E402,F401