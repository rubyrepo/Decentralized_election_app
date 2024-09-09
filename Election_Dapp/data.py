from tinydb import TinyDB

db = TinyDB("voter_data.json")

def createDB():
    global db
    db = TinyDB("voter_data.json")

OTP = [345,346,347,348,349,350]

Voted_OTP = []

