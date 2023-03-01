import json
import datetime
import hashlib

class Blockchain:
    #fonction qui récupère la bdd
    @staticmethod
    def get_db():
        with open('blockchain_db.json', 'r') as db:
            data = json.load(db)
            print
        return data
    # fonction d'ajout en bdd
    def add_to_db(self, element_to_add):
        data = self.get_db()
        with open('blockchain_db.json', "w") as db:
            data.append(element_to_add) 
            json.dump(data, db, indent=4)
        print("block added to db")

    #fonction de création du block nemesis
    def init_chain(self):
        db = self.get_db()
        if len(db) < 1:
            res = self.create_block(
                data="genesis block", proof=1, previous_hash="0", index=1
            )
            self.add_to_db(res)
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
        print("block "+str(index)+" created")
        return block
    
    #renvoi le dernier block créé
    def get_last_block(self):
        chain = self.get_db()
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
    def mine(self, data: str) -> dict:
        last_block = self.get_last_block()
        last_proof = last_block["proof"]
        index = len(self.get_db()) + 1
        proof = self.proof_of_work(
            previous_proof=last_proof, index=index, data=data
        )
        previous_hash = self.hash(block=last_block)
        block = self.create_block(
            data=data, proof=proof, previous_hash=previous_hash, index=index
        )
        self.add_to_db(block)
        return block

    #fonction qui renvoi le hash d'un block
    def hash(self, block: dict) -> str:
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    #fonction de verification de l'intégrité de la chaine 
    def is_chain_valid(self) -> bool:
        chain = self.get_db()
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