from typing import Dict
from models import GameState
from storage import Storage

class MemoryStorage(Storage):
    def __init__(self):
        self._games: Dict[str, GameState] = {}
    
    async def get_game(self, game_id: str) -> GameState:
        if game_id not in self._games:
            # Create new game with empty 15x15 board
            self._games[game_id] = GameState(
                game_id=game_id,
                players={},
                board=[[None for _ in range(15)] for _ in range(15)],
                version=0
            )
        return self._games[game_id]
    
    async def save_game(self, game_state: GameState) -> None:
        self._games[game_state.game_id] = game_state
