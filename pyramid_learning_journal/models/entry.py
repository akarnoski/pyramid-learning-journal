from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode
)

from .meta import Base


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    date = Column(Unicode)
    body = Column(Unicode)

    def to_dict(self):
        """Take all model attributes."""
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date,
            'body': self.body
        }
