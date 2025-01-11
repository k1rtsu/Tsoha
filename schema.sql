CREATE TABLE users (
    id SERIAL PRIMARY KEY,       
    username VARCHAR(50) NOT NULL UNIQUE, 
    password_hash VARCHAR(255) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(20) DEFAULT 'user'
);


CREATE TABLE regions (
    id SERIAL PRIMARY KEY,       
    name VARCHAR(100) NOT NULL UNIQUE, 
    description TEXT             
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,       
    region_id INT NOT NULL,      
    title VARCHAR(200) NOT NULL, 
    description TEXT,            
    created_by INT NOT NULL,     
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (region_id) REFERENCES regions (id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE SET NULL
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,      
    topic_id INT NOT NULL,       
    user_id INT NOT NULL,        
    content TEXT NOT NULL,       
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (topic_id) REFERENCES topics (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,      
    post_id INT NOT NULL,        
    user_id INT NOT NULL,        
    content TEXT NOT NULL,       
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
);
