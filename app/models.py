from database import Base
from sqlalchemy import Column, String, Integer, DateTime, func

class Spimex_Trading_Results(Base):
    __tablename__ = "spimex_trading_results"
    id = Column(Integer, primary_key = True)
    exchange_product_id = Column(String)
    exchange_product_name = Column(String)
    oil_id = Column(String)
    delivery_basis_id = Column(String)
    delivery_basis_name = Column(String)
    delivery_type_id = Column(String)
    volume = Column(String)
    total = Column(String)
    count = Column(String)
    date = Column(String)
    created_on = Column(DateTime, server_default = func.now())
    updated_on = Column(DateTime, server_default=func.now(), onupdate=func.now())