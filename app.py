import streamlit as st
import pandas as pd
import datetime
from src.database import init_db
from src.data_manager import (
    add_project, get_projects, load_habits, load_logs, add_habit, log_habit_completion, delete_habit, edit_habit,
    add_reminder, get_reminders, update_project_status, update_reminder_status, delete_reminder,
    get_backend_name, get_user_progress
)
from src.ui_components import (
    render_add_habit_form, render_habit_card, render_edit_habit_form,
    render_badge_showcase, render_today_progress_ring, render_export_section
)
from src.analytics import render_analytics
from src.ml_logic import get_motivational_message, get_smart_suggestions
from src.utils import is_habit_due
from src.auth import check_password

st.set_page_config(
    page_title="BRAINOVA",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL CSS — Premium Dark Theme
# ============================================================
st.markdown("""
<style>
    /* --- Google Fonts --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* --- Hide Streamlit Defaults --- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* --- Gradient Page Header --- */
    .stAppHeader {
        background: linear-gradient(90deg, #0E1117 0%, #1a1a2e 50%, #0E1117 100%) !important;
    }

    /* --- Sidebar Branding --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E1117 0%, #1a1a2e 100%);
        border-right: 1px solid #262730;
    }

    /* --- Custom Navbar (Radio Buttons) --- */
    div[role="radiogroup"] {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        background: linear-gradient(135deg, #0E1117 0%, #1a1a2e 100%);
        padding: 12px 16px;
        margin-bottom: 24px;
        border-bottom: 1px solid #262730;
        border-radius: 0 0 16px 16px;
    }
    div[role="radiogroup"] label {
        background: rgba(38, 39, 48, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 12px 22px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        margin: 4px !important;
        flex-grow: 1;
        text-align: center;
        min-width: 130px;
    }
    div[data-testid="stRadio"] label:hover {
        background: rgba(246, 51, 102, 0.12);
        border-color: rgba(246, 51, 102, 0.3);
        transform: translateY(-1px);
    }
    div[role="radiogroup"] > label[data-checked="true"] {
        background: linear-gradient(135deg, #F63366 0%, #FF6B6B 100%);
        color: white !important;
        border: none;
        box-shadow: 0 4px 20px rgba(246, 51, 102, 0.35);
    }

    /* --- Cards / Containers --- */
    [data-testid="stVerticalBlock"] > div[data-testid="stExpander"],
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 4px 24px rgba(246, 51, 102, 0.08);
        transform: translateY(-1px);
    }

    /* --- Glassmorphism Metric Cards --- */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.8) 0%, rgba(22, 33, 62, 0.8) 100%);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(246, 51, 102, 0.15);
        border-radius: 14px;
        padding: 18px 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: rgba(246, 51, 102, 0.35);
        box-shadow: 0 6px 28px rgba(246, 51, 102, 0.12);
    }
    [data-testid="stMetricLabel"] {
        color: #aaa !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    [data-testid="stMetricValue"] {
        color: #F63366 !important;
        font-weight: 700 !important;
    }

    /* --- Progress Bar Glow --- */
    [data-testid="stProgress"] > div > div > div {
        background: linear-gradient(90deg, #F63366 0%, #FF6B6B 50%, #FFD600 100%) !important;
        border-radius: 10px;
        box-shadow: 0 0 12px rgba(246, 51, 102, 0.4);
        animation: progressGlow 2s ease-in-out infinite alternate;
    }
    @keyframes progressGlow {
        from { box-shadow: 0 0 8px rgba(246, 51, 102, 0.3); }
        to { box-shadow: 0 0 20px rgba(246, 51, 102, 0.6); }
    }

    /* --- Buttons --- */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(246, 51, 102, 0.2) !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #F63366 0%, #FF6B6B 100%) !important;
        color: white !important;
        border: none !important;
    }

    /* --- Download Buttons --- */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
        border: 1px solid #F63366 !important;
        border-radius: 10px !important;
        color: #F63366 !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #F63366 0%, #FF6B6B 100%) !important;
        color: white !important;
        transform: translateY(-1px) !important;
    }

    /* --- Tabs --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(38, 39, 48, 0.5);
        border-radius: 10px;
        padding: 8px 18px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #F63366 0%, #FF6B6B 100%) !important;
        color: white !important;
        border: none !important;
    }

    /* --- Dividers --- */
    hr {
        border-color: rgba(246, 51, 102, 0.12) !important;
    }

    /* --- Selectbox / Input --- */
    [data-testid="stSelectbox"] > div > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        transition: border-color 0.3s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #F63366 !important;
        box-shadow: 0 0 8px rgba(246, 51, 102, 0.2) !important;
    }

    /* --- Data Tables --- */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* --- Toast Notifications --- */
    [data-testid="stToast"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
        border: 1px solid #F63366 !important;
        border-radius: 12px !important;
    }

    /* --- Custom Footer --- */
    .custom-footer {
        text-align: center;
        padding: 24px;
        margin-top: 40px;
        color: #555;
        font-size: 0.8rem;
        border-top: 1px solid #262730;
    }
    .custom-footer a {
        color: #F63366;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# AUTHENTICATION GATE
# ============================================================
if not check_password():
    st.stop()

# ============================================================
# APP TITLE
# ============================================================
st.markdown("""
<div style='text-align:center; padding: 10px 0 5px 0;'>
    <h1 style='background: linear-gradient(135deg, #F63366 0%, #FF6B6B 50%, #FFD600 100%);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               font-size: 2.5rem; font-weight: 800; margin-bottom: 0;'>
        ✨ BRAINOVA
    </h1>
    <p style='color:#888; font-size:0.95rem; margin-top:4px;'>Build better habits, one day at a time</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# DB INITIALIZATION
# ============================================================
if "db_initialized" not in st.session_state:
    if init_db():
        st.session_state.db_initialized = True
    else:
        st.error("Failed to initialize database. Please check your configuration.")
        st.stop()

# ============================================================
# NAVIGATION
# ============================================================
selected_tab = st.radio(
    "Navigation", 
    ["🔥 Dashboard", "➕ Add Habit", "📝 Add Reminder", "🗂️ Add Project", "📊 Analytics", "⚙️ Settings"], 
    horizontal=True,
    label_visibility="collapsed"
)

# ============================================================
from src.gamification import get_level_info

# ============================================================
# 🔥 DASHBOARD
# ============================================================
if selected_tab == "🔥 Dashboard":
    
    # --- GAMIFICATION HEADER ---
    user_progress = get_user_progress()
    curr_lvl, next_lvl = get_level_info(user_progress['total_xp'])
    
    # Calculate Progress %
    if next_lvl:
        needed = next_lvl['xp_required'] - curr_lvl['xp_required']
        current = user_progress['total_xp'] - curr_lvl['xp_required']
        progress_val = min(1.0, max(0.0, current / needed)) if needed > 0 else 1.0
        str_progress = f"{user_progress['total_xp']} / {next_lvl['xp_required']} XP"
    else:
        progress_val = 1.0
        str_progress = "Max Level Reached! 👑"

    # Level + XP Bar
    with st.container(border=True):
        c1, c2 = st.columns([1, 4])
        with c1:
            st.metric("Level", f"{curr_lvl['level']}", curr_lvl['name'])
        with c2:
            st.write(f"**XP Progress** ({str_progress})")
            st.progress(progress_val)
    
    # --- BADGES SHOWCASE ---
    unlocked_badges = user_progress.get('unlocked_badges', [])
    render_badge_showcase(unlocked_badges)
    
    st.divider()

    # --- REWARD POPUP SYSTEM ---
    if "latest_reward" in st.session_state:
        reward = st.session_state.latest_reward
        xp = reward.get('xp_earned', 0)
        st.toast(f"Heroic! +{xp} XP 🌟")
        
        if reward.get('level_up'):
            st.balloons()
            lvl = reward['current_level']
            st.success(f"🎉 **LEVEL UP!** You are now a **{lvl['name']}** (Level {lvl['level']})!")
        
        new_badges = reward.get('new_badges', [])
        if new_badges:
            from src.gamification import BADGES
            for b in new_badges:
                badge = BADGES.get(b, {})
                st.success(f"🏅 **Badge Unlocked:** {badge.get('icon', '')} {badge.get('name', b)} — {badge.get('desc', '')}")
            
        del st.session_state['latest_reward']

    # --- TODAY'S OVERVIEW (Progress Ring + Motivational Quote) ---
    habits = load_habits(active_only=True)
    logs = load_logs()
    
    today = pd.Timestamp.now()
    today_str = today.strftime("%Y-%m-%d")
    
    # Calculate today's stats
    todays_habits = []
    for _, habit in habits.iterrows() if not habits.empty else []:
        if is_habit_due(habit, today):
            todays_habits.append(habit)
    
    total_today = len(todays_habits)
    completed_today = 0
    if total_today > 0 and not logs.empty:
        completed_ids = logs[logs['date'].astype(str) == today_str]['habit_id'].unique()
        completed_today = sum(1 for h in todays_habits if h['id'] in completed_ids)
    
    col_ring, col_quote = st.columns([1, 2])
    with col_ring:
        render_today_progress_ring(completed_today, total_today)
    with col_quote:
        # Find best current streak for motivational message
        best_streak = 0
        if not habits.empty and not logs.empty:
            from src.analytics import calculate_streaks
            for _, h in habits.iterrows():
                h_logs = logs[logs['habit_id'] == h['id']]
                s = calculate_streaks(h, h_logs)
                best_streak = max(best_streak, s)
        
        msg = get_motivational_message(best_streak)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                    padding: 24px; border-radius: 14px; border: 1px solid rgba(246,51,102,0.15);
                    margin-top: 10px;'>
            <p style='font-size: 1.4rem; margin-bottom: 8px;'>💬</p>
            <p style='font-size: 1.1rem; color: #ddd; font-style: italic; margin: 0;'>{msg}</p>
            <p style='color: #666; font-size: 0.8rem; margin-top: 12px;'>🔥 Best streak: {best_streak} days</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()

    # --- PROJECTS SECTION ---
    projects = get_projects(pending_only=True)
    if not projects.empty:
        st.markdown("### 🗂️ Pending Projects")
        for idx, row in projects.iterrows():
            icon = "🚨" if row['priority'] == 'high' else "⚠️" if row['priority'] == 'medium' else "🟢"
            
            with st.container(border=True):
                c1, c2 = st.columns([6, 1])
                with c1:
                    st.markdown(f" <b style='font-size: 1.5rem;'>{icon} {row['text']}</b>", unsafe_allow_html=True)
                    if row.get('description'):
                        st.caption(row['description'])
                with c2:
                    if st.button("Done", key=f"dash_project_{row['id']}", help="Mark Done"):
                        update_project_status(row['id'], True)
                        st.rerun()

    # --- REMINDERS SECTION ---
    reminders = get_reminders(pending_only=True)
    if not reminders.empty:
        st.markdown("### 📝 Reminders")
        for idx, row in reminders.iterrows():
            icon = "🚨" if row['priority'] == 'high' else "⚠️" if row['priority'] == 'medium' else "🟢"
            
            with st.container(border=True):
                c1, c2 = st.columns([6, 1])
                with c1:
                    st.markdown(f" <b style='font-size: 1.5rem;'>{icon} {row['text']}</b>", unsafe_allow_html=True)
                with c2:
                    if st.button("Done", key=f"dash_rem_{row['id']}", help="Mark Done"):
                        update_reminder_status(row['id'], True)
                        st.rerun()

    # --- HABITS SECTION ---
    st.markdown("### 🎯 Today's Focus")
    
    # 🧠 Smart Suggestions
    suggestions = get_smart_suggestions(habits, logs)
    if suggestions:
        for suggestion in suggestions[:3]:  # Show top 3 suggestions
            st.info(suggestion)
    
    if habits.empty:
        st.info("No habits found. Go to '➕ Add Habit' to start your journey!")
    else:
        todays_habits_df = pd.DataFrame(todays_habits)

        # Filter out completed habits
        if not todays_habits_df.empty:
            pending_habits = todays_habits_df
            if not logs.empty:
                completed_ids = logs[logs['date'].astype(str) == today_str]['habit_id'].unique()
                pending_habits = todays_habits_df[~todays_habits_df['id'].isin(completed_ids)]
            
            if pending_habits.empty:
                st.balloons()
                st.success("🎉 All habits completed for today! You are crushing it!")
            else:
                for index, habit in pending_habits.iterrows():
                    render_habit_card(habit, logs, log_habit_completion)
        else:
            st.write("No habits scheduled for today. Enjoy your free time! 🏖️")

# ============================================================
# ➕ ADD HABIT
# ============================================================
elif selected_tab == "➕ Add Habit":
    st.write("### ✨ Create New Habit")
    
    if "habit_success" in st.session_state:
        st.success(st.session_state.habit_success)
        del st.session_state["habit_success"]
        
    habit_data = render_add_habit_form()
    if habit_data:
        if add_habit(habit_data):
            st.session_state.habit_success = f"Habit '{habit_data['name']}' created successfully! 🚀"
            st.rerun()
        else:
            st.error("Failed to save habit. Please try again.")

# ============================================================
# 📝 ADD REMINDER
# ============================================================
elif selected_tab == "📝 Add Reminder":
    st.write("### 🧠 Sticky Reminders")
    st.caption("A place for non-habit tasks like 'Call Mom' or 'Pay Bills'")
    
    # Callback for adding reminder safely
    def add_reminder_callback():
        text = st.session_state.get("rem_input", "").strip()
        priority = st.session_state.get("rem_priority", "Medium")
        
        if text:
            if add_reminder(text, priority.lower()):
                st.toast("Reminder added successfully! 🚀")
                st.session_state.rem_input = "" # Clear input safely
            else:
                st.error("Failed to add reminder.")

    if "rem_input" not in st.session_state: st.session_state.rem_input = ""
    
    st.text_input("New Reminder", label_visibility="collapsed", placeholder="What needs to be done?", key="rem_input")

    c1, c2 = st.columns([3, 1], gap="large")
    with c1:
        st.selectbox("Priority", ["High", "Medium", "Low"], label_visibility="collapsed", index=1, key="rem_priority")
    with c2:
        st.button("Add Reminder", on_click=add_reminder_callback)

    st.divider()
    
    # List Reminders
    reminders = get_reminders(pending_only=True)
    if reminders.empty:
        st.info("No active reminders. You're free! 🎉")
    else:
        st.subheader("⚠️ Pending Reminders")
        for idx, row in reminders.iterrows():
            icon = "🚨" if row['priority'] == 'high' else "⚠️" if row['priority'] == 'medium' else "🟢"
            
            with st.container(border=True):
                c1, c2 = st.columns([6, 1])
                with c1:
                    st.markdown(f"**{icon} {row['text']}**")
                with c2:
                    if st.button("Done", key=f"rem_list_{row['id']}", help="Mark Done"):
                        update_reminder_status(row['id'], True)
                        st.rerun()
        st.divider()

# ============================================================
# 🗂️ ADD PROJECT
# ============================================================
elif selected_tab == "🗂️ Add Project":
    st.write("### 🗂️ Add Projects")
    st.caption("A place to track larger tasks (projects) or goals.")
    
    def add_project_callback():
        title = st.session_state.get("proj_title", "").strip()
        desc = st.session_state.get("proj_desc", "").strip()
        priority = st.session_state.get("proj_priority", "Medium")
        
        if title:
            if add_project(title, desc, priority.lower()):
                st.toast("Project added successfully! 🚀")
                st.session_state.proj_title = ""
                st.session_state.proj_desc = ""
            else:
                st.error("Failed to add project.")
        else:
            st.warning("Project title is required.")

    if "proj_title" not in st.session_state: st.session_state.proj_title = ""
    if "proj_desc" not in st.session_state: st.session_state.proj_desc = ""

    st.text_input("On which project do you wish to work?", placeholder="e.g. BRAINOVA", key="proj_title")
    
    c1, c2 = st.columns([3, 2])
    with c1:
        st.text_input("Description", placeholder="Add a brief description (optional)", key="proj_desc")
    with c2:
        st.selectbox("Priority", ["High", "Medium", "Low"], index=1, key="proj_priority")

    st.button("Add Project", on_click=add_project_callback)
        
    st.divider()
    
    # List Projects
    projects = get_projects(pending_only=True)
    if projects.empty:
        st.info("No active Projects. You're free! 🎉")
    else:
        st.subheader("⚠️ Pending Projects")
        for idx, row in projects.iterrows():
            p_emoji = "🟥" if row['priority'] == 'high' else "🟨" if row['priority'] == 'medium' else "🟩"
            
            with st.container(border=True):
                rc1, rc2 = st.columns([6, 1])
                
                with rc1:
                    st.markdown(f"**{p_emoji} {row['text']}**")
                    if row['description']:
                        st.caption(row['description'])
                with rc2:
                    if st.button("Done", key=f"project_done_{row['id']}", help="Mark as Done"):
                        update_project_status(row['id'], True)
                        st.rerun()
            st.divider()

# ============================================================
# 📊 ANALYTICS
# ============================================================
elif selected_tab == "📊 Analytics":
    habits = load_habits()
    logs = load_logs()
    render_analytics(habits, logs)

# ============================================================
# ⚙️ SETTINGS
# ============================================================
elif selected_tab == "⚙️ Settings":
    st.header("⚙️ Habit Management Center")
    st.caption("Manage your data, clear old tasks, and organize your workspace.")
    
    # Sub-tabs
    tab_habits, tab_reminders, tab_projects, tab_data = st.tabs(["✨ Habits", "📝 Reminders", "🗂️ Projects", "🔧 Data & Info"])
    
    # --- HABITS MANAGEMENT ---
    with tab_habits:
        habits = load_habits()
        if "edit_mode_id" not in st.session_state:
            st.session_state.edit_mode_id = None

        if habits.empty:
            st.info("No habits to manage yet.")
        else:
            # Edit Mode Logic
            if st.session_state.edit_mode_id:
                habit_to_edit = habits[habits['id'] == st.session_state.edit_mode_id].iloc[0]
                
                if st.button("← Back to List", key="back_edit"):
                    st.session_state.edit_mode_id = None
                    st.rerun()
                    
                updated_data = render_edit_habit_form(habit_to_edit['id'], habit_to_edit)
                
                if updated_data:
                    if edit_habit(habit_to_edit['id'], updated_data):
                        st.success("Habit updated successfully!")
                        st.session_state.edit_mode_id = None
                        st.rerun()
                    else:
                        st.error("Failed to update habit.")
            else:
                # List Mode
                for index, habit in habits.iterrows():
                    with st.container(border=True):
                        c1, c2 = st.columns([4, 1])
                        with c1:
                            st.markdown(f"**{habit['name']}**")
                            st.caption(f"{habit['category']} • {habit['frequency_type']}")
                        with c2:
                            b1, b2 = st.columns(2)
                            with b1:
                                if st.button("✏️", key=f"edit_{habit['id']}", help="Edit Habit"):
                                    st.session_state.edit_mode_id = habit['id']
                                    st.rerun()
                            with b2:
                                if st.button("🗑️", key=f"del_{habit['id']}", help="Delete Habit"):
                                    if delete_habit(habit['id']):
                                        st.success("Deleted!")
                                        st.rerun()

    # --- REMINDERS MANAGEMENT ---
    with tab_reminders:
        reminders = get_reminders(pending_only=False)
        if reminders.empty:
            st.info("No reminders found.")
        else:
            for index, row in reminders.iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([5, 1])
                    with c1:
                        is_done = row['is_completed'] == 1
                        status = "✅" if is_done else "⏳"
                        priority_icon = "🚨" if row['priority'] == 'high' else "⚠️" if row['priority'] == 'medium' else "🟢"
                        
                        st.markdown(f"**{priority_icon} {row['text']}**")
                        st.caption(f"Status: {status} • {'Completed' if is_done else 'Pending'}")
                        
                    with c2:
                        st.write("") # Align
                        if st.button("🗑️", key=f"del_rem_{row['id']}", help="Delete Reminder"):
                            if delete_reminder(row['id']):
                                st.rerun()

    # --- PROJECTS MANAGEMENT ---
    with tab_projects:
        from src.data_manager import delete_project
        projects = get_projects(pending_only=False)
        if projects.empty:
            st.info("No projects found.")
        else:
            for index, row in projects.iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([5, 1])
                    with c1:
                        is_done = row['is_completed'] == 1
                        status = "✅" if is_done else "⏳"
                        p_emoji = "🟥" if row['priority'] == 'high' else "🟨" if row['priority'] == 'medium' else "🟩"
                        
                        st.markdown(f"**{p_emoji} {row['text']}**")
                        if row['description']:
                            st.caption(row['description'])
                        st.caption(f"Status: {status}")
                        
                    with c2:
                        st.write("")
                        if st.button("🗑️", key=f"del_proj_{row['id']}", help="Delete Project"):
                            if delete_project(row['id']):
                                st.rerun()

    # --- DATA & INFO TAB ---
    with tab_data:
        # Database Info
        st.markdown("### 💾 Database Info")
        with st.container(border=True):
            info_c1, info_c2, info_c3 = st.columns(3)
            with info_c1:
                st.metric("Backend", get_backend_name())
            with info_c2:
                user_progress = get_user_progress()
                st.metric("Total XP", user_progress['total_xp'])
            with info_c3:
                st.metric("Badges Unlocked", len(user_progress.get('unlocked_badges', [])))
        
        st.divider()
        
        # Export Section
        render_export_section()
        
        st.divider()
        
        # Reset Progress
        st.markdown("### 🔄 Reset Progress")
        st.warning("This will reset your XP and badges to zero. Your habits and logs will NOT be affected.")
        
        if st.button("🗑️ Reset XP & Badges", type="secondary"):
            st.session_state.confirm_reset = True
        
        if st.session_state.get("confirm_reset", False):
            st.error("⚠️ Are you sure? This action cannot be undone!")
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("Yes, Reset Everything", type="primary"):
                    from src.data_manager import update_user_progress
                    # Reset by setting XP to negative of current to zero it out
                    curr = get_user_progress()
                    from src.database import run_query
                    import json
                    run_query(
                        "UPDATE user_progress SET total_xp = 0, unlocked_badges = '[]' WHERE id = 1",
                    )
                    st.session_state.confirm_reset = False
                    st.success("Progress has been reset! 🔄")
                    st.rerun()
            with col_no:
                if st.button("Cancel"):
                    st.session_state.confirm_reset = False
                    st.rerun()

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class='custom-footer'>
    <p>✨ BRAINOVA — Built with ❤️ using Streamlit</p>
    <p>Track habits • Build streaks • Level up</p>
</div>
""", unsafe_allow_html=True)
