import fastapi
from blockchain import Blockchain

bc = Blockchain()

app = fastapi.FastAPI()


@app.get("/")
async def root():
    bc.get_db()
    message = bc.hello_world(test="bg")
    return {"message": message}

@app.get("/genesis")
async def genesis():
    message = bc.init_chain()
    return message