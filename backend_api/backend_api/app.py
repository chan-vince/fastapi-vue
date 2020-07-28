import fastapi
from fastapi.middleware.cors import CORSMiddleware

from backend_api import __version__
from backend_api.config import OPENAPI_DESCRIPTION
from .rest import practices, employees, access_systems, change_requests

# Create the root instance of a FastAPI app
app = fastapi.FastAPI(title="GP Access Systems PoC API",
                      version=__version__,
                      description=OPENAPI_DESCRIPTION)

origins = [
        "http://127.0.0.1:8081",
        "http://localhost:8081",
        "http://127.0.0.1:80",
        "http://localhost:80",
        "http://78.47.251.229:40093",
        "https://abys.prelim.cloud"
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="https://.*\.prelim\.cloud",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    practices.router, tags=["Practices"], prefix=f"/api/v1"
)
app.include_router(
    employees.router, tags=["Employees"], prefix=f"/api/v1"
)
app.include_router(
    access_systems.router, tags=["Access Systems"], prefix=f"/api/v1"
)
app.include_router(
    change_requests.router, tags=["Change Requests"], prefix=f"/api/v1"
)
# app.include_router(
#     staging_changes.router, tags=["Staging Unified"], prefix=f"/api/v1"
# )