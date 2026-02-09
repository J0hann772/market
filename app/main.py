
import uvicorn
from fastapi import FastAPI
from app.api.v1.api import router
from app.db import base


app = FastAPI(title='Game Shop API')



app.include_router(router)




if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)