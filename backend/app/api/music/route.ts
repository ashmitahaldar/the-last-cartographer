import { generateTrack, MusicTrack, MUSIC_PROMPTS } from "../../../lib/lyria";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export async function OPTIONS() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function POST(req: Request) {
  try {
    const { track } = await req.json();

    if (!track || !(track in MUSIC_PROMPTS)) {
      return Response.json(
        { error: `Unknown track: ${track}` },
        { status: 400, headers: CORS }
      );
    }

    const buffer = await generateTrack(track as MusicTrack);
    const b64 = buffer.toString("base64");

    return Response.json(
      { audio_data: `data:audio/mpeg;base64,${b64}` },
      { headers: CORS }
    );
  } catch (e: any) {
    console.error("music route error:", e);
    return Response.json(
      { error: e.message ?? "music generation failed" },
      { status: 500, headers: CORS }
    );
  }
}
