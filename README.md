# AI Interview System — Intelligent Skill Assessment
An AI-powered interview platform built with Streamlit and Groq AI (LLaMA 3.3).

## Live Demo
https://ai-interview-bot-fwjbffaqzcqzrdbfki4v2n.streamlit.app

## Features
- AI question generation based on domain and difficulty
- Intelligent answer evaluation with skill scoring
- Auto difficulty adjustment based on performance
- Interview timer with auto-submit on timeout
- Multiple interview rounds (Technical, HR, System Design)
- Resume upload and personalized interview generation
- PDF report download with skill breakdown
- Leaderboard with candidate rankings
- Proctoring system with tab switch detection
- Admin panel to view all interviews

## Tech Stack
Python · Streamlit · Groq AI · LLaMA 3.3 · SQLite · Plotly · ReportLab · PyMuPDF

## Project Structure

AI INTERVIEW BOT/
├── app.py                  # Main entry point
├── groq_service.py         # AI question generation and evaluation
├── skill_evaluator.py      # Skill scoring logic
├── pdf_report.py           # PDF report generation
├── resume_parser.py        # Resume PDF extraction
├── db.py                   # Database operations
├── config.py               # Configuration settings
└── pages/
    ├── home.py             # Home dashboard
    ├── interview.py        # Live interview room with timer
    ├── results.py          # Score and feedback
    ├── resume.py           # Resume upload and analysis
    ├── rounds.py           # Interview rounds selection
    ├── leaderboard.py      # Candidate rankings
    └── proctor.py          # Proctoring system


## Setup Instructions
1. Clone the repository
   git clone https://github.com/prachiagg22/AI-INTERVIEW-SYSTEM.git

2. Create virtual environment
   python -m venv myenv
   myenv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Add your Groq API key to `.env` file

   GEMINI_API_KEY=your_groq_api_key_here

   Get free key at: https://console.groq.com

5. Run the app
   streamlit run app.py


## Pages
- **Home** — Dashboard with interview stats
- **Interview** — Live AI interview with timer
- **Results** — Detailed score report with radar chart
- **Resume** — Upload resume for personalized interview
- **Rounds** — Choose Technical, HR or System Design round
- **Leaderboard** — Top candidates ranking
- **Proctor** — Proctored interview mode
- **Admin** — View all interview records

## Developer
- Name: Prachi Aggarwal
- Project: 8th Semester Major Project
- Domain: Artificial Intelligence & Data Science