import pymongo
from decouple import config
from pprint import pprint

MONGO_URL = config(
    "MONGO_URL",
    default="###",
    cast=str,
)

client = pymongo.MongoClient(MONGO_URL)

db = client.bank
collection = db.bank_collection

clients = [
    {
        "name": "Rafael",
        "cpf": "12390856478",
        "address": "Rua X",
        "acc_type": "cc",
        "agency": "0001",
        "acc_num": "21012445801",
        "credit": 800.40,
    },
    {
        "name": "Jorge",
        "cpf": "591321310504",
        "address": "Rua Y",
        "acc_type": "cp",
        "agency": "0001",
        "acc_num": "892304407840",
        "credit": 10.90,
    },
]

insert_clients = db.insert_clients
insert = clients.insert_many(clients)

print("Recupera o primeiro cliente a ter uma Conta Poupança")
pprint(db.insert_clients.find_one({"acc_type": "cp"}))

print("\nRecuperando todos os documentos")
for document in insert_clients.find():
    pprint(document)
