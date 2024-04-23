# main.py
import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, Depends
from src.routes import contacts
from src.routes import user
from src.auth.auth import auth_service
from src.models.models import UserDB
from src.conf.config import settings
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [ 
    "http://localhost:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router)
app.include_router(user.router)

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/")
async def start():
    return "Welcome to ContactsAPP!"

@app.get("/secret")
async def read_item(current_user: UserDB = Depends(auth_service.get_current_user)):
    return {"message": 'secret router', "owner": current_user.email}

if __name__ == '__main__':
    uvicorn.run(
        "main:app", reload=True
    )

# uvicorn main:app --reload
