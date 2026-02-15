
**Automated Executive Reporting & Flight-Ops-AI-Briefing**

## 📌 Project Overview

This project is a specialized dashboard designed for Airline Operations Control Centers (OCC). It processes raw flight data (CSV) and leverages the **Gemini 2.5 Flash** model to generate automated, data-driven executive briefings.
Unlike static dashboards, this tool provides context-aware analysis, adjusting its tone and recommendations based on real-time On-Time Performance (OTP) and the severity of flight disruptions.

## ✨ Key Features

* **Adaptive AI Analysis**: Automatically shifts reporting tone (e.g., Stable vs. Critical) based on system-wide OTP thresholds.
* **Deep-Dive into Disruptions**: Specifically identifies and analyzes "Major Delays" (>60 mins) to highlight systemic operational risks.
* **Tactical Directives**: Generates three actionable "Next Steps" for management to mitigate cascading delays and crew duty issues.
* **Dynamic Visualizations**: Integrated Plotly histograms that color-code flight statuses (On-Time, Minor, Major) for instant situational awareness.

## 📁 Project Structure

* `main.py`: Core application logic, Streamlit UI, and Gemini AI integration.
* `test.py`: Validation script for local data processing and metrics.
* `requirements.txt`: List of Python dependencies (Streamlit, Pandas, Plotly, Google Generative AI).
* `.gitignore`: Ensures security by preventing environment variables (`.env`) and virtual environments (`.myenv/`) from being uploaded.

## 🚀 Quick Setup

1. **Clone the Repository**:
```bash
git clone https://github.com/zaidiakram/Flight-Ops-AI-Briefing.git
cd Flight-Ops-AI-Briefing

```
2. **Install Dependencies**:
```bash
pip install -r requirements.txt

```
3. **Configure Environment**:
Create a `.env` file in the root directory and add your API key:
```text
GEMINI_API_KEY=your_actual_api_key_here

```
4. **Launch the Dashboard**:
```bash
streamlit run main.py

``
