from fastapi import FastAPI
import auth.config
from route import register,user


app = FastAPI()

app.include_router(register.router)
app.include_router(user.router)
