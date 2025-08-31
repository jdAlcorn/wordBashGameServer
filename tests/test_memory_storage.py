import pytest
from models import GameState
from storage.memory import MemoryStorage

@pytest.mark.asyncio
async def test_memory_storage_crud():
    """Test memory storage CRUD round-trip"""
    storage = MemoryStorage()
    
    # Get new game (creates it)
    game_state = await storage.get_game("test-game")
    assert game_state.game_id == "test-game"
    assert game_state.players == {}
    assert len(game_state.board) == 15
    assert game_state.version == 0
    
    # Modify and save
    game_state.players["player1"] = "Alice"
    game_state.version = 1
    await storage.save_game(game_state)
    
    # Retrieve and verify
    retrieved = await storage.get_game("test-game")
    assert retrieved.players["player1"] == "Alice"
    assert retrieved.version == 1
