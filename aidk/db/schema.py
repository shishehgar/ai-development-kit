"""
Database schema.
"""

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    path TEXT NOT NULL UNIQUE,
    language TEXT NOT NULL DEFAULT 'Unknown',
    engineering_score INTEGER NOT NULL DEFAULT 0,
    knowledge_score INTEGER NOT NULL DEFAULT 0,
    security_score INTEGER NOT NULL DEFAULT 0,
    deployment_score INTEGER NOT NULL DEFAULT 0,
    maturity_score INTEGER NOT NULL DEFAULT 0,
    maturity_level TEXT NOT NULL DEFAULT 'Initial',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS git_info (
    project_id INTEGER PRIMARY KEY,
    branch TEXT NOT NULL DEFAULT '',
    clean INTEGER NOT NULL DEFAULT 0,
    remote INTEGER NOT NULL DEFAULT 0,
    remote_name TEXT NOT NULL DEFAULT '',
    remote_url TEXT NOT NULL DEFAULT '',
    last_commit_hash TEXT NOT NULL DEFAULT '',
    last_commit_author TEXT NOT NULL DEFAULT '',
    last_commit_date TEXT NOT NULL DEFAULT '',
    modified_files INTEGER NOT NULL DEFAULT 0,
    staged_files INTEGER NOT NULL DEFAULT 0,
    untracked_files INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS project_features (
    project_id INTEGER PRIMARY KEY,
    docker INTEGER NOT NULL DEFAULT 0,
    continue_config INTEGER NOT NULL DEFAULT 0,
    readme INTEGER NOT NULL DEFAULT 0,
    license INTEGER NOT NULL DEFAULT 0,
    tests INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    recommendation TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_projects_name
ON projects(name);

CREATE INDEX IF NOT EXISTS idx_projects_path
ON projects(path);

CREATE INDEX IF NOT EXISTS idx_recommendations_project
ON recommendations(project_id);
"""
