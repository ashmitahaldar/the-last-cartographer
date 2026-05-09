# The Last Cartographer

An AI-powered visual novel where the NPC is genuinely thinking. Built with Ren'Py and a Next.js backend deployed on Vercel.

---

## What it is

You arrive in Veldthorn — a dying town at the edge of empire. The Northern Pass is the only way through the mountains, and the only person who knows the safe route is Mara Voss, the town's cartographer. She doesn't share it with strangers.

There are no dialogue choices. You type what you say. Mara — powered by GPT-4o — tracks trust, suspicion, and whether you've contradicted yourself across the full conversation. What she tells you, and which of the four endings you reach, is determined in real time by the AI based on how the conversation went.

The core idea: the AI acts as a game director, not a chatbot. NPC state drives world outcomes.

---

## Endings

- **The Confession** — Mara shares the story she's never told anyone. You leave with the complete map and the weight of knowing why she gave it to you.
- **The Trusted Stranger** — She hands you a working copy. Not her best. Enough.
- **The Partial Crossing** — One waypoint and a warning. You'll have to feel your way through the rest.
- **The Closed Door** — She opens it. Precisely. She won't look at you again.
- **Terra Incognita** — You leave without what you came for. Some conversations just show you where the door is.

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Game engine | Ren'Py 8 |
| NPC dialogue | GPT-4o (OpenAI) |
| Voice | ElevenLabs — emotion-aware TTS, settings shift per mood |
| Character sprites | GPT Image 2 (OpenAI) — one portrait per emotional state |
| Music | Lyria (Google Vertex AI) — generative tracks per mood and ending |
| Backend | Next.js 14 App Router, deployed on Vercel |

---

## How the AI works

Every player message is sent to a Next.js backend with:
- The full conversation history
- Mara's current state (`trust`, `suspicion`, `lie_count`, `mood`, `known_facts`, `unlocks`)

GPT-4o returns structured JSON — dialogue, trust/suspicion deltas, mood, whether a lie was detected, and whether an unlock was earned. The game applies the deltas and updates state client-side. The backend never holds state between turns.

Mara has five unlockable story beats (`north_waypoints`, `north_pass`, `marker_sabotage`, `hidden_shelter`, `davan_story`), each gated behind genuine state thresholds. The confession ending requires `davan_story` to be unlocked, zero detected lies, and the player to have expressed genuine personal vulnerability — all of which the AI tracks independently.

ElevenLabs TTS fires in parallel with the GPT-4o call once the dialogue string is ready, so audio arrives in the same response. Music crossfades when Mara's mood changes.

---

## Repository structure

```
the-last-cartographer/
├── The Last Cartographer/        ← Ren'Py project
│   └── game/
│       ├── script.rpy            ← main VN script, scene labels, endings
│       ├── api.rpy               ← HTTP calls to backend, state update logic
│       ├── state.rpy             ← npc_state, ending trigger logic
│       ├── ui.rpy                ← title screen, input, suggestion hints
│       ├── hud.rpy               ← live state display
│       ├── images/               ← Mara sprites (5 moods) + backgrounds
│       └── audio/                ← voiced lines, mood music, ending tracks
└── backend/                      ← Next.js API
    ├── app/api/
    │   ├── chat/route.ts         ← main NPC endpoint
    │   ├── tts/route.ts          ← ElevenLabs proxy
    │   ├── sprites/route.ts      ← GPT Image 2 sprite generation
    │   └── music/route.ts        ← Lyria music generation
    ├── lib/
    │   ├── openai.ts             ← GPT-4o dialogue client
    │   ├── elevenlabs.ts         ← ElevenLabs client
    │   ├── lyria.ts              ← Lyria music client (Vertex AI)
    │   └── prompts.ts            ← Mara system prompt + response schema
    └── scripts/
        ├── generate-audio.ts     ← pre-generate all voiced lines
        ├── generate-sprites.ts   ← pre-generate all mood sprites
        └── generate-music.ts     ← pre-generate all music tracks
```

---

## Setup

### 1. Backend

```bash
cd backend
npm install
```

Create `backend/.env.local`:

```env
# OpenAI — NPC dialogue (GPT-4o) + sprite generation (GPT Image 2)
OPENAI_API_KEY=

# ElevenLabs — voiced dialogue
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=

# Google Vertex AI — Lyria music generation
# Paste the full contents of your service account JSON as a single-line string
GOOGLE_APPLICATION_CREDENTIALS_JSON=

# Vercel deployment URL (used by Ren'Py in production)
NEXT_PUBLIC_BACKEND_URL=https://your-app.vercel.app
```

> **Never commit `.env.local` or your service account JSON file.** Both are excluded by `.gitignore`.

```bash
npm run dev
```

API available at `http://localhost:3000`.

---

### 2. Ren'Py client

Open `The Last Cartographer/` in Ren'Py 8. The game connects to `http://localhost:3000` by default. To point at your deployed Vercel backend, update `BACKEND_URL` in `game/api.rpy`.

---

### 3. Deploy backend (Vercel)

```bash
cd backend && vercel --prod
```

Add all `.env.local` variables under **Settings → Environment Variables**. For `GOOGLE_APPLICATION_CREDENTIALS_JSON`, paste the entire JSON object as the value — Vercel doesn't support file-based credentials.

---

## Pre-generating assets

Sprites and music are generated once and committed as static files.

```bash
# Voiced lines (requires ELEVENLABS_API_KEY + ELEVENLABS_VOICE_ID)
cd backend && npx ts-node scripts/generate-audio.ts

# Character sprites (requires OPENAI_API_KEY)
cd backend && npx ts-node scripts/generate-sprites.ts

# Music tracks (requires GOOGLE_APPLICATION_CREDENTIALS_JSON)
cd backend && npx ts-node scripts/generate-music.ts
```

Output goes to `The Last Cartographer/game/audio/`, `game/images/`, and `game/audio/music/` respectively. The scripts skip files that already exist.
