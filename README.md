# Word Game Server

Minimal multiplayer game server using FastAPI, WebSockets, and DynamoDB.

## Quick Start

### 1. Setup Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -e .
# OR
pip install -r requirements.txt
```

### 3. Run Tests (Optional)
```bash
pip install -e .[test]
pytest
```

### 4. Run Server
```bash
uvicorn app:app --reload
```

Server runs at http://localhost:8000

### 5. Create DynamoDB Table (Optional)

For production use with DynamoDB:

```bash
aws dynamodb create-table \
    --table-name game-states \
    --attribute-definitions AttributeName=game_id,AttributeType=S \
    --key-schema AttributeName=game_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

Set AWS credentials and region:
```bash
export AWS_DEFAULT_REGION=us-east-1
```

## Test Client

Save as `client.py` and run with `python client.py`:

```python
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
```

## Message Types

- `join_game`: Add player to game
- `leave_game`: Remove player from game  
- `request_state`: Get current game state
- `place_tiles`: Place tiles on board (stub)

## Architecture

- `app.py`: FastAPI server with WebSocket endpoints
- `models.py`: Pydantic models for game state and messages
- `storage/`: Storage abstraction with memory and DynamoDB implementations
- `game/state.py`: Game logic functions

## TODO

- [ ] Implement full tile placement validation
- [ ] Add turn management
- [ ] Implement scoring system
- [ ] Add authentication
- [ ] Add game room management
- [ ] Add spectator mode
