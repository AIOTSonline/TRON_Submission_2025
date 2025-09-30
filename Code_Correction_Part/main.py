from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import router

# main FastAPI application instance
app = FastAPI(
    title="Blockly C++ AI Assistant",
    description="An application to test and correct C++ code using AI.",
    version="1.0.0"
)

# A list of origins that are allowed to make requests to this server.
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:5500", 
    "http://localhost:8080",
    "null", 
]

# CORS middleware to the application.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the API routes from the 'router' object in endpoints.py.
app.include_router(router)

# root endpoint to check if the server is running
@app.get("/", tags=["Root"], include_in_schema=False)
async def read_root():
    return {"message": "Blockly C++ AI Assistant API is running."}
