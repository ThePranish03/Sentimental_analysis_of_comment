
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
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (policy_id) REFERENCES Policies(policy_id)
);

-- Analysis Table (Per-Policy Summary)
CREATE TABLE IF NOT EXISTS Analysis (
    analysis_id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT UNIQUE,
    summary TEXT NOT NULL,
    sentiment ENUM('positive','negative','neutral') NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES Policies(policy_id)
);

-- Insert Users
INSERT INTO Users (name, email, password_hash, role) VALUES
('Admin User', 'admin@example.com', 'hashedpassword123', 'admin'),
('Stakeholder A', 'stakeholder@example.com', 'hashedpassword456', 'stakeholder'),
('Public User1', 'user1@example.com', 'hashedpassword789', 'public')
ON DUPLICATE KEY UPDATE email=email;

-- Insert a Policy
INSERT INTO Policies (policy_title, policy_description, section) VALUES
('Clean Energy Policy 2025', 'This policy aims to increase renewable energy adoption in rural areas.', 'Section A')
ON DUPLICATE KEY UPDATE policy_title=policy_title;

-- Insert Comments
INSERT INTO Comments (user_id, policy_id, comment_text) VALUES
(3, 1, 'This is a great step towards sustainability.'),
(2, 1, 'Implementation challenges must be considered.'),
(3, 1, 'Need subsidies for solar panels in villages.');

-- Insert Overall Analysis
INSERT INTO Analysis (policy_id, summary, sentiment) VALUES
(1, 'Overall, users support the Clean Energy Policy but highlight concerns regarding implementation and demand subsidies.', 'positive')
ON DUPLICATE KEY UPDATE summary=summary;
