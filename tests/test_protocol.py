import pytest
from models import *

def test_join_game_message():
    """Test basic protocol parse/build for join_game"""
    data = {
        "type": "join_game",
        "player_id": "player1",
        "player_name": "Alice"
    }
    
    msg = JoinGameMessage(**data)
    assert msg.type == "join_game"
    assert msg.player_id == "player1"
    assert msg.player_name == "Alice"
    
    # Round-trip
    serialized = msg.model_dump()
    assert serialized == data

def test_game_state_response():
    """Test game state response serialization"""
    game_state = GameState(
        game_id="test",
        players={"p1": "Alice"},
        board=[[None for _ in range(15)] for _ in range(15)],
        version=1
    )
    
    response = GameStateResponse(game_state=game_state)
    assert response.type == "game_state"
    
    serialized = response.model_dump()
    assert serialized["type"] == "game_state"
    assert serialized["game_state"]["game_id"] == "test"

def test_error_response():
    """Test error response"""
    error = ErrorResponse(message="Test error")
    assert error.type == "error"
    assert error.message == "Test error"
