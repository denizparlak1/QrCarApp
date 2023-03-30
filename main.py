from fastapi import FastAPI
import auth.config
from route import register,user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    #"https://daglarapp.ey.r.appspot.com",
    #"https://qrcarapp-akzshgayzq-uc.a.run.app"
    "http://qrpark.com.tr",
    "https://qrpark.com.tr"
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
