from fastapi.websockets import WebSocket, WebSocketDisconnect
import logging
from datetime import datetime

active_connections = []

class WebSocketHandler:
    
    async def handle_connection(websocket: WebSocket):
        await websocket.accept()
        active_connections.append(websocket)
        logging.info("New WebSocket client connected.")

        try:
            while True:
                # Keep the connection alive. In this case, we don't need to handle any messages from the client.
                await websocket.receive_text()
        except WebSocketDisconnect:
            active_connections.remove(websocket)
            logging.info("WebSocket client disconnected.")

    async def broadcast_order_status(order_id: str, status: str):
        """ Function to broadcast order status updates to all connected clients. """
        message = {
            "order_id": order_id,
            "status": status,
            "timestamp": str(datetime.utcnow())
        }
        
        for connection in active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logging.error(f"Error sending message: {e}")
                # Optionally, you can remove the connection if it fails
                active_connections.remove(connection)