-- Көңіл-күй күнделігі кестесі
CREATE TABLE IF NOT EXISTS mood_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Сұрақ-жауап кестесі
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    answer_text TEXT, 
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Психологқа жазылу кестесі
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    contact_info TEXT NOT NULL, 
    preferred_time TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Қолдау қабырғасы
CREATE TABLE IF NOT EXISTS support_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT NOT NULL,
    post_text TEXT NOT NULL,
    candle_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
