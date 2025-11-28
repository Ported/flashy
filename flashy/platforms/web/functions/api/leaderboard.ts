/**
 * Leaderboard API endpoint
 * GET: Fetch top 50 players
 * POST: Update player score
 */

interface Env {
  DB: D1Database;
}

interface LeaderboardEntry {
  player_name: string;
  total_score: number;
  highest_level: number;
  total_stars: number;
}

interface ScoreSubmission {
  player_name: string;
  token: string;
  total_score: number;
  highest_level: number;
  total_stars: number;
}

// GET /api/leaderboard - Fetch top 50 players
export async function onRequestGet(context: { env: Env }): Promise<Response> {
  try {
    const { results } = await context.env.DB.prepare(
      `SELECT player_name, total_score, highest_level, total_stars
       FROM leaderboard
       ORDER BY total_score DESC
       LIMIT 50`
    ).all<LeaderboardEntry>();

    const leaderboard = (results || []).map((entry, index) => ({
      rank: index + 1,
      ...entry,
    }));

    return Response.json({ leaderboard });
  } catch (error) {
    console.error("Leaderboard fetch error:", error);
    return Response.json({ error: "Failed to fetch leaderboard" }, { status: 500 });
  }
}

// POST /api/leaderboard - Update player score
export async function onRequestPost(context: {
  env: Env;
  request: Request;
}): Promise<Response> {
  try {
    const body: ScoreSubmission = await context.request.json();
    const { player_name, token, total_score, highest_level, total_stars } = body;

    // Validate input
    if (!player_name || typeof player_name !== "string") {
      return Response.json({ error: "Invalid player name" }, { status: 400 });
    }
    if (!token || typeof token !== "string") {
      return Response.json({ error: "Invalid token" }, { status: 400 });
    }
    if (typeof total_score !== "number" || total_score < 0) {
      return Response.json({ error: "Invalid score" }, { status: 400 });
    }

    // Update score (only if token matches)
    const result = await context.env.DB.prepare(
      `UPDATE leaderboard
       SET total_score = MAX(total_score, ?),
           highest_level = MAX(highest_level, ?),
           total_stars = MAX(total_stars, ?),
           updated_at = datetime('now')
       WHERE player_name = ? AND token = ?`
    )
      .bind(total_score, highest_level, total_stars, player_name, token)
      .run();

    // Check if update happened (token matched)
    if (result.meta.changes === 0) {
      return Response.json({ error: "Invalid token for player" }, { status: 403 });
    }

    // Get player's current rank
    const { results } = await context.env.DB.prepare(
      `SELECT COUNT(*) + 1 as rank
       FROM leaderboard
       WHERE total_score > (SELECT total_score FROM leaderboard WHERE player_name = ?)`
    )
      .bind(player_name)
      .all<{ rank: number }>();

    const rank = results?.[0]?.rank || 1;

    return Response.json({ success: true, rank });
  } catch (error) {
    console.error("Score update error:", error);
    return Response.json({ error: "Failed to update score" }, { status: 500 });
  }
}
