from sqlalchemy import Column, BigInteger, String, sql

from db_api.db_gino import TimedBaseModel


class Info(TimedBaseModel):
    __tablename__ = 'request'
    id = Column(BigInteger)
    request = Column(String(200))

    query: sql.Select
