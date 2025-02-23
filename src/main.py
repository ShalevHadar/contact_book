from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from contact_book.src.api.contacts import models
from contact_book.shared import database
from contact_book.src.api.contacts.routes import router

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
app.include_router(router)

if __name__ == "__main__":
    server_port = os.getenv("PORT", 8001)
    uvicorn.run("contact_book.src.main:app", host="0.0.0.0", port=int(server_port), reload=True)
