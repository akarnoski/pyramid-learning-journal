"""Create instances of Entry class to insert data into database."""
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode
)

from .meta import Base


class Entry(Base):
    """Create instance of Entry model."""
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    date = Column(Unicode)
    tags = Column(Unicode)
    body = Column(Unicode)

    def to_dict(self):
        """Take all model attributes."""
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date,
            'tags': self.tags,
            'body': self.body,
        }
