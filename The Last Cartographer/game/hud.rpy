init python:
    def trust_color(v):
        if v > 65: return "#55cc66"
        if v > 40: return "#cccc44"
        return "#cc4444"

    def suspicion_color(v):
        if v > 60: return "#cc4444"
        if v > 35: return "#cccc44"
        return "#55cc66"

    MOOD_COLORS = {
        "warm":       "#ddaa44",
        "neutral":    "#aaaaaa",
        "suspicious": "#cccc33",
        "afraid":     "#7799cc",
        "cold":       "#44bbcc",
    }

    def mood_color(m):
        return MOOD_COLORS.get(m, "#aaaaaa")


screen state_hud():
    frame:
        xpos 30
        ypos 30
        background "#000000cc"
        padding (22, 18)
        vbox:
            spacing 8
            text "— NPC STATE —" size 16 color "#444444"
            null height 4
            hbox:
                spacing 0
                text "Trust      " size 22 color "#888888"
                text "[npc_state['trust']]" size 22 color trust_color(npc_state["trust"]) bold True
            hbox:
                spacing 0
                text "Suspicion  " size 22 color "#888888"
                text "[npc_state['suspicion']]" size 22 color suspicion_color(npc_state["suspicion"]) bold True
            hbox:
                spacing 0
                text "Mood       " size 22 color "#888888"
                text "[npc_state['mood']]" size 22 color mood_color(npc_state["mood"]) bold True
            if npc_state["lie_count"] > 0:
                null height 4
                text "Lies caught: [npc_state['lie_count']]" size 19 color "#cc4444"
