import fs from "fs";
import path from "path";
import dotenv from "dotenv";
import { generateTrack, MusicTrack, MUSIC_PROMPTS } from "../lib/lyria";

dotenv.config({ path: path.join(__dirname, "../.env.local") });

const OUT_DIR = path.join(
  __dirname,
  "../../The Last Cartographer/game/audio/music"
);

async function main() {
  if (!process.env.GEMINI_API_KEY) {
    console.error("Missing GEMINI_API_KEY in .env.local");
    process.exit(1);
  }

  fs.mkdirSync(OUT_DIR, { recursive: true });
  const tracks = Object.keys(MUSIC_PROMPTS) as MusicTrack[];
  console.log(`Generating ${tracks.length} music tracks → ${OUT_DIR}\n`);

  for (const track of tracks) {
    const outPath = path.join(OUT_DIR, `${track}.mp3`);
    if (fs.existsSync(outPath)) {
      console.log(`  SKIP  ${track}.mp3 (already exists)`);
      continue;
    }
    try {
      console.log(`  GEN   ${track}.mp3 ...`);
      const buffer = await generateTrack(track);
      fs.writeFileSync(outPath, buffer);
      console.log(`  OK    ${track}.mp3 (${buffer.length} bytes)`);
    } catch (e: any) {
      console.error(`  FAIL  ${track}.mp3: ${e.message}`);
    }
  }

  console.log("\nDone.");
}

main();
