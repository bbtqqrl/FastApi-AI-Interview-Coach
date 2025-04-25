from fastapi import Depends, HTTPException, status
from auth.dependencies import get_current_user 

def verify_admin(user_data: dict = Depends(get_current_user)):
    print(user_data)
    print(user_data.get("is_admin"))
    if not user_data.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: admin only"
        )
    return user_data
