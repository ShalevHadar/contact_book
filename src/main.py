from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from server.src import models, database
from server.src.api.v1.endpoints import contacts

app = FastAPI(title="Phone Book API")

# cors for front localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)
app.include_router(contacts.router)

if __name__ == "__main__":
    server_port = os.getenv("PORT", 8001)
    uvicorn.run("server.src.main:app", host="0.0.0.0", port=int(server_port), reload=True)
