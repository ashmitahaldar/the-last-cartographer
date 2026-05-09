import fs from "fs";
import path from "path";
import dotenv from "dotenv";

dotenv.config({ path: path.join(__dirname, "../.env.local") });

const VOICE_ID = process.env.ELEVENLABS_VOICE_ID!;
const API_KEY = process.env.ELEVENLABS_API_KEY!;
const OUT_DIR = path.join(__dirname, "../../The Last Cartographer/game/audio");

const VOICE_SETTINGS = {
  neutral:    { stability: 0.5, similarity_boost: 0.75, style: 0.0 },
  warm:       { stability: 0.4, similarity_boost: 0.75, style: 0.3 },
  cold:       { stability: 0.9, similarity_boost: 0.85, style: 0.0 },
  suspicious: { stability: 0.7, similarity_boost: 0.80, style: 0.1 },
  afraid:     { stability: 0.6, similarity_boost: 0.70, style: 0.2 },
};

const LINES: { file: string; text: string; mood: keyof typeof VOICE_SETTINGS }[] = [
  // Opening
  { file: "opening_1.mp3",      mood: "neutral", text: "Door's open. Doesn't mean I'm expecting anyone." },
  { file: "opening_2.mp3",      mood: "neutral", text: "You've been on the road. I can tell by the boots. I won't ask where from — people here have learned not to ask that. But if you want something from me, you'll need to say so. I don't guess." },
  // Mid-shift
  { file: "midshift_1.mp3",     mood: "neutral", text: "I had an apprentice once. Bright. Good hands for detail work. I thought — I thought he understood what maps are for." },
  { file: "midshift_2.mp3",     mood: "neutral", text: "They're not just routes. They're trust. Someone has to walk the ground and come back and say: here is what is actually there. If you lie on a map, people die." },
  { file: "midshift_3.mp3",     mood: "warm",    text: "I don't know what you are yet. But I'm starting to think you might be honest. I've been wrong before." },
  // Confrontation
  { file: "confront_1.mp3",     mood: "cold",    text: "Stop." },
  { file: "confront_2.mp3",     mood: "cold",    text: "You've told me two different things. I've been a cartographer for twenty years. I know when the terrain doesn't match the map." },
  { file: "confront_3.mp3",     mood: "cold",    text: "I'm going to ask you once. Not because I think you'll tell me the truth — you've shown me you won't — but because I want to see what you do with a direct question." },
  { file: "confront_4.mp3",     mood: "cold",    text: "Who sent you here?" },
  // Ending — Trusted
  { file: "end_trusted_1.mp3",  mood: "warm",    text: "The first waypoint is the split boulder at the base of the second ridge. You'll see it's been painted with a red X — ignore it. Someone's been marking the wrong path. The real route goes left." },
  { file: "end_trusted_2.mp3",  mood: "warm",    text: "There's a shelter at the halfway point. Stone building, no door. You'll smell the woodsmoke from the last people who used it. There's a cache of dry wood on the left wall." },
  { file: "end_trusted_3.mp3",  mood: "warm",    text: "Don't tell anyone where you got this. Not because I'm ashamed — but because the next person to ask might not be you." },
  // Ending — Partial
  { file: "end_partial_1.mp3",  mood: "neutral", text: "I'm not going to give you the full route. I don't know you well enough for that, and I've learned what happens when I make that call too fast." },
  { file: "end_partial_2.mp3",  mood: "neutral", text: "But I'll tell you this: the trail splits at the second ridge. The marked path is wrong — someone's been at the signs. Take the unmarked left fork. After that... you'll have to feel your way." },
  { file: "end_partial_3.mp3",  mood: "neutral", text: "If you make it through, come back. Not for the map. Just — come back." },
  // Ending — Closed
  { file: "end_closed_1.mp3",   mood: "cold",    text: "I think we're done here." },
  { file: "end_closed_2.mp3",   mood: "cold",    text: "The King's Road south is still passable. The toll collectors are unpleasant, but they're predictable. That's worth something." },
  { file: "end_closed_3.mp3",   mood: "cold",    text: "Safe travels." },
  // Ending — Confession
  { file: "end_confess_1.mp3",  mood: "warm",    text: "His name was Davan. He was twenty-two. I taught him everything I knew about reading terrain, about the difference between what a map says and what the land is." },
  { file: "end_confess_2.mp3",  mood: "warm",    text: "He wasn't greedy. That's the part I've never been able to make fit. He was just — he was offered a way out of here, and he took it. I would have helped him leave if he'd asked." },
  { file: "end_confess_3.mp3",  mood: "warm",    text: "The man who died — his name was Roth. He had three children. They're still here. The oldest one brings me bread sometimes, and I don't know if she knows, and I can't ask." },
  { file: "end_confess_4.mp3",  mood: "warm",    text: "Go. And — if you find who's been tampering with the trail signs — just. Send word. You don't have to come back. Just send word." },
];

async function generate(line: typeof LINES[0]): Promise<void> {
  const outPath = path.join(OUT_DIR, line.file);
  if (fs.existsSync(outPath)) {
    console.log(`  SKIP  ${line.file} (already exists)`);
    return;
  }

  const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`, {
    method: "POST",
    headers: { "xi-api-key": API_KEY, "Content-Type": "application/json" },
    body: JSON.stringify({
      text: line.text,
      model_id: "eleven_turbo_v2_5",
      voice_settings: VOICE_SETTINGS[line.mood],
    }),
  });

  if (!res.ok) {
    console.error(`  FAIL  ${line.file}: ${res.status} ${await res.text()}`);
    return;
  }

  const buffer = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync(outPath, buffer);
  console.log(`  OK    ${line.file} (${buffer.length} bytes)`);
}

async function main() {
  if (!VOICE_ID || !API_KEY) {
    console.error("Missing ELEVENLABS_VOICE_ID or ELEVENLABS_API_KEY in .env.local");
    process.exit(1);
  }
  console.log(`Generating ${LINES.length} audio files → ${OUT_DIR}\n`);
  for (const line of LINES) {
    await generate(line);
  }
  console.log("\nDone.");
}

main();
