-- Sample database initialization script
-- This file will be executed when PostgreSQL container starts

-- Create sample tables for data science projects
CREATE TABLE IF NOT EXISTS sample_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    value NUMERIC(10,2),
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO sample_data (name, value, category) VALUES
    ('Sample A', 123.45, 'Type 1'),
    ('Sample B', 67.89, 'Type 2'),
    ('Sample C', 234.56, 'Type 1'),
    ('Sample D', 345.67, 'Type 3')
ON CONFLICT DO NOTHING;