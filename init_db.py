import sqlite3

def setup_database():
    # This will create a file named 'questions.db' in your folder
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    
    # Create the table schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tier INTEGER,
            question_text TEXT
        )
    ''')
    
    # Clear existing data so you can re-run this script safely
    cursor.execute('DELETE FROM questions')
    
    # The Question Bank
    sample_questions = [
        # Tier 0: Easy / Fundamentals
        (0, "Explain the basic concept of Linear Regression and what the line of best fit represents."),
        (0, "What is Logistic Regression primarily used for?"),
        (0, "In Natural Language Processing, what is the core purpose of semantic analysis?"),
        
        # Tier 1: Medium / Architecture & Frameworks
        (1, "How does neighborhood aggregation work in Graph Neural Networks?"),
        (1, "Describe the architecture and primary use cases of an Autoencoder."),
        (1, "What is the mathematical difference between tabular Q-learning and a Deep Q-Network (DQN)?"),
        
        # Tier 2: Hard / Deep Implementation & Math
        (2, "Walk through the mathematical step-by-step problem-solving process of applying logistic regression to a newly generated synthetic dataset."),
        (2, "Explain the generator and discriminator adversarial loss functions in Generative Adversarial Networks (GANs)."),
        (2, "How do morphological transition tables function in complex machine translation pipelines?")
    ]
    
    # Bulk insert the questions
    cursor.executemany('INSERT INTO questions (tier, question_text) VALUES (?, ?)', sample_questions)
    
    conn.commit()
    conn.close()
    print("Success: 'questions.db' initialized and populated!")

if __name__ == "__main__":
    setup_database()