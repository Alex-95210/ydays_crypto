import json
import datetime
import hashlib
import os
from glob import glob

class Blockchain:
    #fonction qui récupère la bdd
    @staticmethod
    def get_db(port):
        blockChain = []
        path_to_json = 'db'+str(port)+'/'

        for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:
            with open(path_to_json + file_name) as json_file:
                data = json.load(json_file)
                blockChain.append(data)
        return blockChain
    
    # fonction d'ajout en bdd
    def add_to_db(self, element_to_add, port,index):
        with open('db'+str(port)+'/'+str(index)+'.json', "x") as db:
            json.dump(element_to_add, db, indent=4)
    
    #fonction de suppression de block
    def remove_last_block(self, index, port):
        os.remove('db'+str(port)+'/'+str(index)+'.json')

    #fonction de création du block nemesis
    def init_chain(self):
        db = self.get_db()
        if len(db) < 1:
            res = self.create_block(
                data="genesis-block,first,one", proof=1, previous_hash="0", index=1
            )
            self.add_to_db(res,1)
        else : 
            res = 2
        print("genesis block created")
        return res
    
    #fonction de création de block
    def create_block(
        self, data: str, proof: int, previous_hash: str, index: int
    ) -> dict:
        block = {
            "index": index,
            "timestamp": str(datetime.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash,
        }
        return block
    
    #renvoi le dernier block créé
    def get_last_block(self, port):
        chain = self.get_db(port)
        return chain[-1]
    
    #fonction de calcul de la proof
    def proof_of_work(self, previous_proof: str, index: int, data: str) -> int:
        proof = 1
        check_proof = False
        #hash jusqu'à ce que les 4 premiers caractères du hash soient 0000
        while not check_proof:
            steak = self.steak(proof, previous_proof, index, data)
            steak_hashed = hashlib.sha256(steak).hexdigest()
            if steak_hashed[:4] == "0000":
                check_proof = True
            else:
                proof += 1

        return proof

    # fonction qui encode (en utf-8) la proof combinées avec la proof du block précédent, l'index du block actuel et sa data
    def steak(
        self, proof: int, previous_proof: int, index: int, data: str
    ) -> bytes:
        steak = str(proof + previous_proof + index) + data
        return steak.encode()

    #fonction pour miner un block 
    def mine(self, data: str, port) -> dict:
        last_block = self.get_last_block(port)
        last_proof = last_block["proof"]
        index = len(self.get_db(port)) + 1
        proof = self.proof_of_work(
            previous_proof=last_proof, index=index, data=data
        )
        previous_hash = self.hash(block=last_block)
        block = self.create_block(
            data=data, proof=proof, previous_hash=previous_hash, index=index
        )
        self.add_to_db(block, port, index)
        return block

    #fonction qui renvoi le hash d'un block
    def hash(self, block: dict) -> str:
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    #fonction de verification de l'intégrité de la chaine 
    def is_chain_valid(self, chain) -> bool:
        # chain = self.get_db()
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            # on verifie si le previous hash correspond bien au hash du block précédent
            if block["previous_hash"] != self.hash(previous_block):
                return False

            previous_proof = previous_block["proof"]
            index, data, proof = block["index"], block["data"], block["proof"]
            hash_operation = hashlib.sha256(
                self.steak(
                    proof=proof,
                    previous_proof=previous_proof,
                    index=index,
                    data=data,
                )
            ).hexdigest()
            # on verifie si le hash du block commence bien par "0000"
            if hash_operation[:4] != "0000":
                return False

            previous_block = block
            block_index += 1

        return True
    #
    def createToken(self,numSerie: str, model: str, color: str):
        token = str(numSerie + model + color)
        tokenHashed = hashlib.sha256(token.encode('utf-8')).hexdigest()
        return tokenHashed

    def createTransaction(self,token: str, previousOwner: str, newOwner: str):
        transaction = str(str(token)+","+previousOwner+","+newOwner)
        return transaction
    
    def findOwner(self, token: str, port):
        chain = self.get_db(port)
        block_index = len(chain) -1

        while block_index > 0:
            block = chain[block_index]
            block_index -= 1
            print(block["data"].split(',')[0])
            if block["data"].split(',')[0] == token :
                return block["data"].split(',')[2]
    
        return 2
    
    def get_helmet_age(self, token: str, port):
        chain = self.get_db(port)
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block["data"].split(',')[0] == token :
                buyDate = datetime.datetime.strptime(block["timestamp"].replace(' ', '-'),'%Y-%m-%d-%H:%M:%S.%f')
                difference = datetime.datetime.now().year - buyDate.year
                return str(difference)
            block_index += 1
    
        return "error"
    
    def checkHelmetAuthenticity(self, serieNum, model, color,port):
        chain = self.get_db(port)
        block_index = 1
        token = self.createToken(serieNum, model, color)
        while block_index < len(chain):
            block = chain[block_index]
            if block["data"].split(',')[0] == token :
                return True
            block_index += 1
    
        return False