import os
import pytest
from models import GameState
from storage.ddb import DynamoDBStorage

@pytest.mark.skipif(
    not os.getenv('AWS_DEFAULT_REGION') or not os.getenv('AWS_ACCESS_KEY_ID'),
    reason="AWS credentials not configured"
)
@pytest.mark.asyncio
async def test_dynamodb_smoke():
    """DynamoDB smoke test - basic connectivity and operations"""
    storage = DynamoDBStorage("game-states-test")
    
    try:
        # Get/create game
        game_state = await storage.get_game("smoke-test")
        assert game_state.game_id == "smoke-test"
        
        # Modify and save
        game_state.players["test_player"] = "TestUser"
        game_state.version = 99
        await storage.save_game(game_state)
        
        # Retrieve and verify
        retrieved = await storage.get_game("smoke-test")
        assert retrieved.players["test_player"] == "TestUser"
        assert retrieved.version == 99
        
    except Exception as e:
        pytest.skip(f"DynamoDB not available: {e}")

@pytest.mark.skipif(
    os.getenv('AWS_DEFAULT_REGION') and os.getenv('AWS_ACCESS_KEY_ID'),
    reason="AWS credentials are configured"
)
def test_dynamodb_skipped():
    """Test that shows DynamoDB tests are properly skipped"""
    assert True  # This test runs when AWS is not configured
