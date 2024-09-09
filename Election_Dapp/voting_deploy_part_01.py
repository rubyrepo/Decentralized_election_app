import json

import web3
from web3 import Web3
from solcx import compile_standard, install_solc

print("Starting to install ...")
install_solc('0.8.0')
print("Finished installation!")

with open("./Election.sol","r") as file:
    election_list_file = file.read()
    print(election_list_file)

compiled_sol = compile_standard(
    {
    "language": "Solidity",
    "sources": {"Election.sol": {"content": election_list_file}},
    "settings": {
    "outputSelection": {
    "*": {
    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
    )

with open("compiled_code_election.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["Election.sol"]["Election"]["evm"]["bytecode"]["object"]

# get abi
abi = json.loads(compiled_sol["contracts"]["Election.sol"]["Election"]["metadata"])["output"]["abi"]

w3 = Web3(web3.HTTPProvider("http://127.0.0.1:8545"))

chain_id = 1337

print(f'This is the connection status : {w3.isConnected()}')


