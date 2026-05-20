import pandas as pd
import random
import datetime

def get_motivational_message(streak):
    """Return a message based on streak length."""
    if streak == 0:
        return random.choice([
            "Every journey begins with a single step. Start today!",
            "Don't worry about yesterday. Today is a new opportunity.",
            "Small progress is still progress."
        ])
    elif streak < 3:
        return random.choice([
            "You're off to a great start! Keep it up!",
            "Consistency is key. You're building momentum.",
            "Great job! Two days in a row!"
        ])
    elif streak < 7:
        return random.choice([
            "You're on fire! 🔥",
            "Almost a full week! Don't break the chain!",
            "You are becoming unstoppable."
        ])
    else:
        return random.choice([
            "Legendary streak! 🏆",
            "This habit is now part of you.",
            "Incredible dedication. Use this energy for other goals too!"
        ])

def get_streak_for_habit(habit_id, logs):
    """Calculate a simplified streak for a specific habit.
    
    Counts consecutive days backward from yesterday where logs
    has an entry for that habit_id.
    """
    if logs.empty:
        return 0

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    # Get all unique dates for this habit
    habit_logs = logs[logs['habit_id'] == habit_id].copy()
    if habit_logs.empty:
        return 0

    habit_logs['date_parsed'] = pd.to_datetime(habit_logs['date']).dt.date
    logged_dates = set(habit_logs['date_parsed'])

    streak = 0
    check_date = yesterday
    while check_date in logged_dates:
        streak += 1
        check_date -= datetime.timedelta(days=1)

    return streak

def get_smart_suggestions(habits, logs):
    """
    Analyze logs to find patterns and suggest improvements.
    Returns a list of insight strings.
    """
    if logs.empty or habits.empty:
        return ["Start logging your habits to get smart insights!"]

    suggestions = []

    # Work with a copy to avoid modifying the original
    logs_copy = logs.copy()
    logs_copy['date'] = pd.to_datetime(logs_copy['date'])
    logs_copy['weekday'] = logs_copy['date'].dt.day_name()

    # --- 1. Best day analysis ---
    weekday_counts = logs_copy['weekday'].value_counts()
    if not weekday_counts.empty:
        best_day = weekday_counts.idxmax()
        suggestions.append(f"💡 You happen to be most consistent on **{best_day}s**. Try to schedule your hardest tasks then!")

    # --- 2. Unstarted habit nudge ---
    for _, habit in habits.iterrows():
        habit_logs = logs_copy[logs_copy['habit_id'] == habit['id']]
        if habit_logs.empty:
            suggestions.append(f"👀 You haven't started **{habit['name']}** yet. How about doing just 5 minutes today?")

    # --- 3. Completion trend (this week vs last week) ---
    today = pd.Timestamp(datetime.date.today())
    # Start of this week (Monday)
    this_week_start = today - pd.Timedelta(days=today.weekday())
    last_week_start = this_week_start - pd.Timedelta(days=7)

    this_week_logs = logs_copy[(logs_copy['date'] >= this_week_start) & (logs_copy['date'] < this_week_start + pd.Timedelta(days=7))]
    last_week_logs = logs_copy[(logs_copy['date'] >= last_week_start) & (logs_copy['date'] < this_week_start)]

    this_week_count = len(this_week_logs)
    last_week_count = len(last_week_logs)

    if last_week_count > 0:
        pct_change = round(((this_week_count - last_week_count) / last_week_count) * 100)
        if pct_change > 0:
            suggestions.append(f"📈 Your completion rate improved by {pct_change}% this week vs last week! Keep it up!")
        elif pct_change < 0:
            suggestions.append(f"📉 Your completions dropped {abs(pct_change)}% this week. Let's bounce back!")

    # --- 4. Streak-at-risk alert ---
    today_date = datetime.date.today()
    today_str_variants = [str(today_date)]  # for matching

    for _, habit in habits.iterrows():
        habit_id = habit['id']
        streak = get_streak_for_habit(habit_id, logs)

        if streak >= 3:
            # Check if habit is due today but not yet completed
            today_logs = logs_copy[
                (logs_copy['habit_id'] == habit_id) &
                (logs_copy['date'].dt.date == today_date)
            ]
            if today_logs.empty:
                suggestions.append(
                    f"⚡ Your **{habit['name']}** streak of {streak} days is at risk! Don't break the chain today."
                )

    # --- 5. Neglected habit (7+ days since last log) ---
    for _, habit in habits.iterrows():
        habit_id = habit['id']
        habit_logs = logs_copy[logs_copy['habit_id'] == habit_id]
        if not habit_logs.empty:
            last_log_date = habit_logs['date'].max().date()
            days_since = (today_date - last_log_date).days
            if days_since >= 7:
                suggestions.append(
                    f"🔕 You haven't done **{habit['name']}** in {days_since} days. Try just 2 minutes today to restart."
                )

    if not suggestions:
        suggestions.append("🌟 You are doing great! Keep tracking to unlock more insights.")

    return suggestions
