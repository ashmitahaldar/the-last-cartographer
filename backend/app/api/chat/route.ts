import type { NextRequest } from "next/server";
import { callMara } from "../../../lib/openai";
import { generateSpeech } from "../../../lib/elevenlabs";
import { FALLBACK_RESPONSE, type NpcState, type Message } from "../../../lib/prompts";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export async function OPTIONS() {
  return new Response(null, { status: 204, headers: CORS });
}

const MAX_TURNS = 15;

export async function POST(request: NextRequest) {
  try {
    const { input, npc_state, history } = (await request.json()) as {
      input: string;
      npc_state: NpcState;
      history: Message[];
    };

    if (history.length / 2 >= MAX_TURNS) {
      return Response.json(
        {
          ...FALLBACK_RESPONSE,
          dialogue: "The hour is late. I have work to finish. Safe travels.",
          mood: "cold",
          audio_url: null,
        },
        { headers: CORS }
      );
    }

    const maraResponse = await callMara(input, npc_state, history);
    const audio_url = await generateSpeech(maraResponse.dialogue, maraResponse.mood);

    return Response.json({ ...maraResponse, audio_url }, { headers: CORS });
  } catch {
    return Response.json(
      { ...FALLBACK_RESPONSE, audio_url: null },
      { status: 200, headers: CORS }
    );
  }
}
