from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import random, uuid

from .models import BattleState
from .data import make_player, SEED_ENEMIES, ALL_TRAITS
from .battle import do_turn

app = FastAPI(title="Text Battle")
BASE = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")

# simple in-memory "db"
BATTLES = {}

def pick_enemy():
    rng = random.Random()
    return rng.choice(SEED_ENEMIES)

@app.get("/", response_class=HTMLResponse)
def index():
    html = (BASE / "templates" / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(html)

@app.get("/traits")
def traits():
    return [{"key": t.key, "name": t.name} for t in ALL_TRAITS.values()]

@app.post("/start")
async def start(request: Request):
    data = await request.json()
    name = data.get("name", "Player")
    trait_keys = data.get("traits", [])

    player = make_player(name, trait_keys)
    enemy = pick_enemy()

    ps = player.total_stats()
    es = enemy.total_stats()

    battle = BattleState(
        battle_id=str(uuid.uuid4()),
        player=player,
        enemy=enemy,
        player_stats=ps,
        enemy_stats=es,
        player_hp=ps.get("hp", 1.0),
        enemy_hp=es.get("hp", 1.0),
    )
    BATTLES[battle.battle_id] = battle
    return battle.model_dump()

@app.post("/turn/{battle_id}")
def turn(battle_id: str):
    battle = BATTLES.get(battle_id)
    if not battle or battle.finished:
        return JSONResponse({"error": "No active battle"}, status_code=400)

    rng = random.Random()
    # player attacks first, then enemy if still alive
    do_turn(battle, "player", rng)
    if not battle.finished:
        do_turn(battle, "enemy", rng)
    return battle.model_dump()

@app.post("/reset/{battle_id}")
def reset(battle_id: str):
    if battle_id in BATTLES:
        del BATTLES[battle_id]
    return {"ok": True}
