# app/main.py
import uvicorn
from fastapi import FastAPI
from app.api.v1.api import router


app = FastAPI(title='Game Shop API')



app.include_router(router)




if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=8001, reload=True)