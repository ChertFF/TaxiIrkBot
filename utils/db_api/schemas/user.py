from sqlalchemy import BigInteger, Column, String, sql, Integer

from utils.db_api.db_gino import TimedBaseModel


class Users(TimedBaseModel):
    __tablename__ = 'users'
    chat_id = Column(BigInteger, primary_key=True)
    name = Column(String(70))
    address = Column(String(100))
    city = Column(String(100))
    number = Column(String(15))
    time = Column(String(5))
    ordered = Column(Integer)
    ban = Column(Integer)
    second_address = Column(String(100))
    second_city = Column(String(100))
    second_time = Column(String(5))
    second_ordered = Column(Integer)
    reminder = Column(Integer)

    query: sql.select