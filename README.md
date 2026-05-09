# The Last Cartographer

An AI-powered visual novel where the NPC is genuinely thinking. Built with Ren'Py and a Next.js backend.

---

## Setup

### 1. Backend

```bash
cd backend
npm install
```

Create `backend/.env.local` with the following variables:

```env
# Claude (Anthropic) — NPC dialogue
ANTHROPIC_API_KEY=

# ElevenLabs — voiced dialogue
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=

# OpenAI — sprite generation (GPT Image 2)
OPENAI_API_KEY=

# Google Vertex AI — Lyria music generation
# Paste the full contents of your service account JSON as a single-line string
GOOGLE_APPLICATION_CREDENTIALS_JSON=

# Vercel deployment URL (used by Ren'Py in production)
NEXT_PUBLIC_BACKEND_URL=https://your-app.vercel.app
```

> **Never commit `.env.local` or your service account JSON file.** Both are excluded by `.gitignore`.

Start the backend locally:

```bash
npm run dev
```

The API will be available at `http://localhost:3000`.

---

### 2. Ren'Py client

Open `The Last Cartographer/` in Ren'Py 8. The game connects to `http://localhost:3000` by default. To point it at your deployed Vercel backend, update `BACKEND_URL` in `The Last Cartographer/game/api.rpy`.

---

### 3. Deploying the backend (Vercel)

```bash
cd backend
vercel --prod
```

Add each variable from `.env.local` to your Vercel project under **Settings → Environment Variables**. For `GOOGLE_APPLICATION_CREDENTIALS_JSON`, paste the entire JSON object as the value (no file path — Vercel doesn't support file-based credentials).

---

## Pre-generating assets

Sprites and music are generated once and committed as static files. To regenerate:

```bash
# Character sprites (requires OPENAI_API_KEY)
cd backend && npx ts-node scripts/generate-sprites.ts

# Music tracks (requires GOOGLE_APPLICATION_CREDENTIALS_JSON)
cd backend && npx ts-node scripts/generate-music.ts
```

Output goes to `The Last Cartographer/game/images/` and `The Last Cartographer/game/audio/music/` respectively.
