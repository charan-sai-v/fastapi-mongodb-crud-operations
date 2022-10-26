from fastapi import FastAPI
from routes import routes
from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values(".env")

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGO_URL"])
    app.database = app.mongodb_client[config["MONGO_DB"]]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


# including the router
app.include_router(routes.router)




