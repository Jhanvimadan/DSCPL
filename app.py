import streamlit as st
from ask_llama import ask_llama
from chatbot_engine import get_devotion, get_prayer, get_meditation, get_accountability
from utils.api_integration import get_video_url
from utils.calender_utils import authenticate_google_calendar, create_event
from streamlit_javascript import st_javascript
import datetime
from database.db_manager import save_reminder, get_user_reminders
from scheduler.reminder_scheduler import start_scheduler
import threading
import streamlit.components.v1 as components

# --- Scheduler ---
def run_scheduler():
    thread = threading.Thread(target=start_scheduler, daemon=True)
    thread.start()

run_scheduler()

st.set_page_config(page_title="DSCPL Spiritual Assistant", layout="wide")

# --- Custom Style for Peaceful Theme ---
st.markdown("""
    <style>
        .stApp {
            background-color: #fff8e1;
            color: #333333;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #ffe0b2;
        }
        .stButton>button {
            background-color: #ffe0b2 !important;
            color: #4e342e !important;
            border: none;
        }
        .stSidebar {
            background-color: #ffecb3 !important;
            color: #4e342e !important;
        }
        .stSelectbox label, .stCheckbox label, .stTextInput label, .stTimeInput label {
            color: #4e342e !important;
        }
        .stSelectbox div, .stCheckbox div, .stTextInput div, .stTimeInput div {
            color: #893f45 !important;
        }
        .css-1n76uvr, .css-1kyxreq {
            color: #4e342e !important;
        }
        input[type="checkbox"]:checked + div:before {
            background-color: #66bb6a !important;
        }

        /* Dark background for assistant replies using streamlit chat message role */
        [data-testid="st.chat_message"]:has(div[data-testid="stMarkdownContainer"]):has(div:has(svg[aria-label="✝️"])) {
            background-color: #e0e0e0 !important;
            border-radius: 10px;
            padding: 10px;
            color: #2c2c2c !important;
        }

        .block-container {
            padding: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- TTS ---
def speak(text):
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance({text!r});
        msg.rate = 1;
        msg.pitch = 1;
        msg.volume = 1;
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code)

# --- Sidebar Navigation ---
st.sidebar.title("✝️ DSCPL")
nav_options = ["🏠 Home", "📖 Daily Devotion", "🙏 Prayer", "🧘 Meditation", "🛡️ Accountability", "💬 Chat", "📊 Progress Dashboard", "⏰ Reminders"]
for option in nav_options:
    if st.sidebar.button(option):
        st.session_state.nav_override = option
nav = st.session_state.get("nav_override", "🏠 Home")

# --- State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are DSCPL, a compassionate, faith-based AI who supports users through scripture, spiritual wisdom, and encouragement."}
    ]
if "last_reply" not in st.session_state:
    st.session_state.last_reply = ""
if "completed_devotions" not in st.session_state:
    st.session_state.completed_devotions = []

# --- Home Page ---
with st.sidebar:
    if st.button("🚨 Emergency SOS", key="sos_button"):
        st.session_state.nav_override = "🚨 SOS"
        st.rerun()

if nav == "🏠 Home":
    st.markdown("""
    <h1 style='text-align: center;'>Your Faithful Spiritual Companion, Digitally</h1>
    <p style='text-align: center; color: gray;'>Welcome to DSCPL — an AI-powered Christian chatbot designed to guide, uplift, and support you through daily devotions, prayers, meditations, and biblical wisdom.</p>
    """, unsafe_allow_html=True)

    services = [
        ("📖 Daily Devotion", "Engage with scripture daily."),
        ("🙏 Prayer", "Faith-filled prayers for you."),
        ("🧘 Meditation", "Calm your spirit with guided reflections."),
        ("🛡️ Accountability", "Find strength and stay on track."),
        ("💬 Chat", "Open conversation with your spiritual companion")
    ]
    cols = st.columns(len(services))
    for i, (title, desc) in enumerate(services):
        with cols[i]:
            if st.button(f"{title}", key=f"service_{i}"):
                st.session_state.nav_override = title
                st.rerun()

    service_styles = [
        "#ffe0b2", "#e0f7fa", "#f3e5f5", "#fff9c4", "#d7ccc8"
    ]

    cols = st.columns(len(services))
    for i, (title, desc) in enumerate(services):
        with cols[i]:
            components.html(f"""
            <div onclick=\"fetch('', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/x-www-form-urlencoded'}},
                    body: 'nav_override=' + encodeURIComponent('{title}')
                }}).then(() => window.location.reload())\"
                style=\"
                    cursor: pointer;
                    padding: 1.2rem;
                    border-radius: 15px;
                    background-color: {service_styles[i]};
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                    text-align: center;
                    font-family: sans-serif;
                    transition: transform 0.2s ease;
                \"
                onmouseover=\"this.style.transform='scale(1.03)'\"
                onmouseout=\"this.style.transform='scale(1)'\"
            >
                <div style=\"font-size: 1.3rem; font-weight: bold; color: #4e342e;\">{title}</div>
                <p style=\"color: #4e342e;\">{desc}</p>
            </div>
            """, height=180)
elif nav == "🚨 SOS":
    st.header("🚨 Emergency Support")
    st.subheader("You're not alone. Let's take a moment.")

    # 1. Scripture for Strength
    st.markdown("**📖 1 Peter 5:7 — _'Cast all your anxiety on Him because He cares for you.'_**")

    # 2. Calming Prompt
    st.markdown("🧘 **Take a deep breath:** Inhale for 4 seconds → Hold for 4 → Exhale for 4")
    st.balloons()

    # 3. Instant Prayer
    st.subheader("🙏 Emergency Prayer")
    st.write("Dear God, please bring peace and strength to my heart in this moment of fear or distress. Surround me with your love and remind me I'm not alone. Amen.")

    # 4. Emergency Contact
    emergency_number = "9152987821"  # Replace with a real helpline or dynamic entry
    st.markdown(f"📞 **Need help now? Call: [{emergency_number}](tel:{emergency_number})**")

    # 5. Optional Email to Accountability Partner (Dummy)
    st.text_input("Enter email of accountability partner (optional)", key="sos_email")
    if st.button("📧 Notify Accountability Partner"):
        st.success("Email sent! (Mock functionality)")
        # You can integrate `smtplib` or an email API here.

# --- Daily Devotion with Scheduling ---
elif nav == "📖 Daily Devotion":
    st.header("📖 Daily Devotion")
    if "devotion_plan" not in st.session_state and "plan_ready" not in st.session_state:
        topic = st.selectbox("Pick a Devotion Topic", [
            "Dealing with Stress", "Overcoming Fear", "Conquering Depression", "Relationships",
            "Healing", "Purpose & Calling", "Anxiety", "Something else..."
        ])
        length = st.selectbox("Choose Program Length", ["7 days", "14 days", "30 days"])

        st.markdown("### 🗓️ Schedule Your Devotion")
        set_reminder = st.toggle("Set Daily Reminder")
        reminder_time = st.time_input("Time for Reminder (24-hour)", value=datetime.time(8, 0)) if set_reminder else None
        sync_calendar = st.checkbox("📅 Sync with Google Calendar")

        if st.button("📖 Begin Program"):
            st.session_state.devotion_plan = [get_devotion(topic) for _ in range(int(length.split()[0]))]
            st.session_state.current_day = 0
            st.session_state.selected_topic = topic
            st.session_state.plan_ready = True

            if set_reminder:
                user_id = "user"  # replace with dynamic if available
                formatted_time = reminder_time.strftime("%H:%M")
                save_reminder(user_id, f"Devotion: {topic}", formatted_time)
                st.success(f"✅ Reminder set for {formatted_time}")

            if sync_calendar:
                st.info("🔗 Connecting to Google Calendar...")
                service = authenticate_google_calendar()
                for i in range(len(st.session_state.devotion_plan)):
                    date = datetime.datetime.now() + datetime.timedelta(days=i)
                    create_event(
                        service,
                        summary=f"Day {i+1} - Devotion",
                        description=f"DSCPL Devotion: {topic}",
                        start_datetime=date.replace(hour=reminder_time.hour, minute=reminder_time.minute)
                    )
                st.success("📅 Events added to Google Calendar")

 # --- Devotion Plan View (continued) ---
if nav == "📖 Daily Devotion" and st.session_state.get("plan_ready"):
    st.markdown(f"### 📅 Day {st.session_state.current_day + 1}")
    plan = st.session_state.devotion_plan[st.session_state.current_day]
    st.subheader("📖 Scripture")
    st.markdown(f"<b>{plan['scripture']}</b>", unsafe_allow_html=True)
    if 'verse' in plan:
        st.markdown(f"<i>{plan['verse']}</i>", unsafe_allow_html=True)

    st.subheader("🙏 Prayer")
    st.write(plan["prayer"])
    st.subheader("🗣️ Declaration")
    st.write(plan["declaration"])

    st.subheader("🎥 Recommended Video")
    if "video_url" in plan and plan["video_url"]:
        st.video(plan["video_url"])
    else:
        st.info("No video available for today.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous") and st.session_state.current_day > 0:
            st.session_state.current_day -= 1
            st.rerun()
    with col2:
        if st.button("🧹 End Plan"):
            for key in ["devotion_plan", "current_day", "selected_topic", "plan_ready"]:
                st.session_state.pop(key, None)
            st.success("✨ Devotion Plan Ended.")
            st.rerun()
    with col3:
        if st.button("Next ➡️") and st.session_state.current_day < len(st.session_state.devotion_plan) - 1:
            st.session_state.current_day += 1
            st.rerun()

            if st.button("Next ➡️") and st.session_state.current_day < len(st.session_state.devotion_plan) - 1:
                st.session_state.completed_devotions.append({
                    "topic": st.session_state.selected_topic,
                    **plan
                })
                st.success(f"✅ Day {st.session_state.current_day + 1} marked as complete!")
                st.session_state.current_day += 1
                st.rerun()

# --- Prayer ---
elif nav == "🙏 Prayer":
    st.header("🙏 Prayer")
    topic = st.selectbox("Prayer Topic", [
        "Personal Growth", "Healing", "Family/Friends", "Forgiveness", "Finances", "Work/Career", "Something else..."
    ])
    custom_goal = st.text_input("Set a prayer goal (optional)")
    if st.button("Start Prayer"):
        st.markdown("**Let us align your heart in prayer.**")
        prayer = get_prayer(topic)
        for key, val in prayer.items():
            st.subheader(key.capitalize())
            st.write(val)
        if custom_goal:
            st.info(f"Your goal: {custom_goal}")

# --- Meditation ---
elif nav == "🧘 Meditation":
    st.header("🧘 Meditation")
    topic = st.selectbox("Meditation Topic", ["Peace", "God's Presence", "Strength", "Wisdom", "Faith", "Something else..."])
    goal = st.text_input("What do you want to focus on today? (optional)")
    if st.button("Start Meditation"):
        meditation = get_meditation(topic)
        st.subheader("📖 Scripture")
        st.write(meditation["scripture"])
        st.subheader("🧘 Prompt")
        st.write(meditation["prompt"])
        st.subheader("💭 Reflection")
        st.write(meditation["reflection"])
        st.subheader("🫁 Breathing Guide")
        st.write("Inhale 4s → Hold 4s → Exhale 4s")
        if goal:
            st.info(f"Focus Goal: {goal}")
            st.markdown(f"🙏 Let today's meditation center around this goal: **{goal}**")

# --- Accountability ---
elif nav == "🛡️ Accountability":
    st.header("🛡️ Accountability")
    area = st.selectbox("Struggle Area", [
        "Pornography", "Alcohol", "Drugs", "Sex", "Addiction", "Laziness", "Something else..."
    ])
    if st.button("Start Accountability"):
        acc = get_accountability(area)
        for key, val in acc.items():
            st.subheader(key.capitalize())
            st.write(val)
        if st.button("🚨 I need help now!"):
            st.warning("You're not alone. Here's a verse for strength:")
            st.write("📖 1 Corinthians 10:13 — 'God is faithful; He will not let you be tempted beyond what you can bear.'")
            st.info("Reach out to a friend, journal your thoughts, or go for a walk.")

# --- Chat ---
elif nav == "💬 Chat":
    st.header("💬 Chat with DSCPL")

    mic_text = st_javascript("""
        const sleep = (ms) => new Promise(r => setTimeout(r, ms));
        const startSpeech = async () => {
            const recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            return await new Promise((resolve, reject) => {
                recognition.onresult = (event) => {
                    const text = event.results[0][0].transcript;
                    resolve(text);
                };
                recognition.onerror = (event) => {
                    resolve("");
                };
                recognition.start();
            });
        };

        const button = document.createElement("button");
        button.innerText = "🎤";
        button.style = "position:absolute; right:8px; top:4px; padding:4px 10px; font-size:20px;";
        const input = document.querySelector("input[type='text']");
        if (input) {
            input.parentNode.appendChild(button);
            button.onclick = async () => {
                const result = await startSpeech();
                input.value = result;
                input.dispatchEvent(new Event('input', { bubbles: true }));
            };
        }

        await sleep(1000);
        """)

    user_input = st.chat_input("Type your message here or use 🎤")

    if user_input:
        st.chat_message("user", avatar="👩‍💻").markdown(user_input)
        with st.spinner("DSCPL is responding..."):
            reply = ask_llama(user_input, st.session_state.chat_history)
        with st.chat_message("assistant", avatar="✝️"):
         st.markdown(
             f"""
             <div style='background-color: #d7ccc8; padding: 10px; border-radius: 10px; color: #1c1c1c;'>
                 {reply}
             </div>
             """, unsafe_allow_html=True
         )

        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.session_state.last_reply = reply

    if st.session_state.last_reply:
        if st.button("🔊 Speak DSCPL's Response"):
            speak(st.session_state.last_reply)
            st.success("🔊 Speaking now...")

    if st.button("🧹 Clear Conversation"):
        st.session_state.chat_history = [
            {"role": "system", "content": "You are DSCPL, a compassionate, faith-based AI offering scriptural guidance, hope, and spiritual wisdom."}
        ]
        st.session_state.last_reply = ""
        st.rerun()
elif nav == "⏰ Reminders":
    st.header("⏰ Set a Reminder")

    user_id = st.text_input("Enter your name or ID", key="reminder_user")
    reminder_message = st.text_area("Reminder message")
    reminder_time = st.time_input("Select reminder time (24-hr format)")
    formatted_time = reminder_time.strftime("%H:%M")

    if st.button("💾 Save Reminder"):
        if user_id and reminder_message:
            save_reminder(user_id, reminder_message, formatted_time)
            st.success(f"Reminder set for {formatted_time}")
    
            # Google Calendar Integration
            service = authenticate_google_calendar()
            reminder_datetime = datetime.datetime.combine(datetime.date.today(), reminder_time)
            create_event(
                service,
                summary=reminder_message,
                description=f"Reminder for {user_id}",
                start_datetime=reminder_datetime
            )
            st.success("📅 Synced to Google Calendar.")
        else:
            st.error("Please enter both your ID and message.")


    st.markdown("---")
    st.subheader("📋 Your Reminders")
    if user_id:
        reminders = get_user_reminders(user_id)
        if reminders:
            for message, time_str in reminders:
                st.write(f"⏰ **{time_str}** — {message}")
        else:
            st.info("No reminders found for this user.")
# --- Progress Dashboard ---
if nav == "📊 Progress Dashboard":
    st.header("📊 Your Progress")
    if "completed_devotions" in st.session_state and st.session_state.completed_devotions:
        for i, devotion in enumerate(st.session_state.completed_devotions):
            with st.expander(f"Day {i + 1}: {devotion['topic']}"):
                st.markdown(f"**Scripture:** {devotion['scripture']}")
                st.markdown(f"**Prayer:** {devotion['prayer']}")
                st.markdown(f"**Declaration:** {devotion['declaration']}")
                if 'verse' in devotion:
                    st.markdown(f"**Verse:** {devotion['verse']}")
                if 'video_url' in devotion:
                    st.markdown("**Video:**")
                    st.video(devotion['video_url'])
    else:
        st.info("You haven't completed any devotions yet. Start your journey today!")
