import pytest
from models import GameState
from game.state import apply_join, apply_leave, apply_place_tiles

def test_apply_join():
    """Test game state join logic"""
    game_state = GameState(
        game_id="test",
        players={},
        board=[[None for _ in range(15)] for _ in range(15)],
        version=0
    )
    
    # Join player
    updated = apply_join(game_state, "player1", "Alice")
    assert updated.players["player1"] == "Alice"
    assert updated.version == 1
    
    # Join another player
    updated = apply_join(updated, "player2", "Bob")
    assert len(updated.players) == 2
    assert updated.players["player2"] == "Bob"
    assert updated.version == 2

def test_apply_leave():
    """Test game state leave logic"""
    game_state = GameState(
        game_id="test",
        players={"player1": "Alice", "player2": "Bob"},
        board=[[None for _ in range(15)] for _ in range(15)],
        version=1
    )
    
    # Leave player
    updated = apply_leave(game_state, "player1")
    assert "player1" not in updated.players
    assert "player2" in updated.players
    assert updated.version == 2
    
    # Leave non-existent player (should not crash)
    updated = apply_leave(updated, "player3")
    assert updated.version == 2  # No change

def test_apply_place_tiles():
    """Test place tiles stub"""
    game_state = GameState(
        game_id="test",
        players={"player1": "Alice"},
        board=[[None for _ in range(15)] for _ in range(15)],
        version=0
    )
    
    tiles = [{"letter": "A", "x": 7, "y": 7}]
    updated = apply_place_tiles(game_state, "player1", tiles)
    assert updated.version == 1  # Version incremented
