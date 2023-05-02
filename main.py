from fastapi import FastAPI
from route import register, user, admin, corp
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    #"https://qrpark.com.tr",
    "https://www.qrpark.com.tr",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(register.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(corp.router)
