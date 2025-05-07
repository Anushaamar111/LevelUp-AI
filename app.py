import streamlit as st
import json
from task_generator import generate_tasks
from send import send_whatsapp_message  # ✅ Import the WhatsApp sender

st.set_page_config(page_title="🧠 Life Coach Bot")
st.title("🧠 Life Coach Bot – Daily Tasks")

# Load or update user profile
if "profile" not in st.session_state:
    try:
        with open("user_profile.json", "r") as f:
            st.session_state.profile = json.load(f)
    except FileNotFoundError:
        st.session_state.profile = {}

with st.expander("👤 Update Your Life Context"):
    goal = st.text_input("What is your main goal?", value=st.session_state.profile.get("goal", ""))
    skills = st.text_area("What are your current skills?", value=st.session_state.profile.get("skills", ""))
    daily_time = st.text_input("How much time can you spend per day?", value=st.session_state.profile.get("daily_time", ""))
    learning_style = st.selectbox("Preferred Learning Style", ["Visual", "Hands-On", "Reading", "Listening"], index=0)
    motivation = st.slider("How motivated are you?", 1, 10, value=int(st.session_state.profile.get("motivation", 7)))

    if st.button("💾 Save Profile"):
        profile = {
            "goal": goal,
            "skills": skills,
            "daily_time": daily_time,
            "learning_style": learning_style,
            "motivation": motivation
        }
        with open("user_profile.json", "w") as f:
            json.dump(profile, f, indent=2)
        st.success("Profile saved!")

# Generate today's tasks
if st.button("🚀 Generate Today's Tasks"):
    tasks = generate_tasks()
    st.session_state["tasks"] = tasks
    send_whatsapp_message(f"🧠 Your Daily LifeCoach Tasks:\n\n{tasks}")  # ✅ Send WhatsApp Message
    st.success("Tasks sent via WhatsApp!")

# Show tasks
if "tasks" in st.session_state:
    st.subheader("📋 Today's Tasks")
    st.markdown(st.session_state["tasks"])

    with open("tasks.json", "w") as f:
        json.dump({"date": str(st.session_state["tasks"])}, f, indent=2)
