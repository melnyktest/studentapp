import mysql.connector
from db_config import DB_CONFIG 

connection = mysql.connector.connect(**DB_CONFIG)

cursor = connection.cursor()

# Create students table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        birth_date DATE NOT NULL,
        class_name VARCHAR(255) NOT NULL
    )
''')

# Create quarters table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS quarters (
        id INT AUTO_INCREMENT PRIMARY KEY,
        year INTEGER NOT NULL,
        quarter ENUM('Q1', 'Q2', 'Q3', 'Q4') NOT NULL,
        UNIQUE(year, quarter)
    )
''')

# Create grades table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT,
        quarter_id INT,
        course_id INT,
        grade INTEGER NOT NULL CHECK (grade BETWEEN 0 AND 100),
        UNIQUE(student_id, course_id, quarter_id),
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
        FOREIGN KEY (quarter_id) REFERENCES quarters(id) ON DELETE CASCADE
    )
''')

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
