import type { Mood } from "./prompts";

const VOICE_SETTINGS: Record<Mood, { stability: number; similarity_boost: number; style: number }> = {
  neutral:    { stability: 0.5, similarity_boost: 0.75, style: 0.0 },
  warm:       { stability: 0.4, similarity_boost: 0.75, style: 0.3 },
  suspicious: { stability: 0.7, similarity_boost: 0.80, style: 0.1 },
  afraid:     { stability: 0.6, similarity_boost: 0.70, style: 0.2 },
  cold:       { stability: 0.9, similarity_boost: 0.85, style: 0.0 },
};

export async function generateSpeech(text: string, mood: Mood): Promise<string | null> {
  const voiceId = process.env.ELEVENLABS_VOICE_ID;
  const apiKey = process.env.ELEVENLABS_API_KEY;

  if (!voiceId || !apiKey) return null;

  try {
    const settings = VOICE_SETTINGS[mood] ?? VOICE_SETTINGS.neutral;
    const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`, {
      method: "POST",
      headers: {
        "xi-api-key": apiKey,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text,
        model_id: "eleven_turbo_v2_5",
        voice_settings: settings,
      }),
    });

    if (!res.ok) {
      console.error("[elevenlabs] TTS failed:", res.status, await res.text());
      return null;
    }

    const buffer = await res.arrayBuffer();
    const base64 = Buffer.from(buffer).toString("base64");
    return `data:audio/mpeg;base64,${base64}`;
  } catch {
    return null;
  }
}
