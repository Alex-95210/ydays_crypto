from fastapi import FastAPI
from blockchain import Blockchain



app = FastAPI()


@app.get("/")
async def root():
    message = Blockchain.helloWorld(test="bg")
    return {"message": message}