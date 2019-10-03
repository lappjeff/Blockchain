import hashlib
import requests
import json
import sys
from blockchain import Blockchain
from uuid import uuid4

valid_proof = Blockchain.valid_proof
# TODO: Implement functionality to search for a proof
def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    :return: A valid proof for the provided block
    """

    block_string = json.dumps(block, sort_keys=True).encode()

    proof = 0

    while valid_proof(block_string, proof) is False:
        proof += 1

    return proof

def get_recipient_id():
    id_file = open('my_id.txt', 'r')

    id = id_file.read()
    if len(id) > 0:
        return id
    else:
        id_file = open('my_id.txt', 'w')
        id_file.write(str(uuid4()).replace('-', ''))
        id_file = open('my_id.txt', 'r')
        id = id_file.read()
        print(f"Created new id {id}")
        return id

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"


    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        r = requests.get(url=f"{node}/last_block")
        block = r.json()['block']
        proof = proof_of_work(block)
        data = {"proof": proof, "recipient_id": get_recipient_id()}
        # TODO: When found, POST it to the server {"proof": new_proof}
        mine_request = requests.post(url=f"{node}/mine", json = data)
        data = mine_request.json()
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if data['message'] == "New Block Forged":
            coins_mined += 1
            print(f"{coins_mined} coins mined")
        else:
            print(f"{data['message']}")
