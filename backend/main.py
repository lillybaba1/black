from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
import uuid
import jwt
from datetime import datetime, timedelta

# In-memory stores (for demo purposes)
users_db = {}
groups_db = {}
posts_db = []
chats = {}

SECRET_KEY = "SECRET"  # Replace with env var in production

app = FastAPI(title="Uni-One Backend")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

class User(BaseModel):
    username: str
    password: str
    avatar_url: str | None = None
    bio: str | None = None
    country: str | None = None

class Group(BaseModel):
    id: str
    name: str
    description: str

class Post(BaseModel):
    id: str
    author: str
    content: str
    timestamp: datetime
    group_id: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = user
    return {"msg": "registered"}

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = jwt.encode({"sub": user.username, "exp": datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        return users_db.get(username)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/groups")
def create_group(group: Group, user: User = Depends(get_current_user)):
    groups_db[group.id] = group
    return group

@app.post("/posts")
def create_post(content: str, group_id: str | None = None, user: User = Depends(get_current_user)):
    post = Post(id=str(uuid.uuid4()), author=user.username, content=content, timestamp=datetime.utcnow(), group_id=group_id)
    posts_db.append(post)
    return post

@app.get("/posts", response_model=List[Post])
def list_posts():
    return posts_db

@app.websocket("/ws/{group_id}")
async def websocket_endpoint(websocket: WebSocket, group_id: str):
    await websocket.accept()
    chats.setdefault(group_id, set()).add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast to all connections in the group
            for conn in list(chats[group_id]):
                await conn.send_text(data)
    except WebSocketDisconnect:
        chats[group_id].remove(websocket)


@app.post("/ai/caption")
def generate_caption(prompt: str):
    caption = prompt[::-1]
    return {"caption": caption}
