# main.py
import uvicorn
from fastapi import FastAPI, Depends
from src.routes import contacts
from src.routes import user
from src.auth.auth import get_current_user
from src.models.models import UserDB

app = FastAPI()

app.include_router(contacts.router)
app.include_router(user.router)

@app.get("/")
async def start():
    return "Welcome to ContactsAPP!"

@app.get("/secret")
async def read_item(current_user: UserDB = Depends(get_current_user)):
    return {"message": 'secret router', "owner": current_user.email}

if __name__ == '__main__':
    uvicorn.run(
        "main:app", reload=True
    )

# uvicorn main:app --reload
