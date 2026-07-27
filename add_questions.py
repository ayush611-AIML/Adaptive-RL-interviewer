import sqlite3

def add_new_questions():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()

    # List of new questions (tier, subject, question_text)
    # Tier 0: Easy, Tier 1: Medium, Tier 2: Hard
    new_questions = [
        # --- DSA ---
        (0, "DSA", "Explain the difference between a stack and a queue."),
        (1, "DSA", "How does a hash table resolve collisions?"),
        (2, "DSA", "Explain the concept of dynamic programming and give an example of a problem it solves."),
        
        # --- Machine Learning ---
        (0, "Machine Learning", "Can you explain the mathematical differences between linear regression and logistic regression?"),
        (1, "Machine Learning", "Walk me through the architecture differences and specific use cases of Convolutional Neural Networks, Autoencoders, and Generative Adversarial Networks."),
        (1, "Machine Learning", "How do you calculate and utilize morphological transition tables in Natural Language Processing?"),
        (2, "Machine Learning", "Explain the neighborhood aggregation mechanisms used in Graph Neural Networks and Graph Attention Networks."),
        (2, "Machine Learning", "What is the primary difference between standard Q-learning and Deep Q Networks (DQN) in reinforcement learning?"),
        
        # --- Projects ---
        (0, "Projects", "Describe a time you had to build a step-by-step presentation to explain complex mathematical concepts to an audience."),
        (1, "Projects", "Walk me through a deep learning software experiment you've coded in Python from start to finish."),
        (2, "Projects", "How do you evaluate and select appropriate research papers to source content for technical presentations?"),
        
        # --- HR Questions ---
        (0, "HR Questions", "How do you prioritize multiple demanding project deadlines at the same time?"),
        (1, "HR Questions", "Can you explain the difference between Trait Emotional Intelligence and Ability Emotional Intelligence, and how you apply them in a team setting?"),
        (2, "HR Questions", "Tell me about a time you had to learn a highly specialized academic topic quickly to prepare for a major evaluation.")
    ]

    print("Adding new questions to the database...")
    
    count = 0
    for tier, subject, text in new_questions:
        # Check if question already exists to prevent duplicates
        cursor.execute("SELECT id FROM questions WHERE question_text = ?", (text,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO questions (tier, subject, question_text) VALUES (?, ?, ?)", (tier, subject, text))
            count += 1
            
    conn.commit()
    conn.close()
    print(f"Success! Added {count} new questions.")

if __name__ == "__main__":
    add_new_questions()