# 🎯 GoalGuider – Personalized Career Roadmap & Streak System

**GoalGuider** is an AI-powered career guidance platform that helps users move from their current skill level to a target career role through a structured roadmap and actionable daily tasks.

Instead of showing long learning paths or generic courses, GoalGuider generates a **personalized roadmap with step-by-step tasks** using AI. Users focus on **one task at a time**, track progress, and maintain a streak while advancing toward their career goals.

---

# 🚀 Features

### 🤖 AI-Generated Career Roadmaps

* Generates **10–14 structured roadmap steps**
* Each step includes **10–12 actionable tasks**
* Adapts to the user's **current level and career goal**

### ✅ Smart Task System

Tasks are automatically divided into three categories:

| Section             | Description                           |
| ------------------- | ------------------------------------- |
| **Present Task**    | Only one task shown to maintain focus |
| **Upcoming Tasks**  | Remaining tasks shown in batches of 5 |
| **Completed Tasks** | Finished tasks stored separately      |

This reduces cognitive overload and helps users stay productive.

### 🔥 Streak Tracking

* Tracks daily consistency
* Motivates users to maintain learning momentum

### 👤 User Profiles

Users can store:

* Current skill level
* Career goal
* Personalized roadmap history

### 📋 Interactive Task Interface

* Dropdown sections for task categories
* Progressive task loading (`+5 more >>`)
* Minimalist focus-driven UI

---

# 🏗️ Tech Stack

### Frontend

* HTML
* CSS
* Vanilla JavaScript

### Backend

* Django
* Django REST Framework

### AI Integration

* Google **Gemini API**

### Database

* SQLite (development)

---

# 📂 Project Structure

```
goalguider/
│
├── backend/
│   ├── roadmap/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── ai_service.py
│   │
│   ├── tasks/
│   │   ├── models.py
│   │
│   ├── profiles/
│   │   ├── models.py
│
├── frontend/
│   ├── roadmap.html
│   ├── tasks.html
│   ├── profile.html
│
├── js/
│   ├── tasks.js
│   ├── utils.js
│   ├── config.js
│
└── css/
    ├── style.css
    ├── nav.css
```

---

# 🧠 How It Works

### 1️⃣ User Input

The user provides:

* Current status
* Career goal

Example:

```
Current Status: Intermediate Python Developer
Career Goal: Software Engineer
```

---

### 2️⃣ AI Roadmap Generation

Gemini generates a structured roadmap:

```
Step 1 → Core Programming Refinement  
Step 2 → Data Structures & Algorithms  
Step 3 → Backend Development  
Step 4 → System Design  
...
```

Each step contains **10+ actionable tasks**.

---

### 3️⃣ Backend Processing

The backend:

1. Calls the AI API
2. Parses the JSON roadmap
3. Saves:

   * Roadmap
   * Steps
   * Tasks

---

### 4️⃣ Task UI Logic

Tasks are categorized dynamically:

```
Present Task
   ↓
Upcoming Tasks
   ↓
Completed Tasks
```

Only **one active task** is shown to keep the user focused.

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/goalguider.git
cd goalguider
```

---

## 2️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

---

## 3️⃣ Environment Variables

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

---

## 4️⃣ Run Database Migrations

```bash
python manage.py migrate
```

---

## 5️⃣ Start Server

```bash
python manage.py runserver
```

Server will run at:

```
http://127.0.0.1:8000
```

---

# 📡 API Endpoints

### Generate Roadmap

```
POST /api/roadmap/generate/
```

Body:

```json
{
  "current_status": "Intermediate programmer",
  "career_goal": "Software Engineer"
}
```

---

### Get Roadmap

```
GET /api/roadmap/
```

---

### Fetch Tasks

```
GET /api/tasks/
```

---

# 🎯 Design Philosophy

GoalGuider follows three core principles:

### Focus

Users should only focus on **one task at a time**.

### Progress Visibility

Roadmaps are broken into **small achievable steps**.

### AI-Guided Learning

Roadmaps adapt dynamically to the user's career goal.

---

# 📈 Future Improvements

Planned features include:

* AI progress feedback
* Skill gap analysis
* Adaptive difficulty
* Daily task scheduling
* Analytics dashboard
* Mobile responsive UI
* Gamified achievements

---

# 👨‍💻 Author

**Krishna J.G**

GoalGuider is designed to make career growth structured, focused, and AI-assisted.

---

# ⭐ Project Vision

> Helping people grow their careers **one focused step at a time.**

