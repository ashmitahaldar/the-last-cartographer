init python:
    import requests
    import json
    import os
    import base64

    BACKEND_URL = os.environ.get("BACKEND_URL", "https://the-last-cartographer.vercel.app")

    def call_npc(player_input, npc_state, history):
        try:
            res = requests.post(
                BACKEND_URL + "/api/chat",
                json={
                    "input": player_input,
                    "npc_state": npc_state,
                    "history": history,
                },
                timeout=20,
            )
            data = res.json()
            renpy.log("API OK: status=%d dialogue=%s" % (res.status_code, data.get("dialogue", "?")))
            return data
        except Exception as e:
            renpy.log("API ERROR: %s — backend=%s" % (str(e), BACKEND_URL))
            return {
                "dialogue": "...",
                "trust_delta": 0,
                "suspicion_delta": 0,
                "mood": npc_state["mood"],
                "unlock": None,
                "inner_thought": "",
                "lie_detected": False,
                "new_known_fact": None,
                "player_vulnerable": False,
                "audio_url": None,
            }

    def play_mood_music(mood):
        """Play looping mood music with crossfade. Silently skips if file missing."""
        try:
            music_path = os.path.join(renpy.config.gamedir, "audio", "music", mood + ".mp3")
            if not os.path.exists(music_path):
                renpy.log("MUSIC: no file for mood %s, skipping" % mood)
                return
            renpy.music.play("audio/music/" + mood + ".mp3", loop=True, fadeout=1.5, fadein=1.5)
            renpy.log("MUSIC: playing %s.mp3" % mood)
        except Exception as e:
            renpy.log("MUSIC ERROR: %s" % str(e))

    def play_ending_music(track):
        """Stop mood music and play a one-shot ending track."""
        try:
            music_path = os.path.join(renpy.config.gamedir, "audio", "music", track + ".mp3")
            if not os.path.exists(music_path):
                renpy.log("MUSIC: no ending track %s, skipping" % track)
                renpy.music.stop(fadeout=2.0)
                return
            renpy.music.stop(fadeout=2.0)
            renpy.music.play("audio/music/" + track + ".mp3", loop=False)
            renpy.log("MUSIC: playing ending %s.mp3" % track)
        except Exception as e:
            renpy.log("MUSIC ERROR: %s" % str(e))

    def save_audio(audio_data_url):
        """Save audio to disk. Returns True if a file was written, False otherwise.
        Caller uses `voice "audio/mara_dialogue.mp3"` to play it via Ren'Py's voice system."""
        if not audio_data_url:
            return False
        try:
            if audio_data_url.startswith("data:audio/mpeg;base64,"):
                b64_data = audio_data_url.split(",", 1)[1]
                audio_bytes = base64.b64decode(b64_data)
                audio_path = os.path.join(renpy.config.gamedir, "audio", "mara_dialogue.mp3")
                with open(audio_path, "wb") as f:
                    f.write(audio_bytes)
                renpy.log("AUDIO: saved mara_dialogue.mp3 (%d bytes)" % len(audio_bytes))
                return True
        except Exception as e:
            renpy.log("AUDIO ERROR: %s" % str(e))
        return False
