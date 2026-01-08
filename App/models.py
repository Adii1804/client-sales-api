from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Date, Numeric, Integer

class Base(DeclarativeBase):
    pass


class LastYearSales(Base):
    __tablename__ = "vw_LastYearSales"
    __table_args__ = {"extend_existing": True}

    RECEIPTID = Column(String)
    CUSTMOBILENO = Column(String)
    TRANSDATE = Column(Date)
    STORE = Column(String)
    PAYMENTAMOUNT = Column(Numeric)

    Itemid = Column(String)
    price = Column(Numeric)
    quantity = Column(Integer)
    discount = Column(Numeric)
