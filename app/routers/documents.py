# 专门负责文档接口。

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
import shutil
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# 定义上传目录
UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# 定义文件上传请求体
@router.post(
    "/upload",
    response_model=schemas.DocumentResponse,
    status_code=201
)
# 如果同一个请求同时有文件和其他字段，就使用 File + Form；此时不能再把另一部分声明成普通JSON Body。
def upload_document(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. 检查用户
    user_statement = select(models.User).where(
        models.User.id == user_id
    )

    user = db.scalars(user_statement).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # 2. 获取安全的原始文件名
    filename = Path(file.filename).name

    # 3. 检查文件类型
    suffix = Path(filename).suffix.lower()

    allowed_extensions = {
        ".pdf",
        ".doc",
        ".docx"
    }

    if suffix not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and Word files are allowed"
        )

    # 4. 先创建数据库记录
    document = models.Document(
        user_id=user_id,
        filename=filename,
        status="uploading"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # 5. 保存真实文件
    saved_filename = f"{document.id}_{filename}"

    file_path = UPLOAD_DIR / saved_filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        document.status = "uploaded"

        db.commit()
        db.refresh(document)

    except Exception:
        document.status = "failed"
        db.commit()

        raise HTTPException(
            status_code=500,
            detail="File upload failed"
        )

    return document

# 创建文件上传
@router.post(
    "",
    response_model=schemas.DocumentResponse,
    status_code=201
)
def create_document(
    document_data: schemas.DocumentCreate,
    db: Session = Depends(get_db)
):
    # 先检查这个用户是否真的存在
    user_statement = select(models.User).where(
        models.User.id == document_data.user_id
    )

    user = db.scalars(user_statement).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # 创建Document ORM对象
    document = models.Document(
        user_id=document_data.user_id,
        filename=document_data.filename,
        status="uploaded"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

# 查询所有文档
@router.get(
    "",
    response_model=list[schemas.DocumentResponse]
)
def get_documents(
    db: Session = Depends(get_db)
):
    statement = select(models.Document)
    documents = db.scalars(statement).all()
    return documents

# 根据文档ID查询一份文档
@router.get(
    "/{document_id}",
    response_model=schemas.DocumentResponse
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    
    statement = select(models.Document).where(
        models.Document.id == document_id
    )

    document = db.scalars(statement).first()

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document

# 查询某个用户的所有文档
@router.get(
    "/user/{user_id}",
    response_model=list[schemas.DocumentResponse]
)
def get_user_documents(
    user_id: int,
    db: Session = Depends(get_db)
):
    # 先检查用户是否存在
    user_statement = select(models.User).where(
        models.User.id == user_id
    )

    user = db.scalars(user_statement).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # 查询属于这个用户的全部文档
    document_statement = select(models.Document).where(
        models.Document.user_id == user_id
    )

    documents = db.scalars(
        document_statement
    ).all()

    return documents

# 删除文档
@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    statement = select(models.Document).where(
        models.Document.id == document_id
    )

    document = db.scalars(statement).first()

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted"
    }