from fastapi import FastAPI
from src.contacts.routes import contact_router
from .errors import register_all_errors
from .middleware import register_middleware

version = "v1"

description = """
A REST API for a book review web service.

This REST API is able to;
- Create Read Update And delete books
- Add reviews to books
- Add tags to Books e.t.c.
    """

version_prefix = f"/api/{version}"

app = FastAPI(
    title="Contact API",
    description=description,
    version=version,
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
)

register_all_errors(app)
register_middleware(app)


app.include_router(contact_router, prefix=f"{version_prefix}/contact", tags=["auth"])
