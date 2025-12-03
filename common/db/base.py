from sqlalchemy.ext.declarative import declarative_base
from .mixins import IDMixin, TimestampMixin

# All models will inherit from this Base
Base = declarative_base()

# All models will inherit from this base class to automatically include ID and timestamps
class CommonBase(Base, IDMixin, TimestampMixin):
    __abstract__ = True
    