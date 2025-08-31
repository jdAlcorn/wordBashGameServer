from pydantic import BaseModel
from typing import Dict, List, Optional, Union

class GameState(BaseModel):
    game_id: str
    players: Dict[str, str]  # player_id -> player_name
    board: List[List[Optional[str]]]
    version: int = 0

class JoinGameMessage(BaseModel):
    type: str = "join_game"
    player_id: str
    player_name: str

class LeaveGameMessage(BaseModel):
    type: str = "leave_game"
    player_id: str

class RequestStateMessage(BaseModel):
    type: str = "request_state"

class PlaceTilesMessage(BaseModel):
    type: str = "place_tiles"
    player_id: str
    tiles: List[Dict]  # TODO: Define tile structure

class GameStateResponse(BaseModel):
    type: str = "game_state"
    game_state: GameState

class ErrorResponse(BaseModel):
    type: str = "error"
    message: str

MessageType = Union[JoinGameMessage, LeaveGameMessage, RequestStateMessage, PlaceTilesMessage]
ResponseType = Union[GameStateResponse, ErrorResponse]
