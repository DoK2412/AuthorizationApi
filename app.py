import os


import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from servise.route import router

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))