from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router

app = FastAPI()

# Allow your frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later you can restrict to ["http://localhost:5500"] or your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)