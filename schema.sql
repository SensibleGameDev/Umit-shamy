-- Ескі кестелерді жою (бар болса)
--DROP TABLE IF EXISTS mood_entries;
--DROP TABLE IF EXISTS questions;
--DROP TABLE IF EXISTS appointments;

-- Көңіл-күй күнделігі кестесі
CREATE TABLE mood_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Сұрақ-жауап кестесі
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    answer_text TEXT, -- Бұл жерді психолог толтырады
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Психологқа жазылу кестесі
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    contact_info TEXT NOT NULL, -- Email, Telegram, т.б.
    preferred_time TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ЖАҢА КЕСТЕ: Қолдау қабырғасы
CREATE TABLE support_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT NOT NULL,
    post_text TEXT NOT NULL,
    candle_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);