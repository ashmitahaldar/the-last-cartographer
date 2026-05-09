# CLAUDE.md — The Last Cartographer

### AI NPC Visual Novel | Hackathon Project

---

## Current Build Phase

**Phase 0 — Pre-Hackathon Setup**

- [ ] Ren'Py project initialized ✓
- [ ] Backend folder scaffolded
- [ ] API keys in `.env.local`
- [ ] Vercel project created and connected
- [ ] Mara reference art generated for Fal
- [ ] Story bible written ✓ (see `mara_story_bible.md`)

> **Update this section as phases complete.** Coding agents should read this first to know where work left off.

Phase 1 — Hour 0–1 | Skeleton
Goal: Ren'Py game runs, backend responds with dummy data

Scaffold Next.js backend with npx create-next-app
Create /api/chat route that returns hardcoded JSON
Build Ren'Py skeleton: title screen → town scene → input box → display response
Confirm Ren'Py requests.post() reaches Vercel endpoint
Deploy backend to Vercel

Coding agent prompt:

"Create a Next.js 14 App Router API route at /api/chat that accepts POST with {input, npc_state, history} and returns a hardcoded JSON object matching this schema: [paste schema]. Include CORS headers."

Phase 2 — Hour 1–2 | Live Gemini Integration
Goal: Real NPC responses printing to screen

Wire Gemini 1.5 Pro into /api/chat using Google AI SDK
Pass system prompt with state interpolated
Parse and validate JSON response (add fallback if malformed)
Print Mara's dialogue to Ren'Py screen

Coding agent prompt:

"Integrate Google Gemini 1.5 Pro into this Next.js route using @google/generative-ai. The system prompt is [paste prompt]. Interpolate trust, suspicion, mood, known_facts from the request body. Return the parsed JSON response. Add a try/catch that returns a fallback neutral response if JSON parsing fails."

Phase 3 — Hour 2–3.5 | State Tracking
Goal: Trust/suspicion/mood update correctly across turns

Implement state update logic in Ren'Py after each response
Pass full conversation history on each call
Sprite swaps working based on mood tag
Unlock flag detection: if unlock == "north_pass" → set a Ren'Py variable

Coding agent prompt:

"In this Ren'Py script.rpy, after receiving the API response dict, update the npc_state dict by adding trust_delta and suspicion_delta (clamped 0–100), set mood to the returned mood, and append any new known_facts. Then swap the displayed Mara sprite using this SPRITE_MAP: [paste map]."

Phase 4 — Hour 3.5–5 | Voice + Endings
Goal: Mara speaks. 3 endings exist and trigger correctly.

Wire /api/tts to ElevenLabs, return audio URL
Call TTS in parallel inside /api/chat response, return audio_url alongside JSON
Ren'Py downloads and plays audio file per turn
Write 3 ending scenes in Ren'Py script (trust won, neutral, betrayed)
Trigger correct ending based on npc_state values at conversation close

Coding agent prompt:

"In this Next.js /api/chat route, after getting the dialogue string from Gemini, make a parallel fetch to ElevenLabs /v1/text-to-speech/{voice_id} with these settings: [paste mood→stability map]. Upload the returned audio buffer to a temp URL or return it as base64. Include audio_url in the final JSON response."

Phase 5 — Hour 5–6 | Story Polish
Goal: Demo feels like a game, not a tech demo

Polish Mara's system prompt — give her secrets, opinions, specific memories
Write opening narration and scene descriptions
Pre-generate all 5 Fal sprites, clean them up
Add mara_thinking idle animation during API wait
Add background music (find royalty-free tracks, 2–3 moods)

Phase 6 — Hour 6–7 | Playtest & Fix
Goal: A stranger can play it without breaking it

Play through 3 times trying to break the AI (nonsense input, very short answers, aggressive tone)
Add input length cap + sanitisation in backend
Tune system prompt based on any weird outputs
Confirm all 3 endings are reachable
Prepare 90-second demo script for judges

---

## Project Overview

A visual novel where the single NPC (Mara) is powered by a live LLM. She tracks trust, suspicion, and lies across the conversation. What she tells you — and what ending you get — is determined by the AI in real time, not a dialogue tree.

**The core demo point:** The AI acts as a game director, not a chatbot. NPC state feeds into world outcomes.

---

## Repository Structure

```
cartographer/
├── CLAUDE.md                        ← you are here
├── mara_story_bible.md              ← full story, system prompt, endings
├── The Last Cartographer/           ← Ren'Py project
│   └── game/
│       ├── script.rpy               ← main VN script, scene labels, ending logic
│       ├── api.rpy                  ← Python block: HTTP calls to backend
│       ├── state.rpy                ← npc_state dict, helper functions
│       ├── images/                  ← Mara sprites (mara_neutral/warm/suspicious/afraid/cold.png)
│       └── audio/                   ← ElevenLabs dialogue cache (runtime) + Lyria tracks (pre-generated)
└── backend/                         ← Next.js API (deploy to Vercel)
    ├── app/api/
    │   ├── chat/route.ts            ← main NPC endpoint
    │   ├── tts/route.ts             ← ElevenLabs proxy
    │   ├── sprites/route.ts         ← Fal sprite generation
    │   └── music/route.ts           ← Lyria music generation
    └── lib/
        ├── gemini.ts                ← Gemini streaming client
        ├── elevenlabs.ts            ← ElevenLabs client
        ├── fal.ts                   ← Fal image client
        ├── lyria.ts                 ← Lyria music generation client
        └── prompts.ts               ← Mara system prompt + JSON schema
```

---

## Tech Stack

| Layer           | Technology                        | Notes                                         |
| --------------- | --------------------------------- | --------------------------------------------- |
| Game client     | Ren'Py 8 (Python 3)               | Visual novel rendering, input, audio          |
| Backend         | Next.js 14 App Router, TypeScript | Deployed to Vercel                            |
| LLM             | Gemini 1.5 Pro                    | Via `@google/generative-ai` SDK               |
| TTS             | ElevenLabs                        | Emotion-aware voice, cached per turn          |
| Sprites         | Fal                               | Pre-generated at session start, 5 moods       |
| Music           | Lyria 3 (Gemini API)              | Pre-generated tracks per mood + ending scenes |
| Dev environment | Daytona                           | Cloud workspace                               |

---

## Environment Variables

All secrets live in `backend/.env.local`. Never commit this file.

```
GEMINI_API_KEY=
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=
FAL_API_KEY=
NEXT_PUBLIC_BACKEND_URL=https://your-app.vercel.app
```

For local dev, Ren'Py should point to `http://localhost:3000`. For production, update `BACKEND_URL` in `game-client/game/api.rpy`.

---

## NPC State Object

This is the single source of truth for Mara's state. Lives in Ren'Py, sent to backend on every turn.

```python
# game-client/game/state.rpy
default npc_state = {
    "trust": 50,           # 0–100. Drives mood and unlocks.
    "suspicion": 20,       # 0–100. High suspicion overrides trust.
    "lie_count": 0,        # Incremented when AI detects contradiction.
    "mood": "neutral",     # neutral | warm | suspicious | afraid | cold
    "known_facts": [],     # Strings: things player has revealed about themselves.
    "unlocks": [],         # Granted unlock keys e.g. ["north_waypoints", "davan_story"]
    "player_vulnerable": False  # True if player expressed personal fear/failure
}
```

**Mood → Sprite mapping:**

```python
SPRITE_MAP = {
    "neutral":    "mara_neutral",
    "warm":       "mara_warm",
    "suspicious": "mara_suspicious",
    "afraid":     "mara_afraid",
    "cold":       "mara_cold"
}
```

**Ending trigger thresholds:**

```python
# Secret ending (check first)
trust > 60 AND "davan_story" in unlocks AND player_vulnerable == True

# Ending 1 — The Trusted Stranger
trust > 65 AND suspicion < 30 AND lie_count == 0

# Ending 2 — The Partial Crossing
(45 <= trust <= 65) OR (30 <= suspicion <= 50) OR lie_count == 1

# Ending 3 — The Closed Door
trust < 35 OR suspicion > 60

# Ending 4 — Terra Incognita (fallback)
player exits without triggering other endings
```

---

## API Contracts

### `POST /api/chat`

**Request:**

```typescript
{
  input: string,           // player's typed message
  npc_state: NpcState,     // full state object (see above)
  history: Message[]       // full conversation history
}

type Message = { role: "user" | "assistant", content: string }
```

**Response (Gemini returns this as JSON, validated server-side):**

```typescript
{
  dialogue: string,          // Mara's spoken response, 2–4 sentences
  trust_delta: number,       // -20 to +20
  suspicion_delta: number,   // -10 to +20
  mood: Mood,                // neutral | warm | suspicious | afraid | cold
  unlock: string | null,     // one unlock key or null
  inner_thought: string,     // private thought, NOT shown to player (yet)
  lie_detected: boolean,     // true if player contradicted earlier statement
  new_known_fact: string | null,   // new fact about player, or null
  player_vulnerable: boolean // true if player expressed personal vulnerability
  audio_url: string | null   // ElevenLabs audio URL, added by backend before returning
}
```

**Important:** The backend fires the ElevenLabs TTS call in parallel once dialogue string is ready, then includes `audio_url` in the final response. Do not make Ren'Py call TTS separately.

---

### `POST /api/tts`

**Request:**

```typescript
{
  text: string,
  mood: Mood
}
```

**Response:**

```typescript
{
  audio_url: string;
}
```

ElevenLabs stability/style settings by mood:

```typescript
const VOICE_SETTINGS = {
  neutral: { stability: 0.5, similarity_boost: 0.75, style: 0.0 },
  warm: { stability: 0.4, similarity_boost: 0.75, style: 0.3 },
  suspicious: { stability: 0.7, similarity_boost: 0.8, style: 0.1 },
  afraid: { stability: 0.6, similarity_boost: 0.7, style: 0.2 },
  cold: { stability: 0.9, similarity_boost: 0.85, style: 0.0 },
};
```

---

### `POST /api/sprites`

**Request:**

```typescript
{
  mood: Mood;
}
```

**Response:**

```typescript
{
  image_url: string;
}
```

Called once per mood at session start via `preload_sprites()`. Not called per turn. Ren'Py downloads images to `game-client/game/images/` and references them as standard Ren'Py image assets.

---

### `POST /api/music`

**Request:**

```typescript
{
  track: MusicTrack; // see track list below
}

type MusicTrack =
  | "neutral"
  | "warm"
  | "suspicious"
  | "afraid"
  | "cold" // mood loops
  | "ending_trusted"
  | "ending_partial"
  | "ending_closed" // ending stings
  | "ending_confession"; // secret ending
```

**Response:**

```typescript
{
  audio_path: string;
} // local filename saved to game-client/game/audio/music/
```

**Important:** `/api/music` is called **only at session start** to pre-generate all tracks. Never called during conversation. Ren'Py plays tracks as looping background music, swapping when mood changes.

**Lyria model selection:**

```typescript
// Mood loops → lyria-3-clip-preview (30s, loops cleanly)
// Ending scenes → lyria-3-pro-preview (full song, plays once)
const LONG_TRACKS = ["ending_trusted", "ending_confession"];
const model = LONG_TRACKS.includes(track)
  ? "lyria-3-pro-preview"
  : "lyria-3-clip-preview";
```

**Track prompts (in `backend/lib/lyria.ts`):**

```typescript
export const MUSIC_PROMPTS: Record<MusicTrack, string> = {
  neutral:
    "Sparse melancholic folk instrumental. Solo acoustic guitar, minor key, slow tempo. A traveller arriving somewhere forgotten. No drums. No resolution.",
  warm: "Gentle folk instrumental, acoustic guitar and soft strings, warm and tentative. A cautious sense of hope beginning to form.",
  suspicious:
    "Tense minimal dark folk. Slow plucked strings, long silences, unsettling undertone. Repeating motif that never resolves.",
  afraid:
    "Sparse ambient folk, barely-there piano, distant wind texture. Something wrong just beneath the surface. Very quiet.",
  cold: "Bare cold instrumental. Single repeated piano note, long reverb, hollow silence between notes. A door closing forever.",
  ending_trusted:
    "Quiet triumphant folk piece, no vocals. Begins with solo guitar, builds slowly with strings. Bittersweet resolution — a journey beginning, tinged with loss.",
  ending_partial:
    "Unresolved folk instrumental. Guitar that starts to build then holds back. Hopeful but uncertain. The feeling of enough but not everything.",
  ending_closed:
    "Minimal dark folk. A single guitar phrase repeated and fading. No resolution. The feeling of a wrong turn only understood too late.",
  ending_confession:
    "Deeply emotional folk piece, no vocals. Piano and cello, intimate and fragile. Two people who finally understood each other, too briefly.",
};
```

**`backend/lib/lyria.ts` implementation:**

```typescript
export async function generateTrack(track: MusicTrack): Promise<Buffer> {
  const isLong = ["ending_trusted", "ending_confession"].includes(track);
  const model = isLong ? "lyria-3-pro-preview" : "lyria-3-clip-preview";
  const prompt = MUSIC_PROMPTS[track];

  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-goog-api-key": process.env.GEMINI_API_KEY!,
      },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
      }),
    },
  );

  const data = await res.json();
  const audioPart = data.candidates[0].content.parts.find(
    (p: any) => p.inlineData,
  );
  if (!audioPart) throw new Error(`No audio returned for track: ${track}`);
  return Buffer.from(audioPart.inlineData.data, "base64");
}
```

**Ren'Py music playback (in `script.rpy`):**

```python
# Play mood music — call this whenever mood changes
# Ren'Py's play music loops by default
$ renpy.music.play("audio/music/neutral.mp3", loop=True, fadeout=1.5, fadein=1.5)

# Stop with fade for ending scenes
$ renpy.music.stop(fadeout=2.0)
play music "audio/music/ending_trusted.mp3"
```

**Pre-generation strategy:**

- Generate all 8 tracks at session start via `/api/music` for each track key
- Save to `game-client/game/audio/music/<track>.mp3`
- **Recommended:** generate tracks before the hackathon, commit the mp3 files to the repo as static assets. Lyria results vary per call — lock in good outputs early.
- Live generation at session start is the fallback if static files are missing

---

## Ren'Py ↔ Backend Communication

Ren'Py uses Python `requests` library inside `init python` blocks. All calls are synchronous (blocking). Show a thinking animation before calling.

```python
# game-client/game/api.rpy
init python:
    import requests, json, os

    BACKEND_URL = "http://localhost:3000"  # change to Vercel URL for production

    def call_npc(player_input, npc_state, history):
        try:
            res = requests.post(
                f"{BACKEND_URL}/api/chat",
                json={"input": player_input, "npc_state": npc_state, "history": history},
                timeout=15
            )
            return res.json()
        except Exception as e:
            # Fallback response if API fails
            return {
                "dialogue": "...",
                "trust_delta": 0, "suspicion_delta": 0,
                "mood": npc_state["mood"],
                "unlock": None, "inner_thought": "",
                "lie_detected": False, "new_known_fact": None,
                "player_vulnerable": False, "audio_url": None
            }

    def apply_state_update(npc_state, response):
        npc_state["trust"] = max(0, min(100, npc_state["trust"] + response["trust_delta"]))
        npc_state["suspicion"] = max(0, min(100, npc_state["suspicion"] + response["suspicion_delta"]))
        npc_state["mood"] = response["mood"]
        if response["lie_detected"]:
            npc_state["lie_count"] += 1
        if response["new_known_fact"]:
            npc_state["known_facts"].append(response["new_known_fact"])
        if response["unlock"] and response["unlock"] not in npc_state["unlocks"]:
            npc_state["unlocks"].append(response["unlock"])
        if response["player_vulnerable"]:
            npc_state["player_vulnerable"] = True
        return npc_state
```

---

## Latency Handling

1. **Sprites** — pre-generated at session start. Never generated per turn.
2. **Music** — pre-generated at session start (or committed as static mp3s before hackathon). Swapped via Ren'Py `play music` with crossfade when mood changes. Never generated per turn.
3. **TTS** — fired in parallel inside `/api/chat` once dialogue is ready. `audio_url` returned in same response.
4. **Thinking animation** — show `mara_thinking` idle sprite while `call_npc()` blocks. Swap on response.
5. **Fallback** — if API call fails or times out (15s), use fallback response (see above). Never crash.
6. **Audio** — if `audio_url` is null, display dialogue text only. Do not block on audio.

---

## Ren'Py Scene Labels

```
label start              → title screen → opening scene → conversation_loop
label conversation_loop  → main AI input/response loop
label mid_shift          → Mara's backstory hint (fires once, trust >= 50, lie_count == 0)
label confrontation      → Mara calls out lies (fires at lie_count >= 2)
label ending_confession  → Secret ending (trust > 60, davan_story unlocked, player_vulnerable)
label ending_trusted     → Ending 1: The Trusted Stranger
label ending_partial     → Ending 2: The Partial Crossing
label ending_closed      → Ending 3: The Closed Door
label ending_incognita   → Ending 4: Terra Incognita (fallback)
```

---

## System Prompt Location

Full system prompt with all state variable interpolation: `mara_story_bible.md` → section "System Prompt (for `/lib/prompts.ts`)"

Copy this into `backend/lib/prompts.ts` as a template literal. Interpolate at request time:

```typescript
export function buildSystemPrompt(state: NpcState): string {
  return MARA_SYSTEM_PROMPT.replace("{trust}", String(state.trust))
    .replace("{suspicion}", String(state.suspicion))
    .replace("{lie_count}", String(state.lie_count))
    .replace("{mood}", state.mood)
    .replace("{known_facts}", state.known_facts.join(", ") || "none yet");
}
```

---

## Coding Agent Instructions

- **Always read this file before writing any code.**
- **Never hardcode API keys.** Use `process.env.VARIABLE_NAME` in backend, `os.environ.get()` in Ren'Py Python blocks.
- **Never call `/api/sprites` inside the conversation loop.** Only at session start.
- **Always include a fallback** for any API call that can fail.
- **Ren'Py image names have no extension** in `show` statements — use `show mara_neutral` not `show mara_neutral.png`.
- **JSON from Gemini may occasionally be malformed.** Always wrap parsing in try/catch and return a safe fallback neutral response.
- **Do not use Ren'Py `menu:` blocks for dialogue choices.** All player input goes through a free-text input box.
- **State is mutated in Ren'Py, not the backend.** The backend returns deltas; Ren'Py applies them.
- **When adding a new feature, check ending trigger thresholds first** — don't accidentally make an ending unreachable.
- **Never call `/api/music` inside the conversation loop.** Music tracks are pre-generated assets, not per-turn generations.
- **Lyria output varies per call.** If generating at runtime, always have a silent fallback — never block the game on music generation.
- **Music files live at `game-client/game/audio/music/<track>.mp3`.** Ren'Py references them as `"audio/music/neutral.mp3"` (relative to the `game/` folder).
- **Mood music crossfades — use `fadeout=1.5, fadein=1.5`** in `play music` calls so transitions feel intentional, not jarring.
- **Stop music before ending scenes** with `renpy.music.stop(fadeout=2.0)` then start the ending track fresh — endings should feel like a shift, not a continuation.
