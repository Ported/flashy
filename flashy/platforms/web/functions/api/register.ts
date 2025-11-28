/**
 * Player registration endpoint
 * POST: Register a new player name (reserves it on the leaderboard)
 */

interface Env {
  DB: D1Database;
}

interface RegisterRequest {
  player_name: string;
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
