from fastapi import FastAPI, HTTPException, Path, Query, Depends
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

from sqlalchemy import text
from app import models 
from app.routers import documents, users
from app.database import Base,engine

# 根据models.py中的表结构，在数据库中创建不存在的表。
# SQLAlchemy，把所有继承Base的模型找出来，根据它们创建数据库表。
Base.metadata.create_all(bind=engine)

# 创建一个FastAPI实例
app = FastAPI(
    title="Enterprise RAG Assiatant",
    description="企业文档智能知识库与问答平台",
    version="0.1.0"
)
# 把 users.py 里面定义的接口注册进整个FastAPI程序。
app.include_router(users.router)
app.include_router(documents.router)

# 路径参数
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
    





# 学习练习
# # 自定义响应的数据格式
# # 需求：响应的数据格式为id\title\content
# class News(BaseModel):
#     id: int
#     title:str
#     content:str

# @app.get("/news/{id}",response_model=News) # response_model就指定了要求的响应数据格式
# async def get_news(id:int):
#     return {
#         "id":id,
#         "title": f"这是第{id}本书",
#         "content": "这是一本好书"
        
#     }


# @app.get("/book/{id}")
# # int是参数类型注解，用户访问时会给路径参数{id}传值，比如127.0.0.1:8000/book/666
# async def get_book(id: int = Path(..., gt=0, lt=101, description="书籍id，取值范围是1-6")):
#     id_list=[1,2,3,4,5,6]
#     if id not in id_list:
#         raise HTTPException(status_code=404,detail="您查找的id不存在") # 异常响应处理

#     return{"id": id, "title": f"这是第{id}本书"}

# @app.get("/author/{name}")
# async def get_name(name: str = Path(...,min_length=2, max_length=10)):
#     return{"name": name,"msg": f"这是{name}的书,非常推荐"}


# # 查询参数
# # 需求：：查询新闻，分页；skip:跳过的记录数，limit：返回的记录数 10
# @app.get("/news/news_list")
# async def get_news_list(
#     skip: int = Query(0, description="跳过的记录数", lt=100), 
#     limit: int = Query(10, description="返回的记录数")
#     ):
#     return {"skip": skip, "limit": 10}

# @app.get("/library")
# async def libirary(
#     kind: str = Query("Python开发", min_length=5, max_length=255), 
#     price: int = Query(ge=50,le=100, description="返回的记录数")
#     ):
#     return {"kind": kind, "price": price}

# # 请求体
# class User_register(BaseModel):
#     username: str = Field(default="李四",min_length=2, max_length=10,description="用户名，长度要求2-10个字")
#     email: str = Field(min_length=3, max_length=20,description="邮箱")

# @app.post("/User_register")
# async def register(user: User_register):
#     return user

# # 响应器类型设置方式
# # 响应HTML类,装饰器中指定响应类
# @app.get("/html", response_class=HTMLResponse)
# async def get_html():
#     return "<h1>这是一级标题<h1>"

# # 响应文件类，返回响应对象
# @app.get("/file")
# async def get_file():
#     image_Path = r"C:\Users\rebirth\Pictures\李念婷\lnt.jpg"
#     return FileResponse(Path)

# # 中间件
# @app.middleware("http")
# async def middleware1(request, call_netx):
#     print("中间件1 start")
#     response = await call_netx(request)
#     print("中间件1 end")
#     return response

# @app.middleware("http")
# async def middleware2(request, call_netx):
#     print("中间件2 start")
#     response = await call_netx(request)
#     print("中间件2 end")
#     return response

# # 依赖注入
# # 创建依赖项
# async def common_parameters(
#         skip: int = Query(0, ge= 0),
#         limit: int = Query(10,le=60)
# ):
#     return{"skip":skip, "limit":limit}

# @app.get("/news/news_list_common")
# async def get_news_list_common(
#     commons = Depends(common_parameters) # 声明依赖项
# ):            
#     return commons