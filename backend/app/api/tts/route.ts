import type { NextRequest } from "next/server";
import { generateSpeech } from "../../../lib/elevenlabs";
import type { Mood } from "../../../lib/prompts";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export async function OPTIONS() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function POST(request: NextRequest) {
  try {
    const { text, mood } = (await request.json()) as { text: string; mood: Mood };
    const audio_url = await generateSpeech(text, mood);
    return Response.json({ audio_url }, { headers: CORS });
  } catch {
    return Response.json({ audio_url: null }, { status: 200, headers: CORS });
  }
}
