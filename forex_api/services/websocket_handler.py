from fastapi.websockets import WebSocket

class WebSocketHandler:
    @staticmethod
    async def handle_connection(websocket: WebSocket):
        await websocket.accept()
        await websocket.send_json({"message": "WebSocket connection established"})
        await websocket.close()
