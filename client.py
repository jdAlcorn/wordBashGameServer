import asyncio
import websockets
import json

async def test_client():
    uri = "ws://localhost:8000/ws/test-game"
    
    async with websockets.connect(uri) as websocket:
        # Join game
        join_msg = {
            "type": "join_game",
            "player_id": "player1",
            "player_name": "Alice"
        }
        await websocket.send(json.dumps(join_msg))
        response = await websocket.recv()
        print("Join response:", response)
        
        # Request current state
        state_msg = {"type": "request_state"}
        await websocket.send(json.dumps(state_msg))
        response = await websocket.recv()
        print("State response:", response)
        
        # Place tiles (stub)
        tiles_msg = {
            "type": "place_tiles",
            "player_id": "player1",
            "tiles": [{"letter": "A", "x": 7, "y": 7}]
        }
        await websocket.send(json.dumps(tiles_msg))
        response = await websocket.recv()
        print("Tiles response:", response)

if __name__ == "__main__":
    asyncio.run(test_client())
