from fastapi import FastAPI, HTTPException
import blockchain as blockchainClass

bc = blockchainClass.Blockchain()

description = """
HellChain API helps you to autenticate your helmet.

You will be able to:

* **Create block**
* **Create Nemesis Block**
* **Read block chain**
* **Read last block**
* **Check chain authenticity**
"""

app = FastAPI(
    title="HellChain",
    description=description,
    version="69",
    contact={
        "name": "HellChain API"
    }
)

@app.get("/")
async def full_chain():
    data = bc.get_db()
    return data

@app.post("/genesis")
async def genesis():
    message = bc.init_chain()
    if message == 2:
        raise HTTPException(status_code=400, detail="The genesis block already exist",headers={"X-Error": "The genesis block already exist"})
    else :
        raise HTTPException(status_code=201, detail="Genesis block created")

@app.get("/last_block")
async def last_block():
    message = bc.get_last_block()
    print(message)
    return message

@app.post("/mine")
async def mine_block(data):
    message = bc.mine(data=data)
    if message == 2:
        raise HTTPException(status_code=400, detail=data,headers={"X-Error": "block chain invalid"})
    else :
        raise HTTPException(status_code=201, detail=message)
    
@app.get("/integrity")
async def check_chain_integrity():
    message = bc.is_chain_valid()
    if message == False:
        raise HTTPException(status_code=400, detail="invalid block chain",headers={"X-Error": "block chain invalid"})
    else :
        raise HTTPException(status_code=200, detail="block chain valid")