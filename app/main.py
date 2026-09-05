from fastapi import FastAPI
from sqlalchemy import text
from app import models 
from app.database import Base,engine

# 根据models.py中的表结构，在数据库中创建不存在的表。
Base.metadata.create_all(bind=engine)
# 创建一个FastAPI后端程序
app = FastAPI(
    title="Enterprise RAG Assiatant",
    description="企业文档智能知识库与问答平台",
    version="0.1.0"
)
@app.get("/health")
def health():
    return{
        "status":"OK"
    }
@app.get("/db-health")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database": "connected"
        }

    except Exception as e:
        return {
            "database": "error",
            "detail": str(e)
        }