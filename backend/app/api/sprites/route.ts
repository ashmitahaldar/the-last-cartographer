import OpenAI from "openai";

let _client: OpenAI | null = null;
const getClient = () => {
  if (!_client) _client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  return _client;
};

type Mood = "neutral" | "warm" | "suspicious" | "afraid" | "cold";

const BASE =
  "Visual novel character portrait of Mara Voss, age 38, cartographer of a dying border town. Anime-influenced illustration style with clean lines, expressive eyes, and detailed shading. Long dark hair with grey streaks, loosely tied or falling over one shoulder. Sharp, intelligent eyes with a guarded expression. Ink-stained fingers, wearing a worn leather apron over plain clothes. At least one rolled map tucked at her side. Background: candlelit map shop with shelves of rolled parchment and a single candle flame, softly blurred. Full upper body portrait, character centred, transparent background.";

const MOOD_SUFFIX: Record<Mood, string> = {
  neutral:
    "Expression: guarded and still. She is not looking directly at the viewer — her gaze is directed slightly downward, watching hands rather than faces. Mouth neutral, posture measured. The look of someone who trusts nothing until it earns trust.",
  warm:
    "Expression: a rare and careful softening. A faint, genuine half-smile — not quite open, but no longer closed. Eyes slightly warmer, posture less rigid. She is starting to ask questions rather than deflect them. Still watchful, but the suspicion has eased.",
  suspicious:
    "Expression: narrowed eyes, jaw set, head tilted slightly as if re-evaluating. She looks directly at the viewer now — not with warmth, but with the focused attention of someone who has caught an inconsistency and is deciding what to do about it. Still. Controlled.",
  afraid:
    "Expression: outwardly composed but visibly tense — a tightness around the eyes, slightly pale, lips pressed together. She is afraid but will not show it openly. The fear is of making the same mistake again. Her gaze is careful, formal, measuring every word.",
  cold:
    "Expression: completely shut down. Hard, flat eyes looking past the viewer rather than at them. Mouth a thin line. She has already decided. The quieter she gets, the more final it is. This is not anger — it is the careful stillness of someone who has learned to control every small thing.",
};

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
    const { mood } = await req.json();

    if (!mood || !(mood in MOOD_SUFFIX)) {
      return Response.json(
        { error: `Unknown mood: ${mood}` },
        { status: 400, headers: CORS }
      );
    }

    const prompt = `${BASE} ${MOOD_SUFFIX[mood as Mood]}`;

    const response = await getClient().images.generate({
      model: "gpt-image-1",
      prompt,
      n: 1,
      size: "1024x1536",
      output_format: "png",
    });

    const b64 = response.data?.[0]?.b64_json;
    if (!b64) {
      return Response.json(
        { error: "No image data returned" },
        { status: 500, headers: CORS }
      );
    }

    return Response.json(
      { image_data: `data:image/png;base64,${b64}` },
      { headers: CORS }
    );
  } catch (e: any) {
    console.error("sprites route error:", e);
    return Response.json(
      { error: e.message ?? "sprite generation failed" },
      { status: 500, headers: CORS }
    );
  }
}
