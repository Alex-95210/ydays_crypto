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

@app.post("/b2c")
async def buyer_to_customer(numSerie, model, color, brandHash, buyerHash):
    token = bc.createToken(numSerie,model,color)
    transaction = bc.createTransaction(token, brandHash, buyerHash)
    message = bc.mine(data=transaction)
    if message == 2:
        raise HTTPException(status_code=400, detail=message,headers={"X-Error": "block chain invalid"})
    else :
        raise HTTPException(status_code=201, detail=message)
    
@app.put("/c2c")
async def customer_to_customer(token, ownerHash, buyerHash):
    transaction = bc.createTransaction(token, ownerHash, buyerHash)
    message = bc.mine(data=transaction)
    if message == 2:
        raise HTTPException(status_code=400, detail=message,headers={"X-Error": "block chain invalid"})
    else :
        raise HTTPException(status_code=204, detail=message)
    
@app.get("/owner")
async def get_current_owner(token):
    res = bc.findOwner(token)
    if res == 2:
        raise HTTPException(status_code=400, detail=res,headers={"X-Error": "token invalid"})
    else :
        raise HTTPException(status_code=200, detail=res)

@app.get("/fisrtSellDate")
async def get_fisrt_sell_date(token):
    res = bc.getFirstSellDate(token)
    if res == 2:
        raise HTTPException(status_code=400, detail=res,headers={"X-Error": "token invalid"})
    else :
        raise HTTPException(status_code=200, detail=res)

@app.get("/tokenInfos")
async def get_token_infos(token):
    res = bc.getTokenInfos(token)
    if res == 2:
        raise HTTPException(status_code=400, detail=res,headers={"X-Error": "token invalid"})
    else :
        raise HTTPException(status_code=200, detail=res)
    
@app.get("/integrity")
async def check_chain_integrity():
    message = bc.is_chain_valid()
    if message == False:
        raise HTTPException(status_code=400, detail="invalid block chain",headers={"X-Error": "block chain invalid"})
    else :
        raise HTTPException(status_code=200, detail="block chain valid")