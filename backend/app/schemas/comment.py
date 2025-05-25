from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Any, Dict, TypeVar, Type

# For forward references
ModelT = TypeVar('ModelT', bound=BaseModel)

class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass

class CommentInDBBase(CommentBase):
    id: int
    task_id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Comment(CommentInDBBase):
    # Using string literal for forward reference
    author: 'dict'  # Will be converted to User in the validator
    
    @classmethod
    def model_validate(
        cls: Type[ModelT],
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: Dict[str, Any] | None = None
    ) -> ModelT:
        # Convert author dict to User model if needed
        if isinstance(obj, dict) and 'author' in obj and isinstance(obj['author'], dict):
            from .user import User
            obj['author'] = User.model_validate(obj['author'])
        return super().model_validate(obj, strict=strict, from_attributes=from_attributes, context=context)
    
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "content": "This is a comment",
                "task_id": 1,
                "user_id": 1,
                "created_at": "2023-01-01T00:00:00",
                "author": {
                    "id": 1,
                    "email": "user@example.com",
                    "full_name": "John Doe",
                    "is_active": True,
                    "is_superuser": False
                }
            }
        }
    )

class CommentInDB(CommentInDBBase):
    pass
