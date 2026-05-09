import fs from "fs";
import path from "path";
import dotenv from "dotenv";
import OpenAI from "openai";

dotenv.config({ path: path.join(__dirname, "../.env.local") });

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const OUT_DIR = path.join(
  __dirname,
  "../../The Last Cartographer/game/images"
);

const BASE =
  "Visual novel character portrait of Mara Voss, age 38, cartographer of a dying border town. Anime-influenced illustration style with clean lines, expressive eyes, and detailed shading. Long dark hair with grey streaks, loosely tied or falling over one shoulder. Sharp, intelligent eyes with a guarded expression. Ink-stained fingers, wearing a worn leather apron over plain clothes. At least one rolled map tucked at her side. Background: candlelit map shop with shelves of rolled parchment and a single candle flame, softly blurred. Full upper body portrait, character centred, transparent background.";

const SPRITES: { mood: string; suffix: string }[] = [
  {
    mood: "neutral",
    suffix:
      "Expression: guarded and still. She is not looking directly at the viewer — her gaze is directed slightly downward, watching hands rather than faces. Mouth neutral, posture measured. The look of someone who trusts nothing until it earns trust.",
  },
  {
    mood: "warm",
    suffix:
      "Expression: a rare and careful softening. A faint, genuine half-smile — not quite open, but no longer closed. Eyes slightly warmer, posture less rigid. She is starting to ask questions rather than deflect them. Still watchful, but the suspicion has eased.",
  },
  {
    mood: "suspicious",
    suffix:
      "Expression: narrowed eyes, jaw set, head tilted slightly as if re-evaluating. She looks directly at the viewer now — not with warmth, but with the focused attention of someone who has caught an inconsistency and is deciding what to do about it. Still. Controlled.",
  },
  {
    mood: "afraid",
    suffix:
      "Expression: outwardly composed but visibly tense — a tightness around the eyes, slightly pale, lips pressed together. She is afraid but will not show it openly. The fear is of making the same mistake again. Her gaze is careful, formal, measuring every word.",
  },
  {
    mood: "cold",
    suffix:
      "Expression: completely shut down. Hard, flat eyes looking past the viewer rather than at them. Mouth a thin line. She has already decided. The quieter she gets, the more final it is. This is not anger — it is the careful stillness of someone who has learned to control every small thing.",
  },
];

async function generate(sprite: typeof SPRITES[0]): Promise<void> {
  const outPath = path.join(OUT_DIR, `mara_${sprite.mood}.png`);
  if (fs.existsSync(outPath)) {
    console.log(`  SKIP  mara_${sprite.mood}.png (already exists)`);
    return;
  }

  console.log(`  GEN   mara_${sprite.mood}.png ...`);
  const response = await client.images.generate({
    model: "gpt-image-1",
    prompt: `${BASE} ${sprite.suffix}`,
    n: 1,
    size: "1024x1536",
    output_format: "png",
  });

  const b64 = response.data?.[0]?.b64_json;
  if (!b64) {
    console.error(`  FAIL  mara_${sprite.mood}.png: no b64_json in response`);
    return;
  }

  const buffer = Buffer.from(b64, "base64");
  fs.writeFileSync(outPath, buffer);
  console.log(`  OK    mara_${sprite.mood}.png (${buffer.length} bytes)`);
}

async function main() {
  if (!process.env.OPENAI_API_KEY) {
    console.error("Missing OPENAI_API_KEY in .env.local");
    process.exit(1);
  }
  fs.mkdirSync(OUT_DIR, { recursive: true });
  console.log(`Generating ${SPRITES.length} sprites → ${OUT_DIR}\n`);
  for (const sprite of SPRITES) {
    await generate(sprite);
  }
  console.log("\nDone.");
}

main();
