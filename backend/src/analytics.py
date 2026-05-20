import pandas as pd
from datetime import timedelta
from src.utils import is_habit_due

def calculate_streaks(habit, habit_logs):
    """
    Calculate current streak based on 'Consecutive Due Dates Completed'.
    """
    if habit_logs.empty:
        return 0
    
    today = pd.Timestamp.now().date()
    try:
        created_at = pd.to_datetime(habit['created_at']).date()
    except:
        return 0
        
    if created_at > today: return 0

    # Get all dates where habit was due, up to today
    due_dates = []
    curr = created_at
    while curr <= today:
        if is_habit_due(habit, curr):
            due_dates.append(curr)
        curr += timedelta(days=1)
        
    if not due_dates: return 0
    
    due_dates.sort(reverse=True)
    logged_dates = set(pd.to_datetime(habit_logs['date']).dt.date)
    
    streak = 0
    for d in due_dates:
        if d in logged_dates:
            streak += 1
        else:
            if d == today:
                continue
            else:
                break
    return streak

def calculate_completion_rate(habit, habit_logs):
    """
    Calculate completion percentage: (Days Completed / Days Due) * 100
    """
    today = pd.Timestamp.now().date()
    try:
        created_at = pd.to_datetime(habit['created_at']).date()
    except:
        return 0.0, 0
    
    if created_at > today: return 0.0, 0
    
    total_due = 0
    curr = created_at
    while curr <= today:
        if is_habit_due(habit, curr):
            total_due += 1
        curr += timedelta(days=1)
        
    completed_count = len(habit_logs['date'].unique()) 
    
    if total_due == 0: return 0.0, 0
    pct = min(100.0, (completed_count / total_due) * 100)
    return pct, total_due

def calculate_missed_habits(habits, logs, days=30):
    """
    Identify habits missed most frequently in the last X days.
    """
    today = pd.Timestamp.now().date()
    start_date = today - timedelta(days=days)
    
    missed_data = []
    
    for _, habit in habits.iterrows():
        missed_count = 0
        total_due = 0
        
        # Determine habit start (cannot miss before created)
        try:
            h_created = pd.to_datetime(habit['created_at']).date()
        except:
            h_created = start_date
            
        check_start = max(start_date, h_created)
        
        # Iterate days
        curr = check_start
        habit_logs = logs[logs['habit_id'] == habit['id']]
        logged_dates = set(pd.to_datetime(habit_logs['date']).dt.date) if not habit_logs.empty else set()
        
        while curr < today: # Don't count today as missed yet
            if is_habit_due(habit, curr):
                total_due += 1
                if curr not in logged_dates:
                    missed_count += 1
            curr += timedelta(days=1)
            
        if missed_count > 0:
            missed_data.append({
                "Habit": habit['name'],
                "Missed": missed_count,
                "Total Due": total_due,
                "Miss Rate": (missed_count/total_due*100) if total_due > 0 else 0
            })
            
    df = pd.DataFrame(missed_data)
    if "Missed" in df.columns:
        return df.sort_values("Missed", ascending=False)
    return df

def get_day_of_week_stats(logs):
    """
    Return total completions by day of week (Mon=0, Sun=6).
    """
    if logs.empty:
        return pd.DataFrame()
        
    df = logs.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['day_name'] = df['date'].dt.day_name()
    # Ensure correct order
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    stats = df['day_name'].value_counts().reindex(days_order, fill_value=0).reset_index()
    stats.columns = ['Day', 'Completions']
    return stats


