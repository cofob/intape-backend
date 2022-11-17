"""InTape Backend."""
# Order makes sense here, as the app is created in the first line.
from .app import app

# Make some work here, to bypass the isort formatter.
some = "work"

from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

# Import all other modules here.
from . import (  # noqa: E402
    core,
    dependencies,
    models,
    routes,
    schemas,
    security,
    utils,
)

__all__ = ["app", "routes", "exceptions", "models", "utils", "schemas", "security", "dependencies", "core"]

app.include_router(routes.router)
# cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(core.middlewares.DBAsyncSessionMiddleware)
