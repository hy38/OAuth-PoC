from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.routes import auth_router

app = FastAPI()

# For CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth 라우터 추가
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the LINE OAuth Project"}
