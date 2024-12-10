from fastapi import APIRouter, WebSocket
from forex_api.services.websocket_handler import WebSocketHandler

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await WebSocketHandler.handle_connection(websocket)
