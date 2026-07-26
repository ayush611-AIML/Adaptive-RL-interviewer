import sqlite3

def setup_database():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    
    # Drop the old table so we can rebuild it with the new 'subject' column
    cursor.execute('DROP TABLE IF EXISTS questions')
    
    # Create the new table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tier INTEGER,
            subject TEXT,
            question_text TEXT
        )
    ''')
    
    new_questions = [
         # 1. HR Questions
        (0, 'HR Questions', 'Tell me about yourself.'),
        (0, 'HR Questions', 'What are your biggest strengths and weaknesses?'),
        (0, 'HR Questions', 'Where do you see yourself in five years?'),
        (0, 'HR Questions', 'Why should we hire you for this Software Engineering role?')
        
        # 2. Data Structures and Algorithms (DSA)
        (0, 'DSA', 'Reverse a linked list.'),
        (0, 'DSA', 'Detect a cycle in a linked list.'),
        (0, 'DSA', 'Merge two sorted arrays.'),
        (1, 'DSA', 'Find the longest substring without repeating characters.'),
        (1, 'DSA', 'Explain the concept of Dynamic Programming with an example.'),
        (2, 'DSA', 'Find the shortest path in a graph.'),
        (2, 'DSA', 'Explain how Backtracking works in the N-Queens problem.'),
        
        # 3. Object-Oriented Programming (OOP)
        (0, 'OOP', 'Explain the four pillars of OOP.'),
        (0, 'OOP', 'What is method overriding?'),
        (1, 'OOP', 'Difference between Interface and Abstract Class.'),
        (1, 'OOP', 'Explain Encapsulation and provide a real-world example.'),
        
        # 4. Database Management System (DBMS)
        (0, 'DBMS', 'Difference between DELETE, DROP, and TRUNCATE.'),
        (1, 'DBMS', 'Explain INNER JOIN and LEFT JOIN.'),
        (1, 'DBMS', 'Write an SQL query to find the second highest salary.'),
        (2, 'DBMS', 'Explain ACID properties in Database Transactions.'),
        (2, 'DBMS', 'What is Database Normalization and why is it used?'),
        
        # 5. Operating System (OS)
        (0, 'Operating System', 'Difference between process and thread.'),
        (1, 'Operating System', 'What is a deadlock?'),
        (1, 'Operating System', 'What is virtual memory?'),
        (2, 'Operating System', 'Explain Context Switching.'),
        (2, 'Operating System', 'What is the difference between a Mutex and a Semaphore?'),
        
        # 6. Computer Networks (CN)
        (0, 'Computer Networks', 'Difference between HTTP and HTTPS.'),
        (1, 'Computer Networks', 'Explain the TCP three-way handshake.'),
        (1, 'Computer Networks', 'What happens when you enter a URL in the browser?'),
        (2, 'Computer Networks', 'Explain the differences between TCP and UDP.'),
        
        # 7. System Design
        (1, 'System Design', 'Explain the CAP Theorem.'),
        (1, 'System Design', 'What is a Load Balancer and why is it necessary?'),
        (2, 'System Design', 'Design a URL shortener like Bitly.'),
        (2, 'System Design', 'Explain how you would design the architecture for WhatsApp.'),
        (2, 'System Design', 'Design YouTube (video uploading and streaming).'),
        
        # 8. Programming Languages
        (0, 'Programming Languages', 'Difference between list and tuple in Python.'),
        (1, 'Programming Languages', 'Explain Python decorators.'),
        (1, 'Programming Languages', 'What is garbage collection in Java?'),
        (2, 'Programming Languages', 'Explain Multithreading and memory management.'),
        
        # 9. Software Engineering
        (0, 'Software Engineering', 'Explain Agile methodology.'),
        (1, 'Software Engineering', 'What is Git branching?'),
        (1, 'Software Engineering', 'Explain the basics of CI/CD.'),
        (2, 'Software Engineering', 'What is the Singleton design pattern?'),
        
        # 10. Web Development Basics
        (0, 'Web Development', 'Explain the difference between HTML, CSS, and JavaScript.'),
        (1, 'Web Development', 'What is a REST API?'),
        (1, 'Web Development', 'What are Cookies and how are they used in sessions?'),
        (2, 'Web Development', 'Explain JWT (JSON Web Tokens) Authentication.'),
        
        # 11. Projects
        (0, 'Projects', 'Tell me about the problem statement for your most recent project.'),
        (1, 'Projects', 'Explain the architecture and technologies used in your main project.'),
        (2, 'Projects', 'What was the hardest technical challenge you faced in your project, and how did you solve it?'),
        
        # 12. Machine Learning
        (0, 'Machine Learning', 'What is the difference between Supervised and Unsupervised Learning?'),
        (1, 'Machine Learning', 'What is overfitting and how do you prevent it using Cross Validation?'),
        (2, 'Machine Learning', 'Explain the basic architecture of Transformers.'),
        (2, 'Machine Learning', 'When would you use a CNN versus an RNN?'),
        
    ]
    
    # Insert the questions into the database
    cursor.executemany('INSERT INTO questions (tier, subject, question_text) VALUES (?, ?, ?)', new_questions)
    conn.commit()
    conn.close()
    print("Database successfully rebuilt with Subjects!")

if __name__ == "__main__":
    setup_database()