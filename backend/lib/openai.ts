import OpenAI from "openai";
import {
  buildSystemPrompt,
  FALLBACK_RESPONSE,
  type NpcState,
  type Message,
  type MaraResponse,
} from "./prompts";

let _client: OpenAI | null = null;
function getClient() {
  if (!_client) _client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  return _client;
}

const VALID_MOODS = new Set(["neutral", "warm", "suspicious", "afraid", "cold"]);

export async function callMara(
  playerInput: string,
  npcState: NpcState,
  history: Message[]
): Promise<Omit<MaraResponse, "audio_url">> {
  try {
    const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
      { role: "system", content: buildSystemPrompt(npcState) },
      ...history.map((m) => ({
        role: m.role as "user" | "assistant",
        content: m.content,
      })),
      { role: "user", content: playerInput },
    ];

    const completion = await getClient().chat.completions.create({
      model: "gpt-4o",
      messages,
      response_format: { type: "json_object" },
      temperature: 0.85,
    });

    const raw = completion.choices[0]?.message?.content ?? "{}";
    const parsed = JSON.parse(raw);

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
    console.error("[openai] callMara failed:", err);
    return { ...FALLBACK_RESPONSE, mood: npcState.mood };
  }
}
