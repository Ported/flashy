/**
 * Database initialization endpoint
 * POST: Initialize the leaderboard table (for local dev/testing)
 */

interface Env {
  DB: D1Database;
}

// POST /api/init - Initialize database schema
export async function onRequestPost(context: { env: Env }): Promise<Response> {
  try {
    // Create the leaderboard table if it doesn't exist
    await context.env.DB.prepare(`
      CREATE TABLE IF NOT EXISTS leaderboard (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT UNIQUE NOT NULL,
        token TEXT NOT NULL,
        total_score INTEGER NOT NULL DEFAULT 0,
        highest_level INTEGER NOT NULL DEFAULT 1,
        total_stars INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
      )
    `).run();

    // Create index separately
    await context.env.DB.prepare(
      `CREATE INDEX IF NOT EXISTS idx_leaderboard_score ON leaderboard(total_score DESC)`
    ).run();

    return Response.json({ success: true, message: "Database initialized" });
  } catch (error) {
    console.error("Init error:", error);
    return Response.json({ error: "Failed to initialize database" }, { status: 500 });
  }
}
