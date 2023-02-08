import json
import datetime

class Blockchain:
    def hello_world(test: str):

        return "hello "+test+" crypto world"

    def get_db():
        with open('blockchain_db.json', 'r') as db:
            data = json.load(db)
        return data

    def add_to_db(self, element_to_add):
        with open('blockchain_db.json', 'r') as db:
            data = json.load(db)
        with open('blockchain_db.json', "w") as db:
            data.append(element_to_add) 
            json.dump(data, db, indent=4)
        print("block added to db")

    def init_chain(self):
        initial_block = self.create_block(
            data="genesis block", proof=1, previous_hash="0", index=1
        )
        return initial_block

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
        print(block)
        print(type(block))
        self.add_to_db(block)
        return block