from fastapi import FastAPI
from user.endpoints import router as user_endpoints

app = FastAPI()

app.include_router(user_endpoints, prefix="/users", tags=["users"])
