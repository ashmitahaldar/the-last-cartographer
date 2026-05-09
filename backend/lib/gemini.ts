import { GoogleGenerativeAI } from "@google/generative-ai";
import {
  buildSystemPrompt,
  FALLBACK_RESPONSE,
  type NpcState,
  type Message,
  type MaraResponse,
} from "./prompts";

const genai = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);

const VALID_MOODS = new Set(["neutral", "warm", "suspicious", "afraid", "cold"]);

export async function callMara(
  playerInput: string,
  npcState: NpcState,
  history: Message[]
): Promise<Omit<MaraResponse, "audio_url">> {
  const model = genai.getGenerativeModel({
    model: "gemini-2.0-flash",
    systemInstruction: buildSystemPrompt(npcState),
  });

  const contents = [
    ...history.map((m) => ({
      role: m.role === "assistant" ? ("model" as const) : ("user" as const),
      parts: [{ text: m.content }],
    })),
    { role: "user" as const, parts: [{ text: playerInput }] },
  ];

  try {
    const result = await model.generateContent({ contents });
    const raw = result.response.text().trim();
    // Strip markdown code fences Gemini sometimes adds
    const cleaned = raw.replace(/^```(?:json)?\n?/, "").replace(/\n?```$/, "");
    const parsed = JSON.parse(cleaned);

    return {
      dialogue: typeof parsed.dialogue === "string" ? parsed.dialogue : "...",
      trust_delta: typeof parsed.trust_delta === "number" ? Math.max(-20, Math.min(20, parsed.trust_delta)) : 0,
      suspicion_delta: typeof parsed.suspicion_delta === "number" ? Math.max(-10, Math.min(20, parsed.suspicion_delta)) : 0,
      mood: VALID_MOODS.has(parsed.mood) ? parsed.mood : npcState.mood,
      unlock: typeof parsed.unlock === "string" ? parsed.unlock : null,
      inner_thought: typeof parsed.inner_thought === "string" ? parsed.inner_thought : "",
      lie_detected: Boolean(parsed.lie_detected),
      new_known_fact: typeof parsed.new_known_fact === "string" ? parsed.new_known_fact : null,
      player_vulnerable: Boolean(parsed.player_vulnerable),
    };
  } catch (err) {
    console.error("[gemini] callMara failed:", err);
    return { ...FALLBACK_RESPONSE, mood: npcState.mood };
  }
}
