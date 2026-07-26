import streamlit as st
import streamlit.components.v1 as components
import torch
import sqlite3
import random
import init_db
from agent import InterviewDQN
from llm import grade_answer
from streamlit_mic_recorder import speech_to_text

# Safely initialize database on startup
try:
    init_db.setup_database()
except Exception:
    pass

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

def fetch_question(tier, subject):
    conn = sqlite3.connect('questions.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute("SELECT id, question_text FROM questions WHERE tier = ? AND subject = ?", (tier, subject))
    available = [q for q in cursor.fetchall() if q[0] not in st.session_state.asked_question_ids]
    conn.close()
    
    if not available:
        return f"We have run out of questions for {subject} at this difficulty level!"
        
    sel = random.choice(available)
    st.session_state.asked_question_ids.append(sel[0])
    return sel[1]

st.title("RL Interviewer")

# ------------- QUANTUM AI CSS THEME -------------
def set_premium_background():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #09090e 0%, #171033 50%, #061e33 100%) !important;
            background-size: 300% 300% !important;
            animation: gradient 12s ease infinite !important;
            color: #f8fafc;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        [data-testid="stHeader"], 
        [data-testid="stAppViewContainer"], 
        [data-testid="stBottom"],
        [data-testid="stBottomBlock"],
        .stApp > header,
        .stAppBottom,
        footer {
            background-color: transparent !important;
            background: transparent !important;
        }
        
        div[data-testid="stBottom"] > * {
            background-color: transparent !important;
        }

        [data-testid="stSidebar"] {
            background-color: rgba(20, 15, 40, 0.4) !important;
            backdrop-filter: blur(20px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        .stSelectbox div[data-baseweb="select"] div, 
        div[data-baseweb="popover"] div {
            color: #ffffff !important;
        }

        div[data-baseweb="popover"] {
            background-color: #171033 !important;
            border: 1px solid rgba(0, 229, 255, 0.2) !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 2.5rem !important;
            color: #00e5ff !important; 
            font-weight: 800 !important;
            text-shadow: 0px 0px 15px rgba(0, 229, 255, 0.4);
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 1rem !important;
            color: #a1a1aa !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        h1 {
            background: -webkit-linear-gradient(45deg, #00e5ff, #b026ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900 !important;
            letter-spacing: 1.5px;
            padding-bottom: 20px;
        }

        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 16px !important;
            padding: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
            margin-bottom: 15px;
        }

        /* Custom Styling for Mic Recorder Button */
        div.row-widget.stButton > button {
            background: rgba(10, 10, 20, 0.8) !important;
            border: 1px solid rgba(0, 229, 255, 0.4) !important;
            color: #00e5ff !important;
            border-radius: 30px !important;
            padding: 10px 25px !important;
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.2) !important;
            transition: all 0.3s ease;
        }
        
        div.row-widget.stButton > button:hover {
            background: rgba(0, 229, 255, 0.1) !important;
            border-color: #00e5ff !important;
            box-shadow: 0 0 25px rgba(0, 229, 255, 0.4) !important;
        }
        
        p, div {
            color: #e2e8f0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_premium_background()

# ------------- INTERACTIVE CURSOR PARTICLES -------------
def add_particle_effect():
    components.html(
        """
        <script>
            const parentDoc = window.parent.document;
            if (!parentDoc.getElementById("quantum-particles")) {
                const canvas = parentDoc.createElement("canvas");
                canvas.id = "quantum-particles";
                canvas.style.position = "fixed";
                canvas.style.top = "0";
                canvas.style.left = "0";
                canvas.style.width = "100vw";
                canvas.style.height = "100vh";
                canvas.style.pointerEvents = "none";
                canvas.style.zIndex = "99999";
                parentDoc.body.appendChild(canvas);

                const ctx = canvas.getContext("2d");
                let particlesArray = [];
                
                function resize() {
                    canvas.width = window.parent.innerWidth;
                    canvas.height = window.parent.innerHeight;
                }
                window.parent.addEventListener("resize", resize);
                resize();

                const mouse = { x: undefined, y: undefined };
                
                window.parent.addEventListener("mousemove", function(event) {
                    mouse.x = event.x;
                    mouse.y = event.y;
                    for (let i = 0; i < 4; i++) { 
                        particlesArray.push(new Particle());
                    }
                });

                class Particle {
                    constructor() {
                        this.x = mouse.x;
                        this.y = mouse.y;
                        this.size = Math.random() * 4 + 1;
                        this.speedX = Math.random() * 3 - 1.5;
                        this.speedY = Math.random() * 3 - 1.5;
                        this.color = Math.random() > 0.5 ? '#00e5ff' : '#b026ff';
                    }
                    update() {
                        this.x += this.speedX;
                        this.y += this.speedY;
                        if (this.size > 0.1) this.size -= 0.05;
                    }
                    draw() {
                        ctx.fillStyle = this.color;
                        ctx.beginPath();
                        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                        ctx.fill();
                    }
                }

                function handleParticles() {
                    for (let i = 0; i < particlesArray.length; i++) {
                        particlesArray[i].update();
                        particlesArray[i].draw();
                        if (particlesArray[i].size <= 0.1) {
                            particlesArray.splice(i, 1);
                            i--;
                        }
                    }
                }

                function animate() {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    handleParticles();
                    window.parent.requestAnimationFrame(animate);
                }
                
                animate();
            }
        </script>
        """,
        height=0,
        width=0,
    )

add_particle_effect()
# -----------------------------------------------------------

with st.sidebar:
    selected_subject = st.selectbox(
        "Select Subject", 
        [
            "DSA", "OOP", "DBMS", "Operating System", 
            "Computer Networks", "System Design", "Programming Languages", 
            "Software Engineering", "Web Development", "Projects", 
            "Machine Learning", "HR Questions"
        ]
    )
    
    if st.button("🔄 Reset Interview"):
        st.session_state.update(mu=0.0, sigma=3.0, questions_asked=0, chat_history=[], asked_question_ids=[])
        st.rerun()

    st.markdown("---")
    st.header("Brain State")
    st.metric("Estimated Skill (μ)", f"{st.session_state.mu:.2f}")
    st.metric("Uncertainty (σ)", f"{st.session_state.sigma:.2f}")
    st.metric("Questions Asked", st.session_state.questions_asked)

current_state = torch.FloatTensor([[st.session_state.mu, st.session_state.sigma, st.session_state.questions_asked]])

if len(st.session_state.chat_history) % 2 == 0:
    with torch.no_grad():
        action = agent(current_state).argmax().item()
    
    st.session_state.current_question = fetch_question(action, selected_subject)

next_question = st.session_state.current_question

for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(text)

with st.chat_message("assistant"):
    st.write(next_question)

# ------------- STYLISH CENTERED MIC RECORDER BUTTON -------------
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<div style='text-align: center;'>🎙️ <b>Click to Speak Answer</b></div>", unsafe_allow_html=True)
    user_answer = speech_to_text(language='en', start_prompt="🎙️ Start Recording", stop_prompt="⏹️ Stop Recording", just_once=True, key='STT')

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