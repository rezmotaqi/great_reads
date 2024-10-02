



from fastapi import APIRouter, Depends


router = APIRouter()



@router.post("/register")
async def register(user: UserCreate, auth_service: AuthService = Depends()):
    access_token = await auth_service.register_user(user)
    return {"access_token": access_token}

@router.post("/login")
async def login(user: UserLogin, auth_service: AuthService = Depends()):
    access_token = await auth_service.login_user(user)
    return {"access_token": access_token}


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user