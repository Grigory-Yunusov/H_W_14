"""
Main application entry point.

This module initializes the FastAPI application, sets up middleware, includes routers,
and defines the startup event for initializing the rate limiter.

Attributes:
    app (FastAPI): The main FastAPI application instance.
"""

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

# Initialize the FastAPI application
app = FastAPI()

# Define the origins that are allowed to make cross-origin requests
origins = [ 
    "http://localhost:3000"
    ]
# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the contacts and user routers
app.include_router(contacts.router)
app.include_router(user.router)

@app.on_event("startup")
async def startup():
    """
    Initializes the rate limiter by connecting to the Redis server.
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/")
async def start():
    """
    Welcome endpoint.

    :return: A welcome message.
    :rtype: str
    """
    return "Welcome to ContactsAPP!"

@app.get("/secret")
async def read_item(current_user: UserDB = Depends(auth_service.get_current_user)):
    """
    A protected endpoint that requires authentication.

    :param current_user: The currently authenticated user.
    :type current_user: UserDB
    :return: A message indicating that this is a secret router and the email of the owner.
    :rtype: dict
    """
    return {"message": 'secret router', "owner": current_user.email}

if __name__ == '__main__':
    """
    Entry point for the application.

    Starts the Uvicorn server with the 'main:app' parameter to specify the module and app instance.
    The '--reload' flag is used to enable hot reloading, which means the server will restart whenever
    the code changes. This is useful during development.
    """
    uvicorn.run(
        "main:app", reload=True
    )

# uvicorn main:app --reload
