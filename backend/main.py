from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any
import datetime

# Import existing logic
from src.data_manager import (
    load_habits, load_logs, add_habit, log_habit_completion, edit_habit, delete_habit,
    get_reminders, add_reminder, update_reminder_status, delete_reminder,
    get_projects, add_project, update_project_status, delete_project,
    get_user_progress, get_backend_name
)
from src.ml_logic import get_smart_suggestions, get_motivational_message
from src.gamification import get_level_info
from src.analytics import calculate_streaks, calculate_completion_rate, get_day_of_week_stats, calculate_missed_habits

app = FastAPI(title="BRAINOVA API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---
class HabitCreate(BaseModel):
    name: str
    category: str
    frequency_type: str
    frequency_value: Optional[str] = None
    target_value: int = 1

class HabitLog(BaseModel):
    date: str
    status: str = "Completed"

class TaskCreate(BaseModel):
    text: str
    description: Optional[str] = ""
    priority: str = "medium"

# --- ROUTES ---

@app.get("/api/info")
def get_info():
    return {"backend": get_backend_name()}

@app.get("/api/progress")
def get_progress():
    progress = get_user_progress()
    curr_lvl, next_lvl = get_level_info(progress['total_xp'])
    return {
        "xp": progress['total_xp'],
        "unlocked_badges": progress.get('unlocked_badges', []),
        "level": curr_lvl,
        "next_level": next_lvl
    }

@app.get("/api/habits")
def api_get_habits(active_only: bool = True):
    df = load_habits(active_only)
    return df.to_dict(orient="records")

@app.post("/api/habits")
def api_add_habit(habit: HabitCreate):
    data = habit.dict()
    if add_habit(data):
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Failed to add habit")

@app.put("/api/habits/{habit_id}")
def api_edit_habit(habit_id: str, habit: HabitCreate):
    if edit_habit(habit_id, habit.dict()):
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Failed to edit habit")

@app.delete("/api/habits/{habit_id}")
def api_delete_habit(habit_id: str):
    if delete_habit(habit_id):
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Failed to delete habit")

@app.post("/api/habits/{habit_id}/log")
def api_log_habit(habit_id: str, log: HabitLog):
    success, reward = log_habit_completion(habit_id, log.date, status=log.status)
    if success:
        return {"status": "success", "reward": reward}
    raise HTTPException(status_code=400, detail="Already logged or failed")

@app.get("/api/logs")
def api_get_logs(days_back: int = 30):
    df = load_logs(days_back)
    return df.to_dict(orient="records")

@app.get("/api/reminders")
def api_get_reminders(pending_only: bool = True):
    df = get_reminders(pending_only)
    return df.to_dict(orient="records")

@app.post("/api/reminders")
def api_add_reminder(task: TaskCreate):
    if add_reminder(task.text, task.priority):
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Failed to add reminder")

@app.put("/api/reminders/{rid}")
def api_update_reminder(rid: str, is_completed: bool):
    if update_reminder_status(rid, is_completed):
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Failed to update reminder")

@app.delete("/api/reminders/{rid}")
def api_delete_reminder(rid: str):
    if delete_reminder(rid):
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Failed to delete")

@app.get("/api/projects")
def api_get_projects(pending_only: bool = True):
    df = get_projects(pending_only)
    return df.to_dict(orient="records")

@app.post("/api/projects")
def api_add_project(task: TaskCreate):
    if add_project(task.text, task.description, task.priority):
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Failed to add project")

@app.put("/api/projects/{pid}")
def api_update_project(pid: str, is_completed: bool):
    if update_project_status(pid, is_completed):
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Failed to update project")

@app.delete("/api/projects/{pid}")
def api_delete_project(pid: str):
    if delete_project(pid):
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Failed to delete")

@app.get("/api/insights")
def api_insights():
    habits = load_habits(active_only=True)
    logs = load_logs(days_back=365)
    suggestions = get_smart_suggestions(habits, logs)
    
    # Calculate best streak for quote
    best_streak = 0
    if not habits.empty and not logs.empty:
        for _, h in habits.iterrows():
            h_logs = logs[logs['habit_id'] == h['id']]
            s = calculate_streaks(h, h_logs)
            best_streak = max(best_streak, s)
            
    quote = get_motivational_message(best_streak)
    
    return {
        "suggestions": suggestions,
        "quote": quote,
        "best_streak": best_streak
    }
