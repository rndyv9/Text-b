from typing import Dict, List, Optional
from pydantic import BaseModel, Field

StatBlock = Dict[str, float]  # e.g. {"hp": 40, "atk": 8, "def": 3, "crit": 0.1}

class Trait(BaseModel):
    key: str
    name: str
    # flat and percent modifiers keyed by stat names; easy to extend with new stats
    flat: Dict[str, float] = Field(default_factory=dict)     # e.g. {"hp": +10}
    percent: Dict[str, float] = Field(default_factory=dict)  # e.g. {"atk": +0.2}

class Character(BaseModel):
    id: str
    name: str
    base_stats: StatBlock
    traits: List[Trait] = Field(default_factory=list)

    def total_stats(self) -> StatBlock:
        # combine base + traits without caring what stats exist
        stats = dict(self.base_stats)
        # apply flat
        for t in self.traits:
            for k, v in t.flat.items():
                stats[k] = stats.get(k, 0.0) + v
        # apply percent
        for t in self.traits:
            for k, v in t.percent.items():
                stats[k] = stats.get(k, 0.0) * (1 + v)
        # ensure minimum keys exist
        for k in ["hp", "atk", "def"]:
            stats.setdefault(k, 0.0)
        return stats

class TurnLog(BaseModel):
    attacker: str
    defender: str
    dmg: float
    crit: bool = False
    defender_hp_after: float

class BattleState(BaseModel):
    battle_id: str
    player: Character
    enemy: Character
    player_stats: StatBlock
    enemy_stats: StatBlock
    player_hp: float
    enemy_hp: float
    turn: int = 1
    log: List[TurnLog] = Field(default_factory=list)
    finished: bool = False
    winner: Optional[str] = None
