import streamlit as st
import torch
import numpy as np
import sqlite3
import random
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
    st.session_state.asked_question_ids = []

def fetch_question(tier):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, question_text FROM questions WHERE tier = ?", (tier,))
    all_questions = cursor.fetchall()
    conn.close()
    
    available_questions = [q for q in all_questions if q[0] not in st.session_state.asked_question_ids]
    
    if not available_questions:
        return "We have run out of questions for this difficulty level!"
        
    selected_question = random.choice(available_questions)
    st.session_state.asked_question_ids.append(selected_question[0])
    
    return f"Tier {tier}: {selected_question[1]}"

st.title("RL Interviewer")

# ------------- SEAMLESS CSS GRADIENT BACKGROUND -------------
def set_premium_background():
    st.markdown(
        """
        <style>
        /* Modern, subtle animated gradient background applied to the very root */
        .stApp {
            background: linear-gradient(-45deg, #0f172a, #1e1b4b, #020617, #172554) !important;
            background-size: 400% 400% !important;
            animation: gradient 15s ease infinite !important;
            color: #f8fafc;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* FORCE ALL BORDERS AND CONTAINERS TO BE TRANSPARENT */
        [data-testid="stHeader"], 
        [data-testid="stAppViewContainer"], 
        [data-testid="stBottom"],
        .stApp > header,
        .stAppBottom,
        footer {
            background-color: transparent !important;
            background: transparent !important;
        }

        /* Glassmorphism sidebar */
        [data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.2) !important;
            backdrop-filter: blur(15px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Styling the metrics in the sidebar */
        [data-testid="stMetricValue"] {
            font-size: 2.5rem !important;
            color: #38bdf8 !important;
            font-weight: 700 !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 1rem !important;
            color: #94a3b8 !important;
        }

        /* Main title styling */
        h1 {
            background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            padding-bottom: 20px;
        }

        /* Chat bubbles styling */
        [data-testid="stChatMessage"] {
            background-color: rgba(30, 41, 59, 0.6);
            border-radius: 10px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 10px;
        }

        /* Input box styling */
        .stChatInputContainer {
            background-color: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid #38bdf8 !important;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        /* Ensure general text remains readable */
        p, div {
            color: #e2e8f0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_premium_background()
# -----------------------------------------------------------

with st.sidebar:
    st.header("Brain State")
    st.metric("Estimated Skill (μ)", f"{st.session_state.mu:.2f}")
    st.metric("Uncertainty (σ)", f"{st.session_state.sigma:.2f}")
    st.metric("Questions Asked", st.session_state.questions_asked)

current_state = torch.FloatTensor([[st.session_state.mu, st.session_state.sigma, st.session_state.questions_asked]])

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