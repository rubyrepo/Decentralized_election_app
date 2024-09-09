import json

import web3
from web3 import Web3
from solcx import compile_standard, install_solc

print("Starting to install ...")
install_solc('0.8.0')
print("Finished installation!")

