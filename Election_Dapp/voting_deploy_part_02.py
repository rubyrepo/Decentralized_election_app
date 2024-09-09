import json
from web3 import Web3
from solcx import install_solc, compile_standard
from voting_deploy_part_01 import w3, abi, bytecode, chain_id
from Keys import my_address, private_key

# Write the functions here!

# These are global variables
tx_receipt = None
nonce = None
election = None
contract_address = None

flag = True

def DEPLOY():
    Election = w3.eth.contract(abi=abi,bytecode=bytecode)
    global nonce
    nonce = w3.eth.get_transaction_count(my_address)
    print(nonce)  #  -> The nonce will be zero!
    transaction = Election.constructor().build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )
    nonce = nonce + 1
    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Deploying the Contract!")
    # Send it!
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    global tx_receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done! Contract deployed to {tx_receipt.contractAddress}")
    global contract_address
    contract_address = tx_receipt.contractAddress
    print("-------------------------")
    print(tx_receipt)
    print(type(tx_receipt))
    global flag
    flag = False


def PLACEVOTE(vote):
    global tx_receipt
    global contract_address
    global nonce
    Election = w3.eth.contract(address=contract_address, abi=abi)
    # Working with deployed Contracts
    create_transaction = Election.functions.placeVote(vote).build_transaction(
    {
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "from": my_address,
    "nonce": nonce,
    }
    )
    nonce = nonce + 1
    signed_create_txn = w3.eth.account.sign_transaction(
    create_transaction, private_key=private_key
    )
    tx_create_hash = w3.eth.send_raw_transaction(signed_create_txn.rawTransaction)
    print("casting the vote...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_create_hash)
    print("vote has been successfully placed.......")


def VIEWVOTESTATUS():
    global tx_receipt
    global election
    Election = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

    votestatus = Election.functions.viewVoteStatus().call(
    {
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "from": my_address,
    "nonce": nonce,
    "to": contract_address

    }
    )
    print(votestatus)
    return votestatus

def DEPLOY_ONCE():
    global flag
    if(flag):
        DEPLOY()


