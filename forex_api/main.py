from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError  # Import RequestValidationError
from fastapi.responses import JSONResponse
from forex_api.routers import orders_router, websocket_router, health_router
from forex_api.database import init_db

app = FastAPI(
    title="Forex Trading Platform API",
    description="A RESTful API for simulating Forex trading with WebSocket support.",
    version="1.0.0",
)

# Include routers
app.include_router(health_router.router, tags=["Health"])
app.include_router(orders_router.router, prefix="/orders", tags=["Orders"])
app.include_router(websocket_router.router, tags=["WebSocket"])

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Forex Trading Platform API"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    # This handler catches validation errors and returns a 400 Bad Request instead of the default 422
    return JSONResponse(
        status_code=400,  # Override 422 with 400
        content={"detail": "Invalid input"}
    )
