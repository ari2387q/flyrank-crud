CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO tasks (title, done)
SELECT 'Buy milk', FALSE
WHERE NOT EXISTS (SELECT 1 FROM tasks);

INSERT INTO tasks (title, done)
SELECT 'Learn FastAPI', TRUE
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE title = 'Learn FastAPI');

INSERT INTO tasks (title, done)
SELECT 'Write API', FALSE
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE title = 'Write API');
