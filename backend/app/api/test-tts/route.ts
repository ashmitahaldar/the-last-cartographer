import { generateSpeech } from "../../../lib/elevenlabs";

export async function GET() {
  const audio_url = await generateSpeech(
    "The pass isn't something I discuss with strangers.",
    "neutral"
  );

  if (!audio_url) {
    return Response.json({ ok: false, error: "generateSpeech returned null — check backend terminal for details" });
  }

  return Response.json({ ok: true, bytes: audio_url.length, preview: audio_url.slice(0, 60) });
}
