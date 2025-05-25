from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ....core.database import get_db
from ....core.security import get_current_user
from ....models.task import Task as TaskModel
from ....models.project import Project as ProjectModel
from ....models.comment import Comment as CommentModel
from ....schemas.task import Task, TaskCreate, TaskUpdate
from ....schemas.comment import Comment, CommentCreate
from ....schemas.user import UserInDB

router = APIRouter()

def get_task(db: Session, task_id: int, user_id: int):
    return db.query(TaskModel).join(
        ProjectModel,
        ProjectModel.owner_id == user_id
    ).filter(
        TaskModel.id == task_id
    ).first()

@router.get("/", response_model=List[Task])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    project_id: Optional[int] = None,
    assignee_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    query = db.query(TaskModel).join(
        ProjectModel,
        ProjectModel.owner_id == current_user.id
    )
    
    if status:
        query = query.filter(TaskModel.status == status)
    if project_id is not None:
        query = query.filter(TaskModel.project_id == project_id)
    if assignee_id is not None:
        query = query.filter(TaskModel.assignee_id == assignee_id)
    
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    # Verify project exists and is owned by user
    project = db.query(ProjectModel).filter(
        ProjectModel.id == task.project_id,
        ProjectModel.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    
    # Verify assignee exists if provided
    if task.assignee_id:
        assignee = db.query(UserModel).filter(UserModel.id == task.assignee_id).first()
        if not assignee:
            raise HTTPException(status_code=400, detail="Assignee not found")
    
    db_task = TaskModel(
        **task.model_dump(),
        created_by=current_user.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=Task)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    task = get_task(db, task_id, current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_task = get_task(db, task_id, current_user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task.model_dump(exclude_unset=True)
    
    # Verify project exists and is owned by user if project_id is being updated
    if 'project_id' in update_data:
        project = db.query(ProjectModel).filter(
            ProjectModel.id == update_data['project_id'],
            ProjectModel.owner_id == current_user.id
        ).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found or access denied")
    
    # Verify assignee exists if assignee_id is being updated
    if 'assignee_id' in update_data and update_data['assignee_id'] is not None:
        assignee = db.query(UserModel).filter(UserModel.id == update_data['assignee_id']).first()
        if not assignee:
            raise HTTPException(status_code=400, detail="Assignee not found")
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_task = get_task(db, task_id, current_user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"ok": True}

@router.post("/{task_id}/comments", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(
    task_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    task = get_task(db, task_id, current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_comment = CommentModel(
        **comment.model_dump(),
        task_id=task_id,
        user_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/{task_id}/comments", response_model=List[Comment])
def read_task_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    task = get_task(db, task_id, current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return db.query(CommentModel).filter(
        CommentModel.task_id == task_id
    ).all()
