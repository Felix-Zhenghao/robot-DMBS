CREATE DATABASE IF NOT EXISTS RobotDB;
USE RobotDB;

CREATE TABLE IF NOT EXISTS Robots (
    model VARCHAR(255) PRIMARY KEY NOT NULL,
    dof INT NOT NULL, -- Degree of Freedom
    robotType ENUM('single_arm', 'bimanual', 'humanoid', 'legged', 'wheeled', 'flying')
);

CREATE TABLE IF NOT EXISTS HumanDemonstrators (
    demonstratorID INT PRIMARY KEY AUTO_INCREMENT
);

CREATE TABLE IF NOT EXISTS Experience (
    robotModel VARCHAR(255),
    demonstratorID INT,
    experience ENUM('novice', 'intermediate', 'expert'),
    FOREIGN KEY (robotModel) REFERENCES Robots(model),
    FOREIGN KEY (demonstratorID) REFERENCES HumanDemonstrators(demonstratorID)
);


CREATE TABLE IF NOT EXISTS Objects (
    objectName VARCHAR(255) PRIMARY KEY NOT NULL,
    classification ENUM('rigid', 'deformable', 'elasto-plastic', 'composite')
);

CREATE TABLE IF NOT EXISTS Tasks (
    taskName VARCHAR(255) PRIMARY KEY,
    taskDescription VARCHAR(255) NOT NULL,
    taskSpecification JSON NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard'),
    taskType ENUM('dexterous_manipulation', 'contact_rich', 'long_horizon')
);

CREATE TABLE IF NOT EXISTS Subtasks (
    subtaskID INT PRIMARY KEY AUTO_INCREMENT,
    taskName VARCHAR(255) NOT NULL,
    subtaskDescription TEXT NOT NULL,
    relativeObject VARCHAR(255) NOT NULL,
    FOREIGN KEY (taskName) REFERENCES Tasks(taskName),
    FOREIGN KEY (relativeObject) REFERENCES Objects(objectName)
);

CREATE TABLE IF NOT EXISTS Demonstrations (
    demoID INT PRIMARY KEY AUTO_INCREMENT,
    createTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    trainingDataKey TEXT,
    dataGenKey TEXT,
    filePathNPZ VARCHAR(255),
    demonstratorID INT,
    robotModel VARCHAR(255),
    taskName VARCHAR(255),
    success BOOLEAN,
    label ENUM('source_demo', 'robot_generated', 'pre-intervention', 'intervention'),
    FOREIGN KEY (demonstratorID) REFERENCES HumanDemonstrators(demonstratorID),
    FOREIGN KEY (taskName) REFERENCES Tasks(taskName),
    FOREIGN KEY (robotModel) REFERENCES Robots(model)
);

CREATE TABLE IF NOT EXISTS ObjectTasks (
    objectTaskID INT PRIMARY KEY AUTO_INCREMENT,
    taskName VARCHAR(255),
    objectName VARCHAR(255),
    objectPositionX DECIMAL(10, 6),
    objectPositionY DECIMAL(10, 6),
    objectPositionZ DECIMAL(10, 6),
    randomizationRange DECIMAL(10, 6),
    FOREIGN KEY (taskName) REFERENCES Tasks(taskName),
    FOREIGN KEY (objectID) REFERENCES Objects(objectName)
);
