-- Create Database
CREATE DATABASE IF NOT EXISTS sih_project;
USE sih_project;

-- Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'stakeholder', 'public') DEFAULT 'public',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Policies Table
CREATE TABLE IF NOT EXISTS Policies (
    policy_id INT AUTO_INCREMENT PRIMARY KEY,
    policy_title VARCHAR(255) NOT NULL,
    policy_description TEXT NOT NULL,
    section VARCHAR(100),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('open','closed') DEFAULT 'open'
);

-- Comments Table
CREATE TABLE IF NOT EXISTS Comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    policy_id INT,
    comment_text TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
	FOREIGN KEY (policy_id) REFERENCES Policies(policy_id) ON DELETE CASCADE
);

-- Analysis Table (Per-Policy Summary)
CREATE TABLE IF NOT EXISTS Analysis (
    analysis_id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT UNIQUE,
    summary TEXT NOT NULL,
    sentiment ENUM('positive','negative','neutral') NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES Policies(policy_id) ON DELETE CASCADE
);

-- Logs Table 
CREATE TABLE IF NOT EXISTS Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(255),
    performed_by INT,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (performed_by) REFERENCES Users(user_id) ON DELETE SET NULL
);

-- Insert Admin User
INSERT INTO Users (name, email, password_hash, role)
VALUES (
    'Admin',
    'admin@example.com',
    -- Hash your password using Python or MySQL's SHA2 (not recommended for production, just for testing)
    SHA2('admin123', 256),
    'admin'
);

--Indexes for easier search
CREATE INDEX idx_user_id ON Comments(user_id);
CREATE INDEX idx_policy_id ON Comments(policy_id);
CREATE INDEX idx_policy_analysis ON Analysis(policy_id);

CREATE VIEW PolicyWithComments AS
SELECT 
    p.policy_id,
    p.policy_title,
    u.name AS user_name,
    c.comment_text,
    c.submitted_at
FROM Policies p
JOIN Comments c ON p.policy_id = c.policy_id
JOIN Users u ON c.user_id = u.user_id;

CREATE VIEW PolicyWithAnalysis AS
SELECT 
    p.policy_id,
    p.policy_title,
    a.summary,
    a.sentiment,
    a.generated_at
FROM Policies p
JOIN Analysis a ON p.policy_id = a.policy_id;


CREATE VIEW PolicySummary AS
SELECT 
    p.policy_id,
    p.policy_title,
    COUNT(c.comment_id) AS total_comments,
    a.sentiment,
    a.summary
FROM Policies p
LEFT JOIN Comments c ON p.policy_id = c.policy_id
LEFT JOIN Analysis a ON p.policy_id = a.policy_id
GROUP BY p.policy_id, a.sentiment, a.summary;
