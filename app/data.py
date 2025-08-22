from .models import Trait, Character
import uuid

# Simple traits; add more any time by listing new stat keys.
ALL_TRAITS = {
    "iron_skin": Trait(key="iron_skin", name="Iron Skin", flat={"def": 2}),
    "glass_cannon": Trait(key="glass_cannon", name="Glass Cannon", percent={"atk": 0.35}, flat={"hp": -5}),
    "lucky": Trait(key="lucky", name="Lucky", flat={"crit": 0.15}, percent={}),
    "steady": Trait(key="steady", name="Steady", flat={"variance": -0.05}),  # reduces damage swing
}

def make_player(name: str, trait_keys):
    traits = [ALL_TRAITS[k] for k in trait_keys if k in ALL_TRAITS]
    return Character(
        id=str(uuid.uuid4()),
        name=name or "Player",
        base_stats={"hp": 40, "atk": 8, "def": 3, "crit": 0.05, "crit_mult": 1.5, "variance": 0.1},
        traits=traits
    )

SEED_ENEMIES = [
    Character(
        id=str(uuid.uuid4()),
        name="Slime",
        base_stats={"hp": 25, "atk": 5, "def": 1, "crit": 0.0, "variance": 0.05},
        traits=[]
    ),
    Character(
        id=str(uuid.uuid4()),
        name="Bandit",
        base_stats={"hp": 35, "atk": 7, "def": 2, "crit": 0.1, "crit_mult": 1.6, "variance": 0.12},
        traits=[]
    ),
    Character(
        id=str(uuid.uuid4()),
        name="Knight",
        base_stats={"hp": 45, "atk": 8, "def": 4, "crit": 0.05, "variance": 0.08},
        traits=[]
    ),
]
