import { GoogleAuth } from "google-auth-library";

export type MusicTrack =
  | "neutral"
  | "warm"
  | "suspicious"
  | "afraid"
  | "cold"
  | "ending_trusted"
  | "ending_partial"
  | "ending_closed"
  | "ending_confession";

export const MUSIC_PROMPTS: Record<MusicTrack, string> = {
  neutral:
    "Sparse melancholic folk instrumental. Solo acoustic guitar, minor key, slow tempo. A traveller arriving somewhere forgotten. No drums. No resolution.",
  warm:
    "Gentle folk instrumental, acoustic guitar and soft strings, warm and tentative. A cautious sense of hope beginning to form.",
  suspicious:
    "Tense minimal dark folk. Slow plucked strings, long silences, unsettling undertone. Repeating motif that never resolves.",
  afraid:
    "Deeply unsettling dark ambient drone. Low sustained strings, dissonant tones, no melody, no rhythm. The feeling of dread before something bad happens. No instruments that sound pleasant or hopeful.",
  cold:
    "Bleak minimal dark ambient. Single low piano note with long decay, hollow reverb, long silences. No melody, no warmth, no resolution. A door closing that will never open again.",
  ending_trusted:
    "Quiet triumphant folk piece, no vocals. Begins with solo guitar, builds slowly with strings. Bittersweet resolution — a journey beginning, tinged with loss.",
  ending_partial:
    "Unresolved folk instrumental. Guitar that starts to build then holds back. Hopeful but uncertain. The feeling of enough but not everything.",
  ending_closed:
    "Minimal dark folk. A single guitar phrase repeated and fading. No resolution. The feeling of a wrong turn only understood too late.",
  ending_confession:
    "Deeply emotional folk piece, no vocals. Piano and cello, intimate and fragile. Two people who finally understood each other, too briefly.",
};

const auth = new GoogleAuth({
  scopes: ["https://www.googleapis.com/auth/cloud-platform"],
  ...(process.env.GOOGLE_APPLICATION_CREDENTIALS_JSON
    ? { credentials: JSON.parse(process.env.GOOGLE_APPLICATION_CREDENTIALS_JSON) }
    : {}),
});

export async function generateTrack(track: MusicTrack): Promise<Buffer> {
  const project = process.env.GOOGLE_CLOUD_PROJECT;
  const location = process.env.GOOGLE_CLOUD_LOCATION ?? "us-central1";

  if (!project) throw new Error("GOOGLE_CLOUD_PROJECT env var is not set");

  const client = await auth.getClient();
  const tokenResponse = await client.getAccessToken();
  const token = tokenResponse.token;
  if (!token) throw new Error("Failed to get Google OAuth token");

  const endpoint = `https://${location}-aiplatform.googleapis.com/v1/projects/${project}/locations/${location}/publishers/google/models/lyria-002:predict`;

  const res = await fetch(endpoint, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json; charset=utf-8",
    },
    body: JSON.stringify({
      instances: [{ prompt: MUSIC_PROMPTS[track] }],
      parameters: {},
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Lyria ${track} failed ${res.status}: ${err}`);
  }

  const data = await res.json();
  const b64 = data?.predictions?.[0]?.bytesBase64Encoded;
  if (!b64) throw new Error(`No audio in Lyria response for: ${track}`);

  return Buffer.from(b64, "base64");
}
