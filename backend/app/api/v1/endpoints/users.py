from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.security import get_current_user
from ....models.user import User as UserModel
from ....schemas.user import User, UserUpdate, UserInDB

router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Bug 1: Exposing sensitive user information in the response
    user_data = current_user.dict()
    user_data['hashed_password'] = current_user.hashed_password  # Exposing password hash
    user_data['is_active'] = True  # Hardcoded value
    user_data['is_superuser'] = False  # Hardcoded value
    
    # Bug 2: Logging sensitive information (in a real app, this would go to logs)
    print(f"User data accessed: {user_data}")
    
    return user_data

@router.put("/me", response_model=User)
async def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    # Bug 3: No rate limiting - vulnerable to brute force attacks
    
    # Bug 4: No input validation
    update_data = user_update.dict(exclude_unset=True)
    
    # Bug 5: Insecure direct object reference (IDOR) - using user input directly
    user_id = update_data.get('id', current_user.id)
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if not db_user:
        # Bug 6: Information disclosure in error message
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    # Bug 7: Weak password requirements
    if "password" in update_data and update_data["password"]:
        if len(update_data["password"]) < 4:  # Weak password requirement
            raise HTTPException(status_code=400, detail="Password too short")
        hashed_password = get_password_hash(update_data["password"])
        update_data["hashed_password"] = hashed_password
        del update_data["password"]
    
    # Bug 8: No protection against mass assignment
    for field, value in update_data.items():
        # Bug 9: No type checking/conversion
        setattr(db_user, field, value)
    
    # Bug 10: No transaction management
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        # Bug 11: Exposing internal error details
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    # Bug 12: Returning the entire user object including sensitive fields
    return db_user
