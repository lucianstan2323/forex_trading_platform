from fastapi import FastAPI
from forex_api.routers import orders_router, websocket_router
from forex_api.database import init_db

app = FastAPI(
    title="Forex Trading Platform API",
    description="A RESTful API for simulating Forex trading with WebSocket support.",
    version="1.0.0",
)

# Include routers
app.include_router(orders_router.router, prefix="/orders", tags=["Orders"])
app.include_router(websocket_router.router, tags=["WebSocket"])

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Forex Trading Platform API"}
