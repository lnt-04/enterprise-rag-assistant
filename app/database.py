import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker


load_dotenv()

# MySQL家的地址。
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    database=os.getenv("DB_NAME"),
    query={
        "charset": "utf8mb4"
    }
)

# Python和MySQL之间建立了一条通信线路。
# SQLAlchemy官方对 Engine 的定义也就是数据库连接入口，并负责管理连接池。
# 创建数据库引擎,也就是创建python通往数据库的大门
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

# 创建一个Session数据库会话，
# ORM 对象与数据库进行交互的主要工作区域，并通过它进行查询、提交、回滚等操作。
SessionLocal = sessionmaker(
    bind=engine
)

# 每来一个需要操作数据库的请求，就给它一个数据库 Session，用完以后关闭。
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Base=所有数据库模型的“共同身份证”，以后只要继承Base类，SQLAlchemy就知道该类是数据库模型
class Base(DeclarativeBase):
    pass