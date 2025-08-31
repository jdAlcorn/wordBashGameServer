from abc import ABC, abstractmethod
from models import GameState

class Storage(ABC):
    @abstractmethod
    async def get_game(self, game_id: str) -> GameState:
        pass
    
    @abstractmethod
    async def save_game(self, game_state: GameState) -> None:
        pass
