# ✨ BRAINOVA

A modern, AI-powered, gamified habit tracking app decoupled into a **React (Vite) Frontend** and a **FastAPI Backend**. Track your progress, earn XP & badges, and stay motivated with smart suggestions.

## 🚀 Architecture
This project is decoupled for high-performance and scalability:
- **Frontend (`/frontend`)**: Built with React & Vite. Deploys natively to Vercel as a static Single Page Application.
- **Backend (`/backend`)**: Built with FastAPI. Deploys effortlessly to Railway or Render via Docker/Nixpacks.

## 🌐 Deployment Instructions

### 1. Backend (Railway)
1. Push this repository to GitHub.
2. Sign in to [Railway](https://railway.app/).
3. Create a **New Project** → **Deploy from GitHub repo**.
4. Select this repository. Set the Root Directory to `/backend` in the deployment settings.
5. Railway will automatically detect the `backend/Procfile` and `backend/railway.json`.
6. Add the following **Environment Variables** in the Railway dashboard:
   - `USE_CLOUD_DB=true`
   - `MONGO_URI=your_mongodb_atlas_connection_string`
   - `APP_PASSWORD=your_optional_bcrypt_hash`
7. Click Deploy. Note your new Railway backend URL (e.g., `https://smart-habit-api.up.railway.app`).

### 2. Frontend (Vercel)
1. Sign in to [Vercel](https://vercel.com/).
2. Create a **New Project** and import this GitHub repository.
3. In the project setup, set the **Root Directory** to `frontend`.
4. The Framework Preset should automatically be detected as **Vite**.
5. Build Command: `npm run build`
6. Output Directory: `dist`
7. **Important**: Add an environment variable `VITE_API_BASE_URL` and set it to your Railway backend URL (e.g., `https://smart-habit-api.up.railway.app`).
8. Click Deploy.

## 🛠️ Local Development

### Running the Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`. You can view the interactive Swagger docs at `http://localhost:8000/docs`.

### Running the Frontend
```bash
cd frontend
npm install
npm run dev
```
The UI will be available at `http://localhost:5173`.

---
Made with ❤️ by Project Maker
