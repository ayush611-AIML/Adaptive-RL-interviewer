import sqlite3
import random
import antigravity # Taking flight!
import streamlit as st
import torch
import numpy as np
from agent import InterviewDQN
from llm import grade_answer

@st.cache_resource
def load_model():
    model = InterviewDQN()
    model.load_state_dict(torch.load("dqn_model.pth"))
    model.eval()
    return model

agent = load_model()

if "mu" not in st.session_state:
    st.session_state.mu = 0.0
    st.session_state.sigma = 3.0
    st.session_state.questions_asked = 0
    st.session_state.chat_history = []

# Track asked questions so we don't repeat them
if "asked_question_ids" not in st.session_state:
    st.session_state.asked_question_ids = []

question_bank = {
    0: "Tier 1: Basic question",
    1: "Tier 2: Intermediate question",
    2: "Tier 3: Advanced question"
}

def fetch_question(tier):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    
    # Fetch all questions for the target tier
    cursor.execute("SELECT id, question_text FROM questions WHERE tier = ?", (tier,))
    all_questions = cursor.fetchall()
    conn.close()
    
    # Filter out questions we have already asked
    available_questions = [q for q in all_questions if q[0] not in st.session_state.asked_question_ids]
    
    if not available_questions:
        return "We have run out of questions for this difficulty level!"
        
    # Pick a random question from the available ones
    selected_question = random.choice(available_questions)
    
    # Record the ID so we don't ask it again
    st.session_state.asked_question_ids.append(selected_question[0])
    
    return f"Tier {tier}: {selected_question[1]}"


st.title("RL Interviewer")

with st.sidebar:
    st.header("Brain State")
    st.metric("Estimated Skill (μ)", f"{st.session_state.mu:.2f}")
    st.metric("Uncertainty (σ)", f"{st.session_state.sigma:.2f}")
    st.metric("Questions Asked", st.session_state.questions_asked)

# Predict next question
current_state = torch.FloatTensor([[st.session_state.mu, st.session_state.sigma, st.session_state.questions_asked]])
# Only fetch a new question if the user just answered the previous one, 
# or if it's the very first question.
if len(st.session_state.chat_history) % 2 == 0:
    with torch.no_grad():
        action = agent(current_state).argmax().item()
    
    st.session_state.current_question = fetch_question(action)

next_question = st.session_state.current_question

for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(text)

with st.chat_message("assistant"):
    st.write(next_question)

user_answer = st.chat_input("Type your answer here...")

if user_answer:
    st.session_state.chat_history.append(("assistant", next_question))
    st.session_state.chat_history.append(("user", user_answer))
    
    score = grade_answer(next_question, user_answer)
    learning_rate = 0.5 * st.session_state.sigma
    
    if score > 0.5:
        st.session_state.mu += learning_rate * (1 - score)
    else:
        st.session_state.mu -= learning_rate * (1 - score)
        
    st.session_state.sigma *= 0.8
    st.session_state.questions_asked += 1
    
    st.rerun()