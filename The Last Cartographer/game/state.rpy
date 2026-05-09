default npc_state = {
    "trust": 50,
    "suspicion": 20,
    "lie_count": 0,
    "mood": "neutral",
    "known_facts": [],
    "unlocks": [],
    "player_vulnerable": False
}

default conversation_history = []
default mid_shift_played = False
default confrontation_played = False

init python:
    SPRITE_MAP = {
        "neutral":    "neutral",
        "warm":       "warm",
        "suspicious": "suspicious",
        "afraid":     "afraid",
        "cold":       "cold",
    }

    def apply_state_update(state, response):
        state["trust"] = max(0, min(100, state["trust"] + response.get("trust_delta", 0)))
        state["suspicion"] = max(0, min(100, state["suspicion"] + response.get("suspicion_delta", 0)))
        state["mood"] = response.get("mood", state["mood"])
        if response.get("lie_detected"):
            state["lie_count"] += 1
        if response.get("new_known_fact"):
            state["known_facts"].append(response["new_known_fact"])
        if response.get("unlock") and response["unlock"] not in state["unlocks"]:
            state["unlocks"].append(response["unlock"])
        if response.get("player_vulnerable"):
            state["player_vulnerable"] = True
        return state

    def check_ending(state, turn_count, leaving=False):
        t = state["trust"]
        s = state["suspicion"]
        l = state["lie_count"]
        u = state["unlocks"]

        # Forced ending: Mara ends the conversation herself after things go badly enough
        if turn_count >= 3 and (t < 20 or s > 80 or l >= 3):
            return "ending_closed"

        # All resolution endings only fire when the player chooses to leave
        if not leaving:
            return None

        # Must have had at least 2 turns — leaving immediately always gives incognita
        if turn_count < 2:
            return "ending_incognita"

        if t > 65 and s < 30 and l == 0 and "davan_story" in u and state.get("player_vulnerable"):
            return "ending_confession"
        if t > 58 and s < 30 and l == 0:
            return "ending_trusted"
        if t < 35 or s > 60:
            return "ending_closed"
        if (45 <= t <= 65) or (30 <= s <= 50) or l == 1:
            return "ending_partial"

        return "ending_incognita"
