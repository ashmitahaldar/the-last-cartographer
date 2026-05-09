import { callMara } from "../../../lib/openai";

export async function GET() {
  const testState = {
    trust: 50, suspicion: 20, lie_count: 0,
    mood: "neutral" as const, known_facts: [], unlocks: [], player_vulnerable: false,
  };

  try {
    const result = await callMara("Hello, I need your help finding a route through the mountains.", testState, []);
    return Response.json({ ok: true, result });
  } catch (err) {
    return Response.json({ ok: false, error: String(err) }, { status: 500 });
  }
}
