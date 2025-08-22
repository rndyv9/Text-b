import random
from .models import BattleState, TurnLog

def compute_damage(attacker_stats, defender_stats, rng: random.Random):
    atk = attacker_stats.get("atk", 0.0)
    df = defender_stats.get("def", 0.0)
    crit_chance = attacker_stats.get("crit", 0.0)  # e.g. 0.1 = 10%
    variance = attacker_stats.get("variance", 0.1)  # ±10% default if present

    base = max(1.0, atk - df * 0.6)
    # small random variance
    spread = base * (rng.uniform(-variance, variance))
    dmg = max(1.0, base + spread)

    is_crit = rng.random() < crit_chance
    if is_crit:
        crit_mult = attacker_stats.get("crit_mult", 1.5)
        dmg *= crit_mult

    return round(dmg, 2), is_crit

def do_turn(state: BattleState, actor: str, rng: random.Random) -> BattleState:
    if state.finished:
        return state

    if actor == "player":
        atk_stats, def_stats = state.player_stats, state.enemy_stats
        def_name = state.enemy.name
    else:
        atk_stats, def_stats = state.enemy_stats, state.player_stats
        def_name = state.player.name

    dmg, crit = compute_damage(atk_stats, def_stats, rng)

    if actor == "player":
        state.enemy_hp = max(0.0, state.enemy_hp - dmg)
        hp_after = state.enemy_hp
        target_name = state.enemy.name
    else:
        state.player_hp = max(0.0, state.player_hp - dmg)
        hp_after = state.player_hp
        target_name = state.player.name

    state.log.append(TurnLog(
        attacker=actor,
        defender=target_name,
        dmg=dmg,
        crit=crit,
        defender_hp_after=hp_after
    ))
    # check end
    if state.enemy_hp <= 0 or state.player_hp <= 0:
        state.finished = True
        state.winner = "player" if state.enemy_hp <= 0 and state.player_hp > 0 else \                       "enemy" if state.player_hp <= 0 and state.enemy_hp > 0 else "draw"
    state.turn += 1
    return state
