from sqlalchemy import Column, Integer, String, Sequence, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import *


class Bookings(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    condition = Column(String(255))
    duration_of_booking = Column(String(255))
    tool_id = Column(Integer, ForeignKey('tools.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # foreign keys
    returns = relationship("Returns")
    invoices = relationship("Invoices")
    dispatch = relationship("Dispatch")

    def __repr__(self):
        return str(self.__dict__)
