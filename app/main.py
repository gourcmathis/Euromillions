from domain import predict
from domain import model
from fastapi import FastAPI

NAME = "Eurosimulateur"

app = FastAPI(
    title="Eurosimulateur",
    version="1.0"
)

app.include_router(predict.router)
app.include_router(model.router)