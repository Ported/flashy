-- Flashy Leaderboard Schema
-- Run with: wrangler d1 execute flashy-leaderboard --file=schema.sql

CREATE TABLE IF NOT EXISTS leaderboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT UNIQUE NOT NULL,
    token TEXT NOT NULL,
    total_score INTEGER NOT NULL DEFAULT 0,
    highest_level INTEGER NOT NULL DEFAULT 1,
    total_stars INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast leaderboard queries (sorted by score descending)
CREATE INDEX IF NOT EXISTS idx_leaderboard_score ON leaderboard(total_score DESC);
