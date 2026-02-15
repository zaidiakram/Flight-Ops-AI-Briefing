from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
from google import genai  


st.set_page_config(
    page_title="Flight Data Reporting Automation",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")


st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(10, 20, 30, 0.85), rgba(10, 20, 30, 0.85)), 
        url('https://images.unsplash.com/photo-1436491865332-7a61a109cc05?q=80&w=2074&auto=format&fit=crop');
        background-size: cover;
        background-attachment: fixed;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(20, 30, 40, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    [data-testid="stSidebar"] * { color: #E0E0E0 !important; }

    div[data-testid="stMetric"], div.stDataFrame {
        background-color: rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px; border-radius: 12px; backdrop-filter: blur(10px);
    }

    h1, h2, h3, h4, p, li { color: #F0F2F6 !important; }

    /* Uploader Text Black Fix */
    [data-testid="stFileUploader"] section { color: #000000 !important; }
    [data-testid="stFileUploader"] section * { color: #000000 !important; }
    button[data-testid="baseButton-secondary"] * { color: #000000 !important; }

    .stButton>button {
        background: linear-gradient(90deg, #00A8E8 0%, #007EA7 100%);
        color: white !important;
        border-radius: 8px; border: none; font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)



@st.cache_data(ttl=3600)
def load_data(file):
    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.upper().str.strip()
        return df
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        return None

def generate_ai_report(stats_dict):
    if not API_KEY:
        st.error("⚠️ API Key missing. Please check Secrets or .env")
        return None
    
    try:
       
        client = genai.Client(api_key=API_KEY)
        
        current_date = datetime.now().strftime("%d %B, %Y")
        
        prompt = f"""
        Role: Senior Airline Operations Director.
        Date: {current_date}
        Data: {stats_dict}
        Task: Provide a sharp Executive Briefing {current_date}. 
        Focus on the {stats_dict['major_delays']} major delays.
        Format: Markdown with clear sections.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        st.error(f"AI Connection Error: {e}")
        return None



st.title("✈️ Flight Data Reporting Automation")

with st.sidebar:
    st.header("📂 Data Source")
    uploaded_file = st.file_uploader("Choose CSV File", type=["csv"])
   
    
  
if uploaded_file:
    df = load_data(uploaded_file)
    
    if df is not None:
        target_col = "ARRIVAL_DELAY"
        
        if target_col in df.columns:
           
            df[target_col] = pd.to_numeric(df[target_col], errors="coerce").fillna(0)
            
         
            total = len(df)
            avg_delay = round(df[target_col].mean(), 1)
            major_delays = int(len(df[df[target_col] > 30]))
            on_time_rate = round((len(df[df[target_col] <= 15]) / total) * 100, 1)

          
            st.markdown("### Performance Overview")
            m1, m2, m3, m4 = st.columns(4)
            
            m1.metric("Total Flights", f"{total:,}")
            m2.metric("Average Delay", f"{avg_delay}m")
            m3.metric("Major Disruptions", major_delays)
            m4.metric("On-Time Rate", f"{on_time_rate}%")

            st.markdown("---")

          
            col_chart, col_ai = st.columns([2, 1])

            with col_chart:
                st.subheader("Delay Distribution Analysis")
                
             
                df['STATUS'] = df[target_col].apply(
                    lambda x: 'On-Time/Early' if x <= 0 
                    else ('Minor Delay' if x <= 30 else 'Critical Delay')
                )
                
                fig = px.histogram(
                    df, 
                    x=target_col, 
                    color='STATUS',
                    nbins=40,
                    color_discrete_map={
                        'On-Time/Early': '#00CC96', # Green
                        'Minor Delay': '#FFA15A',    # Orange
                        'Critical Delay': '#EF553B'   # Red
                    },
                    labels={target_col: "Delay (Minutes)", "count": "Flights"},
                    template="plotly_dark"
                )

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", 
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#E0E0E0",
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="white")),
                    bargap=0.1,
                    margin=dict(l=20, r=20, t=50, b=20)
                )

             
                fig.add_vline(x=15, line_dash="dash", line_color="#F0F2F6", 
                              annotation_text="Target Buffer (15m)", annotation_position="top left")

              
                fig.update_xaxes(showgrid=False, zeroline=True, zerolinecolor='rgba(255,255,255,0.2)')
                fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
                
                st.plotly_chart(fig, use_container_width=True)

            with col_ai:
                if st.button("Generate Report", type="primary"):
                    with st.spinner("Analyzing operational vectors..."):
                        stats = {"total": total, "avg_delay": avg_delay, "major_delays": major_delays, "on_time_rate": on_time_rate}
                        report = generate_ai_report(stats)
                        if report:
                            st.info("📄 **Strategic Briefing Ready**")
                            st.markdown(report)
        else:
            st.error(f"❌ Column '{target_col}' not found. Check CSV headers.")
else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👋 Waiting for data. Please select a CSV file from the sidebar...")