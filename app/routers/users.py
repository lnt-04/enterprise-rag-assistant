# 专门负责用户接口。
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models, schemas
from app.database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# 创建用户 请求体
@router.post("", response_model=schemas.UserResponse, status_code=201)
def create_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    
    # 检查用户名是否重复
    statement = select(models.User).where(
        models.User.username == user_data.username
    )

    existing_user = db.scalars(statement).first()

    if existing_user is not None:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )
    # 检查邮箱是否重复
    email_statement = select(models.User).where(
        models.User.email == user_data.email
    )

    existing_email = db.scalars(
        email_statement
    ).first()

    if existing_email is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )
    # 创建ORM对象
    user = models.User(
        username=user_data.username,
        email=user_data.email
    )
# 保存到数据库
    db.add(user)
    db.commit() # 提交事务
    db.refresh(user) # 从数据库把最新的数据刷新回这个Python对象。

    return user

# 创建单个用户查询
@router.get("/{user_id}", response_model=schemas.UserResponse) # 返回的数据，应该整理成 UserResponse 的格式。
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    # SQL查询语句对象。先写语句
    statement = select(models.User).where( 
        models.User.id == user_id
    )
# 用当前Session执行刚才这条查询语句，并获取ORM对象结果。再查询
    user = db.scalars(statement).first()  

# 错误处理
    if user is None:
        #如果用户不存在，就主动结束请求，并返回404。
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

# 查询所有用户，如果数据为空则返回空列表[]
@router.get("", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    statement = select(models.User)

    users = db.scalars(statement).all()

    return users