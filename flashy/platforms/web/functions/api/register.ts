/**
 * Player registration endpoint
 * POST: Register a new player name (reserves it on the leaderboard)
 */

import { BLOCKED_WORDS } from "./blocklist";

interface Env {
  DB: D1Database;
}

interface RegisterRequest {
  player_name: string;
}

/**
 * Check if a name contains blocked words.
 * Normalizes common letter substitutions (l33t speak).
 */
export function containsBlockedWord(name: string): boolean {
  // Normalize: lowercase and common substitutions
  const normalized = name
    .toLowerCase()
    .replace(/0/g, "o")
    .replace(/1/g, "i")
    .replace(/3/g, "e")
    .replace(/4/g, "a")
    .replace(/5/g, "s")
    .replace(/@/g, "a")
    .replace(/\$/g, "s")
    .replace(/[_\-\s]/g, ""); // Remove separators

  // Check if any blocked word appears as a substring
  for (const word of BLOCKED_WORDS) {
    if (normalized.includes(word)) {
      return true;
    }
  }
  return false;
}

// POST /api/register - Reserve a player name
export async function onRequestPost(context: {
  env: Env;
  request: Request;
}): Promise<Response> {
  try {
    const body: RegisterRequest = await context.request.json();
    const { player_name } = body;

    // Validate input
    if (!player_name || typeof player_name !== "string") {
      return Response.json({ error: "Invalid player name" }, { status: 400 });
    }

    // Sanitize name (same rules as frontend)
    const safeName = player_name.replace(/[^a-zA-Z0-9 \-_]/g, "").trim();
    if (!safeName || safeName.length === 0) {
      return Response.json({ error: "Invalid player name" }, { status: 400 });
    }

    if (safeName.length > 20) {
      return Response.json({ error: "Name too long (max 20 characters)" }, { status: 400 });
    }

    // Check for inappropriate names (return same error as "taken" to not reveal filtering)
    if (containsBlockedWord(safeName)) {
      return Response.json(
        { error: "Name already taken", available: false },
        { status: 409 }
      );
    }

    // Generate a token for this player
    const token = crypto.randomUUID();

    // Try to insert the player (will fail if name exists due to UNIQUE constraint)
    try {
      await context.env.DB.prepare(
        `INSERT INTO leaderboard (player_name, token, total_score, highest_level, total_stars)
         VALUES (?, ?, 0, 1, 0)`
      )
        .bind(safeName, token)
        .run();

      return Response.json({ success: true, player_name: safeName, token });
    } catch (insertError: unknown) {
      // Check if it's a unique constraint violation
      if (
        insertError instanceof Error &&
        insertError.message.includes("UNIQUE constraint failed")
      ) {
        return Response.json(
          { error: "Name already taken", available: false },
          { status: 409 }
        );
      }
      throw insertError;
    }
  } catch (error) {
    console.error("Registration error:", error);
    return Response.json({ error: "Failed to register player" }, { status: 500 });
  }
}

// GET /api/register?name=X - Check if name is available
export async function onRequestGet(context: {
  env: Env;
  request: Request;
}): Promise<Response> {
  try {
    const url = new URL(context.request.url);
    const name = url.searchParams.get("name");

    if (!name) {
      return Response.json({ error: "Name parameter required" }, { status: 400 });
    }

    // Check blocklist first (report as unavailable, same as taken)
    if (containsBlockedWord(name)) {
      return Response.json({ available: false, player_name: name });
    }

    const { results } = await context.env.DB.prepare(
      `SELECT 1 FROM leaderboard WHERE player_name = ?`
    )
      .bind(name)
      .all();

    const available = !results || results.length === 0;

    return Response.json({ available, player_name: name });
  } catch (error) {
    console.error("Name check error:", error);
    return Response.json({ error: "Failed to check name" }, { status: 500 });
  }
}
