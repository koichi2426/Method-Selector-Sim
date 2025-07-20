from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.router.fastapi import router

app = FastAPI()

# フロントエンドからのアクセスを許可するためのCORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Next.jsのオリジン
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを組み込む
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello from Backend!"}