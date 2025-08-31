import json
import logging
from typing import Dict, Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from models import *
from storage.memory import MemoryStorage
from storage.ddb import DynamoDBStorage
from game.state import apply_join, apply_leave, apply_place_tiles
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Word Game Server")

# Use DynamoDB if AWS credentials available, otherwise memory storage
try:
    storage = DynamoDBStorage() if os.getenv('AWS_DEFAULT_REGION') else MemoryStorage()
    logger.info(f"Using storage: {type(storage).__name__}")
except Exception:
    storage = MemoryStorage()
    logger.info("Falling back to MemoryStorage")

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, game_id: str):
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = set()
        self.active_connections[game_id].add(websocket)
        logger.info(f"Client connected to game {game_id}")
    
    def disconnect(self, websocket: WebSocket, game_id: str):
        if game_id in self.active_connections:
            self.active_connections[game_id].discard(websocket)
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]
        logger.info(f"Client disconnected from game {game_id}")
    
    async def broadcast_to_game(self, game_id: str, message: dict):
        if game_id in self.active_connections:
            for connection in self.active_connections[game_id].copy():
                try:
                    await connection.send_text(json.dumps(message))
                except Exception:
                    self.active_connections[game_id].discard(connection)

manager = ConnectionManager()

@app.get("/")
async def get():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>Word Game Server</title></head>
    <body>
        <h1>Word Game Server</h1>
        <p>Connect to WebSocket at: ws://localhost:8000/ws/{game_id}</p>
    </body>
    </html>
    """)

@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}

@app.get("/ws/healthz")
async def ws_health_check():
    return {"status": "healthy"}

@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    await manager.connect(websocket, game_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            try:
                # Get current game state
                game_state = await storage.get_game(game_id)
                
                # Process message based on type
                if message_data["type"] == "join_game":
                    msg = JoinGameMessage(**message_data)
                    game_state = apply_join(game_state, msg.player_id, msg.player_name)
                    await storage.save_game(game_state)
                    
                elif message_data["type"] == "leave_game":
                    msg = LeaveGameMessage(**message_data)
                    game_state = apply_leave(game_state, msg.player_id)
                    await storage.save_game(game_state)
                    
                elif message_data["type"] == "request_state":
                    # Just return current state
                    pass
                    
                elif message_data["type"] == "place_tiles":
                    msg = PlaceTilesMessage(**message_data)
                    game_state = apply_place_tiles(game_state, msg.player_id, msg.tiles)
                    await storage.save_game(game_state)
                
                # Broadcast updated state to all clients in game
                response = GameStateResponse(game_state=game_state)
                await manager.broadcast_to_game(game_id, response.model_dump())
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                error_response = ErrorResponse(message=str(e))
                await websocket.send_text(json.dumps(error_response.model_dump()))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
