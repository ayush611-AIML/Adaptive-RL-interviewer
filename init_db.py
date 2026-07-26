import sqlite3

def setup_database():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS questions')
    cursor.execute('''
        CREATE TABLE questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            tier INTEGER, 
            subject TEXT, 
            question_text TEXT
        )
    ''')
    
    data = [
        # DSA
        (0, 'DSA', 'Reverse a linked list.'), 
        (1, 'DSA', 'Find the longest substring without repeating characters.'),
        (1, 'DSA', 'Detect a cycle in a linked list.'),
        
        # OOP
        (0, 'OOP', 'Explain the four pillars of OOP.'), 
        (1, 'OOP', 'Difference between Interface and Abstract Class.'),
        (1, 'OOP', 'What is method overriding?'),
        
        # DBMS
        (0, 'DBMS', 'Difference between DELETE, DROP, and TRUNCATE.'), 
        (1, 'DBMS', 'Explain INNER JOIN and LEFT JOIN.'),
        (2, 'DBMS', 'Write an SQL query to find the second highest salary.'),
        
        # Operating System
        (0, 'Operating System', 'Difference between process and thread.'), 
        (1, 'Operating System', 'What is a deadlock?'),
        (1, 'Operating System', 'What is virtual memory?'),
        
        # Computer Networks
        (0, 'Computer Networks', 'Difference between HTTP and HTTPS.'), 
        (1, 'Computer Networks', 'Explain the TCP three-way handshake.'),
        
        # System Design
        (1, 'System Design', 'Explain the CAP Theorem.'), 
        (2, 'System Design', 'Design a URL shortener.'),
        
        # Programming Languages
        (0, 'Programming Languages', 'Difference between list and tuple in Python.'), 
        (1, 'Programming Languages', 'Explain Python decorators.'),
        
        # Software Engineering
        (0, 'Software Engineering', 'Explain Agile methodology.'), 
        (1, 'Software Engineering', 'What is Git branching?'),
        
        # Web Development
        (0, 'Web Development', 'Explain the difference between HTML, CSS, and JS.'), 
        (1, 'Web Development', 'What is a REST API?'),
        
        # Projects
        (0, 'Projects', 'Tell me about the problem statement for your most recent project.'), 
        (2, 'Projects', 'What was your hardest technical challenge?'),
        
        # Machine Learning
        (0, 'Machine Learning', 'Difference between Supervised and Unsupervised Learning?'), 
        (2, 'Machine Learning', 'Explain Transformers architecture.'),
        
        # HR Questions
        (0, 'HR Questions', 'Tell me about yourself.'), 
        (0, 'HR Questions', 'Why should we hire you?')
    ]
    
    cursor.executemany('INSERT INTO questions (tier, subject, question_text) VALUES (?, ?, ?)', data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()