-- Create database
CREATE DATABASE IF NOT EXISTS fnapdb;
USE fnapdb;

-- Table for officials
CREATE TABLE officials (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    workplace VARCHAR(150),
    level VARCHAR(100),
    image VARCHAR(250),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table for trainings
CREATE TABLE trainings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table that relates officials and trainings
CREATE TABLE training_history (
    id_history INT PRIMARY KEY AUTO_INCREMENT,
    official_id INT,
    training_id INT,
    training_date DATE,
    training_city VARCHAR(100),
    modality VARCHAR(50),
    duration VARCHAR(50),
    state VARCHAR(100),
    other_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (official_id) REFERENCES officials(id),
    FOREIGN KEY (training_id) REFERENCES trainings(id)
);

-- Table for users
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table for logs
CREATE TABLE logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(255) NOT NULL,
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE Seguimiento_Curso_Lote (
    id_seguimiento INT PRIMARY KEY AUTO_INCREMENT,
    id_historial INT NOT NULL,
    id_curso INT NOT NULL,
    estado ENUM('No Iniciado', 'En Progreso', 'Completado', 'No Completado') NOT NULL DEFAULT 'No Iniciado',
    fecha_inicio DATE,
    fecha_completado DATE,
    calificacion DECIMAL(4,2),
    FOREIGN KEY (id_historial) REFERENCES Historial(id_historial),
    FOREIGN KEY (id_curso) REFERENCES Cursos(id_curso),
    UNIQUE (id_historial, id_curso) -- Garantiza que no se duplique el seguimiento de un curso para el mismo historial
);