import json
import boto3
from botocore.exceptions import ClientError
from models import GameState
from storage import Storage

class DynamoDBStorage(Storage):
    def __init__(self, table_name: str = "game-states"):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
    
    async def get_game(self, game_id: str) -> GameState:
        try:
            response = self.table.get_item(Key={'game_id': game_id})
            if 'Item' in response:
                return GameState(**response['Item']['game_state'])
        except ClientError:
            pass
        
        # Create new game if not found
        game_state = GameState(
            game_id=game_id,
            players={},
            board=[[None for _ in range(15)] for _ in range(15)],
            version=0
        )
        await self.save_game(game_state)
        return game_state
    
    async def save_game(self, game_state: GameState) -> None:
        self.table.put_item(
            Item={
                'game_id': game_state.game_id,
                'game_state': game_state.model_dump()
            }
        )
