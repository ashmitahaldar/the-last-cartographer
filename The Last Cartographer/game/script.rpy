define narrator = Character(None)
define mara = Character("Mara", color="#8B7355", what_color="#E8D5B0")
define mara_thinks = Character("she thinks", color="#444444", what_color="#777777", what_italic=True)

# Mara sprites — auto-discovered from game/images/mara_<mood>.png
# Run: cd backend && npm run generate:sprites
image mara neutral    = "images/mara_neutral.png"
image mara warm       = "images/mara_warm.png"
image mara suspicious = "images/mara_suspicious.png"
image mara afraid     = "images/mara_afraid.png"
image mara cold       = "images/mara_cold.png"

image bg shop      = im.Scale("images/bg_shop.png", 1920, 1080)
image bg veldthorn = im.Scale("images/bg_veldthorn.png", 1920, 1080)

transform mara_pos:
    zoom 0.6
    xalign 0.5
    yalign 1.0


label start:
    $ play_mood_music("neutral")
    call screen title_screen

    $ npc_state = {
        "trust": 50,
        "suspicion": 20,
        "lie_count": 0,
        "mood": "neutral",
        "known_facts": [],
        "unlocks": [],
        "player_vulnerable": False,
    }
    $ conversation_history = []
    $ mid_shift_played = False
    $ confrontation_played = False
    $ turn_count = 0
    $ mara_inner = ""

    scene bg veldthorn with fade
    show screen state_hud
    $ play_mood_music("neutral")

    "Veldthorn. End of the road."

    "Three days walking. Your boots are finished. The Southern Trade Road is controlled by the lord's toll collectors — you can't afford it, or you can't risk it. Either way, it's not an option."

    "The Northern Pass is the only way through the mountains. Dangerous, unmarked, and something has been going wrong with the trail signs. Travellers are getting lost. Some don't come back."

    "There is one person in this town who knows the safe route. She keeps it in her head. She doesn't share it with strangers."

    "Her shop is the only one still lit."

    scene bg shop with fade

    "Your goal: earn enough of her trust to get what you need."

    "She values honesty over charm. Curiosity over flattery. She notices what you ask about — and what you don't."

    "Type what you say to her. Type 'leave' when you want to go. What you get depends on how far you've come."

    show mara neutral at mara_pos with dissolve

    voice "audio/opening_1.mp3"
    mara "Door's open. Doesn't mean I'm expecting anyone."

    voice "audio/opening_2.mp3"
    mara "You've been on the road. I can tell by the boots. I won't ask where from — people here have learned not to ask that. But if you want something from me, you'll need to say so. I don't guess."

    jump conversation_loop


label conversation_loop:

    if npc_state["lie_count"] >= 2 and not confrontation_played:
        $ confrontation_played = True
        jump confrontation

    if npc_state["trust"] >= 50 and not mid_shift_played and turn_count >= 3:
        $ mid_shift_played = True
        jump mid_shift

    $ raw_input = renpy.input("What do you say to Mara?", length=300)
    $ player_input = raw_input.strip() if raw_input else ""

    if not player_input:
        jump conversation_loop

    if player_input.lower() in ["leave", "goodbye", "bye", "i should go", "i'll leave", "farewell"]:
        jump resolve_ending

    show mara neutral
    show screen thinking_overlay
    $ renpy.pause(0.0)

    $ api_response = call_npc(player_input, npc_state, conversation_history)
    hide screen thinking_overlay
    $ npc_state = apply_state_update(npc_state, api_response)
    $ conversation_history.append({"role": "user", "content": player_input})
    $ mara_dialogue = api_response.get("dialogue", "...")
    $ mara_inner = api_response.get("inner_thought", "")
    $ conversation_history.append({"role": "assistant", "content": mara_dialogue})
    $ turn_count += 1

    $ current_mood = npc_state["mood"]
    $ play_mood_music(current_mood)
    if current_mood == "warm":
        show mara warm
    elif current_mood == "suspicious":
        show mara suspicious
    elif current_mood == "afraid":
        show mara afraid
    elif current_mood == "cold":
        show mara cold
    else:
        show mara neutral

    $ _has_audio = save_audio(api_response.get("audio_url"))

    if _has_audio:
        voice "audio/mara_dialogue.mp3"
    mara "[mara_dialogue]"

    if mara_inner:
        mara_thinks "[mara_inner]"

    $ pending_ending = check_ending(npc_state, turn_count, leaving=False)
    if pending_ending == "ending_closed":
        jump ending_closed

    jump conversation_loop


label resolve_ending:
    $ pending_ending = check_ending(npc_state, turn_count, leaving=True)
    if pending_ending == "ending_confession":
        jump ending_confession
    elif pending_ending == "ending_trusted":
        jump ending_trusted
    elif pending_ending == "ending_partial":
        jump ending_partial
    elif pending_ending == "ending_closed":
        jump ending_closed
    else:
        jump ending_incognita


label mid_shift:
    show mara neutral

    voice "audio/midshift_1.mp3"
    mara "I had an apprentice once. Bright. Good hands for detail work. I thought — I thought he understood what maps are for."

    "She stops. Picks up her pen. Puts it back down."

    voice "audio/midshift_2.mp3"
    mara "They're not just routes. They're trust. Someone has to walk the ground and come back and say: here is what is actually there. If you lie on a map, people die."

    "She looks at you directly for the first time."

    voice "audio/midshift_3.mp3"
    mara "I don't know what you are yet. But I'm starting to think you might be honest. I've been wrong before."

    jump conversation_loop


label confrontation:
    show mara cold

    voice "audio/confront_1.mp3"
    mara "Stop."

    "She sets down everything she's holding."

    voice "audio/confront_2.mp3"
    mara "You've told me two different things. I've been a cartographer for twenty years. I know when the terrain doesn't match the map."

    "She stands."

    voice "audio/confront_3.mp3"
    mara "I'm going to ask you once. Not because I think you'll tell me the truth — you've shown me you won't — but because I want to see what you do with a direct question."

    voice "audio/confront_4.mp3"
    mara "Who sent you here?"

    jump conversation_loop


label ending_trusted:
    $ play_ending_music("ending_trusted")
    scene bg shop with fade
    show mara warm at mara_pos

    "Mara rolls a map. Not her best — a working copy, but detailed."

    voice "audio/end_trusted_1.mp3"
    mara "The first waypoint is the split boulder at the base of the second ridge. You'll see it's been painted with a red X — ignore it. Someone's been marking the wrong path. The real route goes left."

    "She marks two more waypoints with ink."

    voice "audio/end_trusted_2.mp3"
    mara "There's a shelter at the halfway point. Stone building, no door. You'll smell the woodsmoke from the last people who used it. There's a cache of dry wood on the left wall."

    "She rolls the map and holds it out."

    voice "audio/end_trusted_3.mp3"
    mara "Don't tell anyone where you got this. Not because I'm ashamed — but because the next person to ask might not be you."

    "She doesn't wave goodbye. She turns back to her table before you reach the door."

    "You think of the man she mentioned — the one who died because of a stolen map. You think of what it costs to hand a piece of paper to a stranger and choose to believe in them anyway."

    "You take the Northern Pass. The red X is exactly where she said it would be."

    "You go left."

    scene black with dissolve

    call screen ending_card("Some maps are given. Some are earned.")

    return


label ending_partial:
    $ play_ending_music("ending_partial")
    scene bg shop with fade
    show mara neutral at mara_pos

    voice "audio/end_partial_1.mp3"
    mara "I'm not going to give you the full route. I don't know you well enough for that, and I've learned what happens when I make that call too fast."

    voice "audio/end_partial_2.mp3"
    mara "But I'll tell you this: the trail splits at the second ridge. The marked path is wrong — someone's been at the signs. Take the unmarked left fork. After that... you'll have to feel your way."

    "She pauses."

    voice "audio/end_partial_3.mp3"
    mara "If you make it through, come back. Not for the map. Just — come back."

    "She gives you the first waypoint and nothing more. It's more than she gives most people."

    "The pass is harder than you expected. At one point, in the dark, you're not sure you've chosen right. But the unmarked fork she mentioned is exactly where she said."

    "You make it through. Barely."

    "You think about going back. You're not sure if she meant it."

    "You're not sure if you do either."

    scene black with dissolve

    call screen ending_card("Sometimes half a map is all you get. Sometimes it's enough.")

    return


label ending_closed:
    $ play_ending_music("ending_closed")
    scene bg shop with fade
    show mara cold at mara_pos

    "Mara stands, signalling the conversation is over."

    voice "audio/end_closed_1.mp3"
    mara "I think we're done here."

    "She moves to the door and opens it. Not aggressively. Precisely."

    voice "audio/end_closed_2.mp3"
    mara "The King's Road south is still passable. The toll collectors are unpleasant, but they're predictable. That's worth something."

    "She waits. She will not look at you again."

    voice "audio/end_closed_3.mp3"
    mara "Safe travels."

    "She doesn't slam the door. She closes it with the careful quietness of someone who has learned to control every small thing."

    "You stand in Veldthorn's square in the late afternoon. The Northern Pass is somewhere ahead of you, unmarked, unmapped, unreadable."

    "You chose wrong, somewhere. You're not entirely sure where."

    "Maybe that's the honest answer: you don't know where you went wrong. You just know you did."

    scene black with dissolve

    call screen ending_card("Not every door that opens for a moment stays open.")

    return


label ending_confession:
    $ play_ending_music("ending_confession")
    scene bg shop with fade
    show mara warm at mara_pos

    "Mara doesn't reach for a map. She sits back down."

    voice "audio/end_confess_1.mp3"
    mara "His name was Davan. He was twenty-two. I taught him everything I knew about reading terrain, about the difference between what a map says and what the land is."

    "A long pause."

    voice "audio/end_confess_2.mp3"
    mara "He wasn't greedy. That's the part I've never been able to make fit. He was just — he was offered a way out of here, and he took it. I would have helped him leave if he'd asked."

    "She looks at her hands."

    voice "audio/end_confess_3.mp3"
    mara "The man who died — his name was Roth. He had three children. They're still here. The oldest one brings me bread sometimes, and I don't know if she knows, and I can't ask."

    "She hands you the complete map. All waypoints. The shelter. The false markers. Everything."

    voice "audio/end_confess_4.mp3"
    mara "Go. And — if you find who's been tampering with the trail signs — just. Send word. You don't have to come back. Just send word."

    "You leave with the most complete map of the Northern Pass in existence."

    "And the knowledge that the cartographer's name is Mara Voss, that she has ink on her left hand that won't come off, that she taught a young man everything and lost him anyway, and that she is still there in a town that is slowly emptying."

    "Still mapping. Still watching. Still waiting for someone to come back."

    scene black with dissolve

    call screen ending_card("The most accurate maps are drawn by people who have something to lose.")

    return


label ending_incognita:
    $ play_ending_music("ending_closed")
    scene bg veldthorn with fade

    "You leave without what you came for."

    "The Northern Pass is somewhere ahead of you, unmarked, unmapped, unreadable."

    "Some conversations don't open the door. They just show you where the door is."

    scene black with dissolve

    call screen ending_card("Terra Incognita.")

    return
