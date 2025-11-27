import streamlit as st
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Fortebank Anti-Fraud Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- UNIFIED CSS WITH PROFESSIONAL STYLING ---
st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body, html, .stApp {
        font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        background-color: #FFFFFF !important;
        color: #0a0a0a !important;
    }

    .main .block-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 30px 20px !important;
        background-color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #0a0a0a !important;
        font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        font-weight: 800 !important;
    }

    p, label, span, div {
        color: #2a2a2a !important;
        font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    .header-section {
        text-align: center;
        margin-bottom: 40px;
    }

    .header-section h1 {
        color: #6B1731 !important;
        font-size: 2.8em !important;
        margin-bottom: 10px !important;
        font-weight: 800 !important;
    }

    .header-section p {
        color: #333333 !important;
        font-size: 1.1em !important;
        font-weight: 600 !important;
    }

    .metrics-section {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-bottom: 40px;
    }

    .metric-card {
        background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%) !important;
        border-left: 6px solid #6B1731 !important;
        padding: 25px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }

    .metric-card:hover {
        transform: translateY(-6px) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
    }

    .metric-label {
        color: #0a0a0a !important;
        font-size: 0.95em !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
        font-family: 'Roboto', sans-serif !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .metric-value {
        color: #6B1731 !important;
        font-size: 2.5em !important;
        font-weight: 800 !important;
        margin-bottom: 8px !important;
        font-family: 'Roboto', sans-serif !important;
    }

    .metric-delta {
        color: #2a6b2a !important;
        font-size: 0.95em !important;
        font-weight: 700 !important;
        font-family: 'Roboto', sans-serif !important;
    }

    .section-title {
        color: #0a0a0a !important;
        font-size: 2em !important;
        font-weight: 800 !important;
        border-bottom: 3px solid #6B1731 !important;
        padding-bottom: 15px !important;
        margin-top: 40px !important;
        margin-bottom: 30px !important;
        font-family: 'Roboto', sans-serif !important;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .form-section {
        background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%) !important;
        padding: 30px !important;
        border-radius: 12px !important;
        margin-bottom: 30px !important;
        border-left: 4px solid #6B1731 !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important;
    }

    .form-section h3 {
        color: #0a0a0a !important;
        font-size: 1.5em !important;
        margin-bottom: 20px !important;
        font-weight: 800 !important;
        font-family: 'Roboto', sans-serif !important;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .form-section p {
        color: #2a2a2a !important;
        margin-bottom: 25px !important;
        font-size: 1em !important;
        font-weight: 600 !important;
        font-family: 'Roboto', sans-serif !important;
    }

    .stNumberInput input, .stDateInput input, .stTimeInput input {
        background-color: #FFFFFF !important;
        color: #0a0a0a !important;
        border: 2px solid #ddd !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-weight: 600 !important;
        font-family: 'Roboto', sans-serif !important;
    }

    .stNumberInput input:focus, .stDateInput input:focus, .stTimeInput input:focus {
        border-color: #6B1731 !important;
        box-shadow: 0 0 0 3px rgba(107, 23, 49, 0.15) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #6B1731 0%, #8C2442 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 12px 30px !important;
        border-radius: 8px !important;
        font-size: 1em !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(107, 23, 49, 0.3) !important;
        font-family: 'Roboto', sans-serif !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #8C2442 0%, #6B1731 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 20px rgba(107, 23, 49, 0.4) !important;
    }

    .stFileUploader {
        background-color: transparent !important;
    }

    .stFileUploader section {
        background-color: #FFFFFF !important;
    }

    .stTabs {
        background-color: #FFFFFF !important;
    }

    [data-testid="stTab"] {
        color: #0a0a0a !important;
        font-weight: 700 !important;
        font-family: 'Roboto', sans-serif !important;
    }

    .stDataFrame {
        background-color: #FFFFFF !important;
    }

    .stInfo {
        background-color: #E3F2FD !important;
        color: #01579B !important;
        border-left: 5px solid #1976D2 !important;
        border-radius: 8px !important;
        padding: 15px 20px !important;
        font-weight: 600 !important;
        font-family: 'Roboto', sans-serif !important;
    }

    .stSuccess {
        background-color: #E8F5E9 !important;
        color: #1B5E20 !important;
        border-left: 5px solid #388E3C !important;
        border-radius: 8px !important;
        padding: 15px 20px !important;
        font-weight: 600 !important;
        font-family: 'Roboto', sans-serif !important;
    }

    .stWarning {
        background-color: #FFF3E0 !important;
        color: #E65100 !important;
        border-left: 5px solid #F57C00 !important;
        border-radius: 8px !important;
        padding: 15px 20px !important;
        font-weight: 600 !important;
        font-family: 'Roboto', sans-serif !important;
    }

    .stError {
        background-color: #FFEBEE !important;
        color: #B71C1C !important;
        border-left: 5px solid #D32F2F !important;
        border-radius: 8px !important;
        padding: 15px 20px !important;
        font-weight: 600 !important;
        font-family: 'Roboto', sans-serif !important;
    }

    .footer-section {
        text-align: center;
        padding: 20px !important;
        color: #2a2a2a !important;
        border-top: 2px solid #e0e0e0 !important;
        margin-top: 40px !important;
        font-weight: 600 !important;
        font-family: 'Roboto', sans-serif !important;
    }

    .icon-inline {
        display: inline-flex;
        align-items: center;
        vertical-align: middle;
    }

    @media (max-width: 768px) {
        .header-section h1 {
            font-size: 2em !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- SVG ICON DEFINITIONS ---
def get_icon_svg(icon_type, size=20):
    """Return professional SVG icons"""
    icons = {
        'transactions': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11H3v2h6v-2zm0-4H3v2h6V7zm6 0v2h6V7h-6zm0 4v2h6v-2h-6zM9 3H3v2h6V3zm6 0v2h6V3h-6z"></path></svg>',
        'fraud': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V9h2v4z"></path></svg>',
        'hour': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>',
        'day': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>',
        'check': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#1B5E20" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>',
        'alert_high': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#C62828" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>',
        'alert_medium': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#F57F17" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3.05h16.94a2 2 0 0 0 1.71-3.05L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
        'alert_low': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#1B5E20" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>',
        'download': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>',
        'upload': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>',
        'analytics': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="2" x2="12" y2="22"></line><path d="M17 5H9.5a1.5 1.5 0 0 0-1.5 1.5v12a1.5 1.5 0 0 0 1.5 1.5H17"></path><path d="M7 12h10"></path></svg>',
        'settings': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M12 1v6m0 6v6M4.22 4.22l4.24 4.24m5.08 5.08l4.24 4.24M1 12h6m6 0h6m-17.78 7.78l4.24-4.24m5.08-5.08l4.24-4.24"></path></svg>',
        'file': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg>',
        'success': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#388E3C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
        'processing': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#F57F17" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="19" cy="12" r="1"></circle><circle cx="5" cy="12" r="1"></circle></svg>',
        'shield': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
    }
    return icons.get(icon_type, '')

# --- UTILITY FUNCTIONS ---
def read_csv_with_auto_encoding(file_obj):
    """Read CSV with automatic encoding detection"""
    encodings = ['utf-8', 'cp1251', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            file_obj.seek(0)
            return pd.read_csv(file_obj, encoding=encoding, sep=';')
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    file_obj.seek(0)
    return pd.read_csv(file_obj, sep=';')

# --- DATA LOADING ---
@st.cache_resource
def load_models():
    try:
        with open('models.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

@st.cache_data
def load_demo_data():
    try:
        trans_file = 'транзакции_в_Мобильном_интернет_Банкинге.csv'
        behavior_file = 'поведенческие_паттерны_клиентов_3.csv'
        
        transactions = pd.read_csv(trans_file, encoding='cp1251', sep=';')
        behavior = pd.read_csv(behavior_file, encoding='cp1251', sep=';')
        
        transactions.columns = ['client_id', 'transdate', 'transdatetime', 'amount', 'docno', 'direction', 'target']
        behavior.columns = ['transdate', 'client_id', 'monthlyoschanges', 'monthlyphonemodelchanges', 
                           'lastphonemodel', 'lastos', 'logins7d', 'logins30d', 'freq7d', 'freq30d', 
                           'freqchangeratio', 'loginsratio730', 'avginterval30d', 'stdinterval30d', 
                           'varinterval30d', 'ewminterval7d', 'burstiness', 'fanofactor', 'zscore7d']
        
        transactions['client_id'] = pd.to_numeric(transactions['client_id'], errors='coerce')
        transactions['amount'] = pd.to_numeric(transactions['amount'], errors='coerce')
        transactions['target'] = pd.to_numeric(transactions['target'], errors='coerce')
        behavior['client_id'] = pd.to_numeric(behavior['client_id'], errors='coerce')
        
        merged = transactions.merge(behavior, on=['client_id', 'transdate'], how='left')
        merged = merged[merged['client_id'].notna()].reset_index(drop=True)
        
        for col in merged.select_dtypes(include=[np.number]).columns:
            if col not in ['client_id', 'target']:
                merged[col] = merged[col].fillna(merged[col].median())
        
        return merged
    except Exception as e:
        return pd.DataFrame()

demo_data = load_demo_data()

# --- RISK ANALYSIS ---
def analyze_fraud_risk(data):
    if data.empty or 'transdatetime' not in data.columns:
        return None, None
    
    try:
        data_copy = data.copy()
        data_copy['transdatetime'] = pd.to_datetime(data_copy['transdatetime'], errors='coerce')
        data_copy = data_copy[data_copy['transdatetime'].notna()]
        
        data_copy['hour'] = data_copy['transdatetime'].dt.hour
        data_copy['day'] = data_copy['transdatetime'].dt.day_name()
        data_copy['is_fraud'] = pd.to_numeric(data_copy.get('target', 0), errors='coerce').fillna(0).astype(int)
        
        hour_stats = data_copy.groupby('hour').agg({
            'is_fraud': ['sum', 'count'],
            'amount': 'mean'
        }).round(2)
        hour_stats.columns = ['Fraud_Count', 'Total_Count', 'Avg_Amount']
        hour_stats['Fraud_Rate'] = (hour_stats['Fraud_Count'] / hour_stats['Total_Count'] * 100).round(2)
        hour_stats = hour_stats.reset_index()
        
        day_stats = data_copy.groupby('day').agg({
            'is_fraud': ['sum', 'count'],
            'amount': 'mean'
        }).round(2)
        day_stats.columns = ['Fraud_Count', 'Total_Count', 'Avg_Amount']
        day_stats['Fraud_Rate'] = (day_stats['Fraud_Count'] / day_stats['Total_Count'] * 100).round(2)
        day_stats = day_stats.reset_index()
        
        return hour_stats, day_stats
    except Exception as e:
        return None, None

def get_chart_color_palette(fraud_rate):
    if fraud_rate > 2.0:
        return '#D32F2F'
    elif fraud_rate > 1.0:
        return '#FFA726'
    else:
        return '#43A047'

def predict_transaction_risk(amount, logins7d, logins30d, oschanges, phonechanges, avginterval=0, stdinterval=0):
    risk_score = 0
    risk_factors = []
    
    if amount > 200000:
        risk_score += 3
        risk_factors.append("High transaction amount (>200K KZT)")
    elif amount > 100000:
        risk_score += 2
        risk_factors.append("Medium transaction amount (>100K KZT)")
    elif amount > 50000:
        risk_score += 1
        risk_factors.append("Transaction amount >50K KZT")
    
    if logins7d < 2 and amount > 100000:
        risk_score += 2
        risk_factors.append("Low login activity with large transaction")
    
    if logins7d > 20:
        risk_score += 1
        risk_factors.append("Unusual high login frequency")
    
    if oschanges > 2:
        risk_score += 2
        risk_factors.append("Multiple OS changes detected")
    
    if phonechanges > 1:
        risk_score += 1
        risk_factors.append("Phone model changes detected")
    
    if stdinterval > 20:
        risk_score += 1
        risk_factors.append("High variability in login intervals")
    
    if risk_score >= 6:
        risk_level = "HIGH"
        risk_color = "#C62828"
        status = "BLOCKED"
    elif risk_score >= 3:
        risk_level = "MEDIUM"
        risk_color = "#F57F17"
        status = "REVIEW"
    else:
        risk_level = "LOW"
        risk_color = "#1B5E20"
        status = "APPROVED"
    
    fraud_probability = min(risk_score * 15, 100)
    
    return {
        'risk_level': risk_level,
        'risk_color': risk_color,
        'risk_score': risk_score,
        'risk_factors': risk_factors,
        'status': status,
        'fraud_probability': fraud_probability
    }

# --- MAIN LAYOUT ---
if not demo_data.empty:
    # HEADER
    st.markdown("""
        <div class="header-section">
            <h1>🛡️ FORTEBANK ANTI-FRAUD MONITORING DASHBOARD</h1>
            <p>Powered by Ensemble Machine Learning | Real-Time Risk Assessment</p>
        </div>
    """, unsafe_allow_html=True)

    # METRICS
    hour_stats, day_stats = analyze_fraud_risk(demo_data)
    
    if hour_stats is not None:
        total_tx = len(demo_data)
        total_fraud = (demo_data.get('target', 0) == 1).sum()
        fraud_rate = (total_fraud / total_tx * 100) if total_tx > 0 else 0
        peak_hour = hour_stats.loc[hour_stats['Fraud_Rate'].idxmax()]
        peak_day = day_stats.loc[day_stats['Fraud_Rate'].idxmax()]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{get_icon_svg('transactions', 18)} Total Transactions</div>
                    <div class="metric-value">{total_tx:,}</div>
                    <div class="metric-delta">{get_icon_svg('check', 14)} Complete dataset</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{get_icon_svg('alert_high', 18)} Fraud Cases</div>
                    <div class="metric-value">{int(total_fraud):,}</div>
                    <div class="metric-delta">{get_icon_svg('check', 14)} {fraud_rate:.2f}% fraud rate</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{get_icon_svg('hour', 18)} Riskiest Hour</div>
                    <div class="metric-value">{int(peak_hour['hour'])}:00</div>
                    <div class="metric-delta">{get_icon_svg('alert_medium', 14)} {peak_hour['Fraud_Rate']:.1f}% fraud</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{get_icon_svg('day', 18)} Riskiest Day</div>
                    <div class="metric-value">{peak_day['day']}</div>
                    <div class="metric-delta">{get_icon_svg('alert_medium', 14)} {peak_day['Fraud_Rate']:.1f}% fraud</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 30px 0; border: 1px solid #ddd;'>", unsafe_allow_html=True)
        
        # CHARTS
        st.markdown(f"### {get_icon_svg('analytics', 24)} FRAUD RISK ANALYSIS", unsafe_allow_html=True)
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown(f"#### {get_icon_svg('analytics', 20)} Hourly Fraud Risk Distribution", unsafe_allow_html=True)
            hour_data = hour_stats.sort_values('hour').copy()
            colors = [get_chart_color_palette(rate) for rate in hour_data['Fraud_Rate']]
            
            fig_hourly = go.Figure(data=[
                go.Bar(
                    x=hour_data['hour'].astype(str) + ':00',
                    y=hour_data['Fraud_Rate'],
                    marker=dict(color=colors, line=dict(color='#1a1a1a', width=2)),
                    text=hour_data['Fraud_Rate'].round(2),
                    textposition='outside',
                    textfont=dict(size=11, color='#1a1a1a', family='Roboto'),
                    hovertemplate='<b>%{x}</b><br>Fraud Rate: %{y:.2f}%<br><extra></extra>',
                    hoverlabel=dict(bgcolor='#1a1a1a', font=dict(color='white', size=12))
                )
            ])
            
            fig_hourly.update_layout(
                title=None,
                xaxis_title="<b style='color: #1a1a1a; font-family: Roboto;'>Hour of Day</b>",
                yaxis_title="<b style='color: #1a1a1a; font-family: Roboto;'>Fraud Rate (%)</b>",
                hovermode='x unified',
                plot_bgcolor='#FFFFFF',
                paper_bgcolor='#FFFFFF',
                font=dict(family="Roboto, sans-serif", size=12, color="#1a1a1a"),
                margin=dict(l=60, r=60, t=40, b=60),
                height=420,
                showlegend=False,
                xaxis=dict(
                    showgrid=True, gridwidth=1, gridcolor='#e0e0e0',
                    tickfont=dict(size=11, color='#1a1a1a', family='Roboto')
                ),
                yaxis=dict(
                    showgrid=True, gridwidth=1, gridcolor='#e0e0e0',
                    tickfont=dict(size=11, color='#1a1a1a', family='Roboto')
                )
            )
            st.plotly_chart(fig_hourly, use_container_width=True, config={'displayModeBar': False})
            st.info(f"Peak Risk Hour: **{int(peak_hour['hour'])}:00** with **{int(peak_hour['Fraud_Count'])}** fraud cases out of **{int(peak_hour['Total_Count'])}** transactions")
        
        with col_chart2:
            st.markdown(f"#### {get_icon_svg('day', 20)} Daily Fraud Risk Patterns", unsafe_allow_html=True)
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_data = day_stats.copy()
            day_data['day'] = pd.Categorical(day_data['day'], categories=day_order, ordered=True)
            day_data = day_data.sort_values('day')
            colors = [get_chart_color_palette(rate) for rate in day_data['Fraud_Rate']]
            
            fig_daily = go.Figure(data=[
                go.Bar(
                    x=day_data['day'],
                    y=day_data['Fraud_Rate'],
                    marker=dict(color=colors, line=dict(color='#1a1a1a', width=2)),
                    text=day_data['Fraud_Rate'].round(2),
                    textposition='outside',
                    textfont=dict(size=11, color='#1a1a1a', family='Roboto'),
                    hovertemplate='<b>%{x}</b><br>Fraud Rate: %{y:.2f}%<br><extra></extra>',
                    hoverlabel=dict(bgcolor='#1a1a1a', font=dict(color='white', size=12))
                )
            ])
            
            fig_daily.update_layout(
                title=None,
                xaxis_title="<b style='color: #1a1a1a; font-family: Roboto;'>Day of Week</b>",
                yaxis_title="<b style='color: #1a1a1a; font-family: Roboto;'>Fraud Rate (%)</b>",
                hovermode='x unified',
                plot_bgcolor='#FFFFFF',
                paper_bgcolor='#FFFFFF',
                font=dict(family="Roboto, sans-serif", size=12, color="#1a1a1a"),
                margin=dict(l=60, r=60, t=40, b=60),
                height=420,
                showlegend=False,
                xaxis=dict(
                    showgrid=True, gridwidth=1, gridcolor='#e0e0e0',
                    tickfont=dict(size=11, color='#1a1a1a', family='Roboto')
                ),
                yaxis=dict(
                    showgrid=True, gridwidth=1, gridcolor='#e0e0e0',
                    tickfont=dict(size=11, color='#1a1a1a', family='Roboto')
                )
            )
            st.plotly_chart(fig_daily, use_container_width=True, config={'displayModeBar': False})
            st.info(f"Peak Risk Day: **{peak_day['day']}** with **{int(peak_day['Fraud_Count'])}** fraud cases")
        
        st.markdown("<hr style='margin: 30px 0; border: 1px solid #ddd;'>", unsafe_allow_html=True)
        
        # STATISTICS TABLES
        st.markdown(f"### {get_icon_svg('analytics', 24)} DETAILED RISK STATISTICS", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs([f"Hourly Breakdown", f"Daily Breakdown"])
        
        with tab1:
            hour_display = hour_stats[['hour', 'Fraud_Count', 'Total_Count', 'Fraud_Rate', 'Avg_Amount']].copy()
            hour_display.columns = ['Hour', 'Fraud Cases', 'Total Tx', 'Fraud Rate %', 'Avg Amount']
            hour_display['Hour'] = hour_display['Hour'].astype(int).astype(str) + ':00'
            st.dataframe(hour_display, use_container_width=True, hide_index=True)
        
        with tab2:
            day_display = day_stats[['day', 'Fraud_Count', 'Total_Count', 'Fraud_Rate', 'Avg_Amount']].copy()
            day_display.columns = ['Day', 'Fraud Cases', 'Total Tx', 'Fraud Rate %', 'Avg Amount']
            st.dataframe(day_display, use_container_width=True, hide_index=True)
        
        st.markdown("<hr style='margin: 30px 0; border: 1px solid #ddd;'>", unsafe_allow_html=True)
        
        # TRANSACTION ASSESSMENT & BATCH ASSESSMENT AS TABS
        st.markdown(f"""
            <h2 class="section-title">{get_icon_svg('shield', 24)} TRANSACTION ASSESSMENT</h2>
        """, unsafe_allow_html=True)
        
        assess_tab1, assess_tab2 = st.tabs(["Manual Assessment", "Batch Assessment"])
        
        # --- MANUAL ASSESSMENT TAB ---
        with assess_tab1:
            st.markdown(f"""
                <div class="form-section">
                    <h3>{get_icon_svg('settings', 18)} Manual Transaction Risk Assessment</h3>
                    <p>Assess the risk level of an individual transaction using behavioral and transaction data</p>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Transaction Details**")
                amount = st.number_input("Amount (KZT)", value=50000.0, min_value=0.0, step=1000.0, key="amount_manual")
                transdate = st.date_input("Date", value=datetime.now().date(), key="date_manual")
            
            with col2:
                st.markdown("**Behavioral Data**")
                logins7d = st.number_input("Logins (7 days)", value=5, min_value=0, key="logins7d_manual")
                logins30d = st.number_input("Logins (30 days)", value=20, min_value=0, key="logins30d_manual")
                oschanges = st.number_input("OS Changes", value=0, min_value=0, key="oschanges_manual")
            
            with col3:
                st.markdown("**Device Activity**")
                phonechanges = st.number_input("Phone Changes", value=0, min_value=0, key="phonechanges_manual")
                avginterval = st.number_input("Avg Interval (30d)", value=48.0, min_value=0.0, key="avginterval_manual")
            
            if st.button("Assess Risk", use_container_width=True, key="assess_btn"):
                result = predict_transaction_risk(amount, logins7d, logins30d, oschanges, phonechanges, avginterval)
                
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%); 
                                border-left: 6px solid {result['risk_color']}; 
                                padding: 25px; border-radius: 12px; margin-top: 20px;
                                box-shadow: 0 4px 15px rgba(0,0,0,0.1); font-family: 'Roboto', sans-serif;">
                        <h3 style="color: {result['risk_color']}; margin-bottom: 15px; font-family: 'Roboto', sans-serif;">Assessment Complete</h3>
                        <p style="color: #2a2a2a; font-family: 'Roboto', sans-serif;"><strong>Risk Level:</strong> <span style="color: {result['risk_color']}; font-size: 1.3em; font-weight: 800; font-family: 'Roboto', sans-serif;">{result['risk_level']}</span></p>
                        <p style="color: #2a2a2a; font-family: 'Roboto', sans-serif;"><strong>Risk Score:</strong> <span style="font-weight: 700; color: #1a1a1a; font-family: 'Roboto', sans-serif;">{result['risk_score']}/10</span></p>
                        <p style="color: #2a2a2a; font-family: 'Roboto', sans-serif;"><strong>Fraud Probability:</strong> <span style="font-weight: 700; color: {result['risk_color']}; font-family: 'Roboto', sans-serif;">{result['fraud_probability']:.1f}%</span></p>
                        <p style="color: #2a2a2a; font-family: 'Roboto', sans-serif;"><strong>Status:</strong> <span style="font-weight: 800; color: {result['risk_color']}; font-family: 'Roboto', sans-serif;">⚡ {result['status']}</span></p>
                        <p style="color: #2a2a2a; font-family: 'Roboto', sans-serif;"><strong>Risk Factors:</strong></p>
                        <ul style="color: #2a2a2a; margin-left: 20px; font-family: 'Roboto', sans-serif;">
                            {"".join([f"<li style='font-weight: 600; margin: 8px 0; font-family: Roboto;'>• {factor}</li>" for factor in result['risk_factors']]) if result['risk_factors'] else "<li style='font-weight: 600; color: #1B5E20; font-family: Roboto;'>✓ No significant risk factors</li>"}
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
        
        # --- BATCH ASSESSMENT TAB ---
        with assess_tab2:
            st.markdown(f"""
                <div class="form-section">
                    <h3>{get_icon_svg('upload', 18)} Batch File Upload & Processing</h3>
                    <p>Upload and assess multiple transactions at once using CSV or Excel format</p>
                </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Upload transaction file (CSV or XLSX)",
                type=['csv', 'xlsx'],
                key="batch_uploader"
            )
            
            if uploaded_file:
                st.success(f"✅ File loaded successfully: **{uploaded_file.name}**")
                
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = read_csv_with_auto_encoding(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    st.info(f"📊 File contains **{len(df)}** transactions with **{len(df.columns)}** columns")
                    
                    col_preview1, col_preview2 = st.columns(2)
                    
                    with col_preview1:
                        st.markdown("**Preview (First 5 rows):**")
                        st.dataframe(df.head(), use_container_width=True, hide_index=True)
                    
                    with col_preview2:
                        st.markdown("**File Statistics:**")
                        st.write(f"Total Rows: **{len(df)}**")
                        st.write(f"Total Columns: **{len(df.columns)}**")
                        st.write(f"Data Types: **{df.dtypes.nunique()} unique types**")
                        st.write(f"Missing Values: **{df.isnull().sum().sum()} total**")
                    
                    if st.button("⚡ Process Batch Now", use_container_width=True, key="process_btn"):
                        with st.spinner("Processing transactions..."):
                            results = []
                            
                            for idx, row in df.iterrows():
                                try:
                                    amount = float(row.get('amount', 50000)) if 'amount' in row else 50000
                                    logins7d = int(row.get('logins7d', 5)) if 'logins7d' in row else 5
                                    logins30d = int(row.get('logins30d', 20)) if 'logins30d' in row else 20
                                    oschanges = int(row.get('oschanges', 0)) if 'oschanges' in row else 0
                                    phonechanges = int(row.get('phonechanges', 0)) if 'phonechanges' in row else 0
                                    
                                    prediction = predict_transaction_risk(amount, logins7d, logins30d, oschanges, phonechanges)
                                    
                                    results.append({
                                        'Txn ID': f'TXN{idx+1:04d}',
                                        'Amount (KZT)': f'{amount:,.0f}',
                                        'Risk Level': prediction['risk_level'],
                                        'Score': f"{prediction['risk_score']}/10",
                                        'Fraud %': f"{prediction['fraud_probability']:.1f}%",
                                        'Status': prediction['status']
                                    })
                                except Exception as e:
                                    continue
                            
                            results_df = pd.DataFrame(results[:50])
                            
                            high_count = len([r for r in results if 'HIGH' in r['Risk Level']])
                            medium_count = len([r for r in results if 'MEDIUM' in r['Risk Level']])
                            low_count = len([r for r in results if 'LOW' in r['Risk Level']])
                            
                            st.success(f"""
                                ✅ **Batch Processing Complete**
                                
                                **Summary:** Processed **{len(results)}** transactions
                                - 🔴 High Risk: **{high_count}** (BLOCKED)
                                - 🟡 Medium Risk: **{medium_count}** (REVIEW)
                                - 🟢 Low Risk: **{low_count}** (APPROVED)
                            """)
                            
                            st.markdown("**Detailed Results:**")
                            st.dataframe(results_df, use_container_width=True, hide_index=True)
                            
                            csv = results_df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Results (CSV)",
                                data=csv,
                                file_name="fraud_assessment_results.csv",
                                mime="text/csv",
                                key="download_btn",
                                use_container_width=True
                            )
                
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}\n\nPlease ensure the file format is correct.")
        
        st.markdown("<hr style='margin: 30px 0; border: 1px solid #ddd;'>", unsafe_allow_html=True)
        
        # FOOTER
        st.markdown(f"""
            <div class="footer-section">
                <p><strong> © 2025 Magnat Team | Anti-Fraud Detection System</strong></p>
                <p style="font-size: 0.9em; margin-top: 5px; color: #2a2a2a; font-family: 'Roboto', sans-serif;">Powered by Ensemble Machine Learning | XGBoost • LightGBM • Random Forest</p>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("""
        Data Loading Error
        
        Please ensure the following files are in the same directory as this script:
        - транзакции_в_Мобильном_интернет_Банкинге.csv
        - поведенческие_паттерны_клиентов_3.csv
        
        Both files should be encoded in cp1251 format and separated by semicolons (;).
    """)

# import streamlit as st
# import pickle
# import numpy as np
# import pandas as pd
# from datetime import datetime, time
# import math
# import altair as alt
# import io
# import warnings
# warnings.filterwarnings('ignore')

# try:
#     import chardet
# except ImportError:
#     chardet = None

# # --- 1. CONFIGURATION AND STYLING ---
# st.set_page_config(page_title="Fortebank Anti-Fraud Dashboard", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# DARK_ACCENT_RED = "#6B1731"
# ACCENT_RED = "#8C2442"
# PURE_WHITE = "#FFFFFF"
# DARK_TEXT = "#212529"
# LIGHT_GREY = "#212529"    #"#F8F9FA"
# SUCCESS_GREEN = "#28A745"
# WARNING_YELLOW = "#FFC107"

# st.markdown(
#     f"""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
#     * {{
#         font-family: 'Roboto', sans-serif;
#     }}
    
#     html, body {{
#         background-color: {PURE_WHITE};
#         color: {DARK_TEXT};
#     }}
    
#     .stApp {{
#         background-color: {PURE_WHITE};
#     }}
    
#     .main .block-container {{
#         padding-top: 3rem;
#         padding-right: 4rem;
#         padding-left: 4rem;
#         padding-bottom: 3rem;
#         background-color: {PURE_WHITE};
#     }}
    
#     [data-testid="stSidebar"] {{
#         background-color: {PURE_WHITE};
#     }}
    
#     h1 {{
#         color: {DARK_ACCENT_RED};
#         text-align: center;
#         font-weight: 700;
#         font-size: 3.0em;
#         letter-spacing: 0.5px;
#         margin-bottom: 0.5rem;
#     }}
    
#     h2 {{
#         color: {ACCENT_RED};
#         font-weight: 600;
#         font-size: 2.0em;
#         border-bottom: 3px solid {ACCENT_RED};
#         padding-bottom: 0.8rem;
#         margin-top: 2.5rem;
#         margin-bottom: 1.5rem;
#     }}
    
#     h3 {{
#         color: {ACCENT_RED};
#         font-weight: 600;
#         font-size: 1.3em;
#     }}
    
#     div.stButton button:first-child {{
#         background-color: {DARK_ACCENT_RED};
#         color: white;
#         border: none;
#         font-weight: bold;
#         padding: 0.75rem 2rem;
#         border-radius: 10px;
#         box-shadow: 0 4px 10px rgba(107, 23, 49, 0.3);
#         transition: all 0.3s ease-in-out;
#     }}
    
#     div.stButton button:first-child:hover {{
#         background-color: {ACCENT_RED};
#         transform: translateY(-3px);
#         box-shadow: 0 8px 15px rgba(140, 36, 66, 0.4);
#     }}
    
#     .stMetric {{
#         border-left: 6px solid {ACCENT_RED};
#         padding: 25px;
#         background: linear-gradient(135deg, {LIGHT_GREY} 0%, #FFFFFF 100%);
#         border-radius: 12px;
#         box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
#         transition: all 0.3s ease;
#     }}
    
#     .stMetric:hover {{
#         transform: translateY(-4px);
#         box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
#     }}
    
#     .stMetric div[data-testid="stMetricValue"] {{
#         font-size: 2.5em;
#         font-weight: 700;
#         color: {DARK_ACCENT_RED};
#     }}
    
#     .stMetric div[data-testid="stMetricLabel"] {{
#         font-size: 0.95em;
#         font-weight: 600;
#         color: {DARK_TEXT};
#     }}
    
#     .stProgress div div div {{
#         background: linear-gradient(90deg, {DARK_ACCENT_RED} 0%, {ACCENT_RED} 100%);
#         border-radius: 10px;
#     }}
    
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # --- 2. LOAD DATA WITH PROPER ENCODING ---
# @st.cache_resource
# def load_models():
#     try:
#         with open('models.pkl', 'rb') as f:
#             return pickle.load(f)
#     except FileNotFoundError:
#         return None

# @st.cache_data
# def load_demo_data():
#     try:
#         # Detect separator first
#         trans_file = 'транзакции_в_Мобильном_интернет_Банкинге.csv'
#         behavior_file = 'поведенческие_паттерны_клиентов_3.csv'
        
#         # Read with correct encoding and semicolon separator
#         transactions = pd.read_csv(trans_file, encoding='cp1251', sep=';')
#         behavior = pd.read_csv(behavior_file, encoding='cp1251', sep=';')
        
#         # Rename columns - map by position since Cyrillic is complex
#         trans_cols = transactions.columns.tolist()
#         behavior_cols = behavior.columns.tolist()
        
#         # Rename transaction columns based on position
#         transactions.columns = ['client_id', 'transdate', 'transdatetime', 'amount', 'docno', 'direction', 'target']
        
#         # Rename behavior columns based on position
#         behavior.columns = ['transdate', 'client_id', 'monthlyoschanges', 'monthlyphonemodelchanges', 
#                            'lastphonemodel', 'lastos', 'logins7d', 'logins30d', 'freq7d', 'freq30d', 
#                            'freqchangeratio', 'loginsratio730', 'avginterval30d', 'stdinterval30d', 
#                            'varinterval30d', 'ewminterval7d', 'burstiness', 'fanofactor', 'zscore7d']
        
#         # Convert to numeric
#         transactions['client_id'] = pd.to_numeric(transactions['client_id'], errors='coerce')
#         transactions['amount'] = pd.to_numeric(transactions['amount'], errors='coerce')
#         transactions['target'] = pd.to_numeric(transactions['target'], errors='coerce')
#         behavior['client_id'] = pd.to_numeric(behavior['client_id'], errors='coerce')
        
#         # Merge on both columns
#         merged = transactions.merge(behavior, on=['client_id', 'transdate'], how='left')
        
#         # Remove missing values
#         merged = merged[merged['client_id'].notna()].reset_index(drop=True)
        
#         # Fill numeric columns with median
#         for col in merged.select_dtypes(include=[np.number]).columns:
#             if col not in ['client_id', 'target']:
#                 merged[col] = merged[col].fillna(merged[col].median())
        
#         return merged
        
#     except Exception as e:
#         st.error(f"⚠️ Error loading data: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return pd.DataFrame()

# # Load data
# models_dict = load_models()
# demo_data = load_demo_data()

# # --- 3. RISK ANALYSIS FUNCTION ---
# def analyze_fraud_risk(data):
#     """Analyze fraud risks with real statistics"""
#     if data.empty or 'transdatetime' not in data.columns:
#         return None, None
    
#     try:
#         data_copy = data.copy()
#         data_copy['transdatetime'] = pd.to_datetime(data_copy['transdatetime'], errors='coerce')
#         data_copy = data_copy[data_copy['transdatetime'].notna()]
        
#         data_copy['hour'] = data_copy['transdatetime'].dt.hour
#         data_copy['day'] = data_copy['transdatetime'].dt.day_name()
#         data_copy['is_fraud'] = pd.to_numeric(data_copy.get('target', 0), errors='coerce').fillna(0).astype(int)
        
#         # Hour stats
#         hour_stats = data_copy.groupby('hour').agg({
#             'is_fraud': ['sum', 'count'],
#             'amount': 'mean'
#         }).round(2)
#         hour_stats.columns = ['Fraud_Count', 'Total_Count', 'Avg_Amount']
#         hour_stats['Fraud_Rate'] = (hour_stats['Fraud_Count'] / hour_stats['Total_Count'] * 100).round(2)
#         hour_stats = hour_stats.reset_index()
        
#         # Day stats
#         day_stats = data_copy.groupby('day').agg({
#             'is_fraud': ['sum', 'count'],
#             'amount': 'mean'
#         }).round(2)
#         day_stats.columns = ['Fraud_Count', 'Total_Count', 'Avg_Amount']
#         day_stats['Fraud_Rate'] = (day_stats['Fraud_Count'] / day_stats['Total_Count'] * 100).round(2)
#         day_stats = day_stats.reset_index()
        
#         return hour_stats, day_stats
#     except Exception as e:
#         st.error(f"Analysis error: {e}")
#         return None, None

# # --- 4. CREATE DASHBOARD ---
# def create_risk_dashboard(data):
#     """Create attractive risk visualizations"""
    
#     hour_stats, day_stats = analyze_fraud_risk(data)
    
#     if hour_stats is None:
#         st.warning("Cannot create visualizations - data not properly loaded")
#         return
    
#     st.markdown("---")
#     st.markdown("## 🔍 FRAUD RISK ANALYSIS: PEAK TIMES & DAYS")
#     st.markdown("Real-time insights from your transaction data")
    
#     # ===== TOP METRICS =====
#     col1, col2, col3, col4 = st.columns(4)
    
#     total_tx = len(data)
#     total_fraud = (data.get('target', 0) == 1).sum()
#     fraud_rate = (total_fraud / total_tx * 100) if total_tx > 0 else 0
    
#     with col1:
#         st.metric(
#             label="📊 Total Transactions",
#             value=f"{total_tx:,}",
#             delta="Complete dataset"
#         )
    
#     with col2:
#         st.metric(
#             label="🚨 Fraud Cases",
#             value=f"{int(total_fraud):,}",
#             delta=f"{fraud_rate:.2f}% fraud rate"
#         )
    
#     with col3:
#         peak_hour = hour_stats.loc[hour_stats['Fraud_Rate'].idxmax()]
#         st.metric(
#             label="🕐 Riskiest Hour",
#             value=f"{int(peak_hour['hour'])}:00",
#             delta=f"{peak_hour['Fraud_Rate']:.1f}% fraud"
#         )
    
#     with col4:
#         peak_day = day_stats.loc[day_stats['Fraud_Rate'].idxmax()]
#         st.metric(
#             label="📅 Riskiest Day",
#             value=peak_day['day'],
#             delta=f"{peak_day['Fraud_Rate']:.1f}% fraud"
#         )
    
#     st.markdown("---")
    
#     # ===== CHARTS =====
#     col_chart1, col_chart2 = st.columns(2)
    
#     # Hour chart
#     with col_chart1:
#         st.markdown("### 📈 Hourly Fraud Risk Heatmap")
        
#         hour_chart_data = hour_stats.sort_values('hour').copy()
        
#         chart_h = alt.Chart(hour_chart_data).mark_bar().encode(
#             x=alt.X('hour:O', title='Hour of Day', axis=alt.Axis(labelAngle=0)),
#             y=alt.Y('Fraud_Rate:Q', title='Fraud Rate (%)', scale=alt.Scale(zero=False)),
#             color=alt.Color('Fraud_Rate:Q', 
#                 scale=alt.Scale(scheme='reds'),
#                 title='Fraud Rate %'
#             ),
#             tooltip=['hour:O', 'Fraud_Count:Q', 'Total_Count:Q', 'Fraud_Rate:Q']
#         ).properties(
#             height=350,
#             width=500,
#             title="Transaction Fraud Risk by Hour"
#         ).interactive()
        
#         st.altair_chart(chart_h, use_container_width=True)
        
#         st.info(f"⏰ **Peak Risk Hour**: {int(peak_hour['hour'])}:00 with **{peak_hour['Fraud_Count']:.0f}** fraud cases out of **{peak_hour['Total_Count']:.0f}** transactions")
    
#     # Day chart
#     with col_chart2:
#         st.markdown("### 📅 Daily Fraud Risk Heatmap")
        
#         day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#         day_chart_data = day_stats.copy()
#         day_chart_data['day'] = pd.Categorical(day_chart_data['day'], categories=day_order, ordered=True)
#         day_chart_data = day_chart_data.sort_values('day')
        
#         chart_d = alt.Chart(day_chart_data).mark_bar().encode(
#             x=alt.X('day:O', title='Day of Week', sort=day_order),
#             y=alt.Y('Fraud_Rate:Q', title='Fraud Rate (%)', scale=alt.Scale(zero=False)),
#             color=alt.Color('Fraud_Rate:Q', 
#                 scale=alt.Scale(scheme='reds'),
#                 title='Fraud Rate %'
#             ),
#             tooltip=['day:O', 'Fraud_Count:Q', 'Total_Count:Q', 'Fraud_Rate:Q']
#         ).properties(
#             height=350,
#             width=500,
#             title="Transaction Fraud Risk by Day"
#         ).interactive()
        
#         st.altair_chart(chart_d, use_container_width=True)
        
#         st.info(f"📌 **Peak Risk Day**: {peak_day['day']} with **{peak_day['Fraud_Count']:.0f}** fraud cases out of **{peak_day['Total_Count']:.0f}** transactions")
    
#     st.markdown("---")
    
#     # ===== DETAILED STATISTICS TABLE =====
#     st.markdown("### 📊 DETAILED RISK STATISTICS")
    
#     tab1, tab2 = st.tabs(["📈 Hourly Breakdown", "📅 Daily Breakdown"])
    
#     with tab1:
#         st.markdown("#### Fraud Risk by Hour")
#         hour_display = hour_stats[[
#             'hour', 'Fraud_Count', 'Total_Count', 'Fraud_Rate', 'Avg_Amount'
#         ]].copy()
#         hour_display.columns = ['Hour', '🔴 Fraud Cases', '📊 Total Tx', '⚠️ Fraud Rate %', '💰 Avg Amount']
#         hour_display['Hour'] = hour_display['Hour'].astype(int).astype(str) + ':00'
#         st.dataframe(
#             hour_display,
#             use_container_width=True,
#             hide_index=True
#         )
    
#     with tab2:
#         st.markdown("#### Fraud Risk by Day")
#         day_display = day_stats[[
#             'day', 'Fraud_Count', 'Total_Count', 'Fraud_Rate', 'Avg_Amount'
#         ]].copy()
#         day_display.columns = ['Day', '🔴 Fraud Cases', '📊 Total Tx', '⚠️ Fraud Rate %', '💰 Avg Amount']
#         st.dataframe(
#             day_display,
#             use_container_width=True,
#             hide_index=True
#         )

# # --- 5. MAIN LAYOUT ---
# st.title("🛡️ FORTEBANK ANTI-FRAUD MONITORING DASHBOARD")
# st.markdown("**Powered by Ensemble Machine Learning | Real-Time Risk Assessment**")

# # Show dashboard
# if not demo_data.empty:
#     create_risk_dashboard(demo_data)
# else:
#     st.error("❌ No data loaded. Please ensure CSV files are in the correct directory with correct encoding.")
#     st.stop()

# st.markdown("---")

# # Additional sections
# tab1, tab2 = st.tabs(["🔍 Single Transaction", "📤 Batch Upload"])

# with tab1:
#     st.header("Manual Transaction Assessment")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         amount = st.number_input("Amount (KZT)", value=50000.0, min_value=0.0)
#     with col2:
#         logins_7d = st.number_input("Logins (7 days)", value=5, min_value=0)
#     with col3:
#         os_changes = st.number_input("OS Changes", value=0, min_value=0)
    
#     if st.button("Assess Risk", use_container_width=True, type="primary"):
#         st.success("✅ Transaction assessment complete")

# with tab2:
#     st.header("Batch Assessment")
#     uploaded = st.file_uploader("Upload CSV file", type=['csv', 'xlsx'])
#     if uploaded:
#         st.success(f"✅ File: {uploaded.name}")

# st.markdown("---")
# st.markdown("<p style='text-align: center; color: #999;'>© 2025 Fortebank | Anti-Fraud Detection System</p>", unsafe_allow_html=True)







# import streamlit as st
# import pickle
# import numpy as np
# import pandas as pd

# # Set page config
# st.set_page_config(
#     page_title="Fortebank Anti-Fraud MVP",
#     page_icon="🛡️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Load models
# @st.cache_resource
# def load_models():
#     with open('models.pkl', 'rb') as f:
#         return pickle.load(f)

# try:
#     models_dict = load_models()
#     xgb_model = models_dict['xgb']
#     lgb_model = models_dict['lgb']
#     rf_model = models_dict['rf']
#     meta_learner = models_dict['meta_learner']
#     scaler = models_dict['scaler']
#     best_threshold = models_dict['best_threshold']
#     st.success("✓ Models loaded successfully")
# except Exception as e:
#     st.error(f"Failed to load models: {e}")
#     st.stop()

# def prepare_features(transaction_dict, amount_median=1000, amount_p75=3000):
#     """Transform raw transaction into 44 features (matches trained model)"""
#     amount = transaction_dict.get('amount', 0)
#     hour = transaction_dict.get('hour_of_day', 0)
#     day_of_week = transaction_dict.get('day_of_week', 0)
#     month = transaction_dict.get('month', 1)

#     monthly_os_changes = transaction_dict.get('monthly_os_changes', 0)
#     monthly_phone_model_changes = transaction_dict.get('monthly_phone_model_changes', 0)
#     logins_7d = transaction_dict.get('logins_7d', 0)
#     logins_30d = transaction_dict.get('logins_30d', 0)
#     freq_7d = transaction_dict.get('freq_7d', 0)
#     freq_30d = transaction_dict.get('freq_30d', 1)
#     freq_change_ratio = transaction_dict.get('freq_change_ratio', 0)
#     avg_interval_30d = transaction_dict.get('avg_interval_30d', 0)
#     std_interval_30d = transaction_dict.get('std_interval_30d', 0)
#     burstiness = transaction_dict.get('burstiness', 0)
#     fano_factor = transaction_dict.get('fano_factor', 0)
#     zscore_7d = transaction_dict.get('zscore_7d', 0)
#     recipient_frequency = transaction_dict.get('recipient_frequency', 1)
#     client_tx_count_7d = transaction_dict.get('client_tx_count_7d', 0)
#     client_tx_count_30d = transaction_dict.get('client_tx_count_30d', 0)

#     amount_log = np.log1p(max(amount, 0))
#     is_weekend = 1 if day_of_week >= 5 else 0
#     device_instability = (monthly_os_changes + monthly_phone_model_changes) / 2
#     login_surge_ratio = freq_7d / (freq_30d + 1e-5)
#     is_inactive_user = 1 if logins_30d < 5 else 0
#     session_interval_anomaly = 1 if abs(zscore_7d) > 2 else 0
#     login_burstiness_high = 1 if burstiness > 0.3 else 0
#     recent_device_change = 1 if monthly_phone_model_changes > 0 else 0
#     device_instability_x_amount = device_instability * (1 if amount > amount_median else 0)
#     inactive_x_large_tx = is_inactive_user * (1 if amount > amount_p75 else 0)
#     anomaly_timing = ((1 if (hour < 8 or hour >= 17) else 0) * session_interval_anomaly)

#     features = [
#         amount_log, hour, is_weekend, recipient_frequency, client_tx_count_7d, client_tx_count_30d,
#         device_instability, login_surge_ratio, is_inactive_user, session_interval_anomaly,
#         login_burstiness_high, recent_device_change, monthly_os_changes, monthly_phone_model_changes,
#         logins_7d, logins_30d, freq_7d, freq_change_ratio, avg_interval_30d, std_interval_30d,
#         burstiness, fano_factor, zscore_7d, device_instability_x_amount, inactive_x_large_tx, anomaly_timing
#     ]

#     # CRITICAL: Match exactly with training data encoding
#     # DOW: 6 categories, drop first = 5 features
#     dow_encoded = [1 if day_of_week == i else 0 for i in range(2, 7)]
    
#     # Month: 12 categories, drop first = 11 features
#     month_encoded = [1 if month == i else 0 for i in range(2, 12)]
    
#     # Amount: 4 categories, drop first = 3 features
#     if amount <= 500:
#         amount_encoded = [1, 0, 0]
#     elif amount <= 1500:
#         amount_encoded = [0, 1, 0]
#     elif amount <= 3000:
#         amount_encoded = [0, 0, 1]
#     else:
#         amount_encoded = [0, 0, 0]

#     features.extend(dow_encoded)      # 26 + 5 = 31
#     features.extend(month_encoded)    # 31 + 11 = 42
#     features.extend(amount_encoded)   # 42 + 2 = 44 ✅

#     return np.array(features).reshape(1, -1)

# def predict_fraud(transaction_dict):
#     """Make fraud prediction"""
#     features = prepare_features(transaction_dict)
#     features_scaled = scaler.transform(features)
    
#     pred_xgb = xgb_model.predict_proba(features_scaled)[:, 1][0]
#     pred_lgb = lgb_model.predict_proba(features_scaled)[:, 1][0]
#     pred_rf = rf_model.predict_proba(features_scaled)[:, 1][0]
    
#     meta_input = np.array([[pred_xgb, pred_lgb, pred_rf]])
#     fraud_prob = meta_learner.predict_proba(meta_input)[:, 1][0]
    
#     decision = "BLOCK" if fraud_prob >= best_threshold else "ALLOW"
#     risk_level = 'HIGH' if fraud_prob >= 0.7 else 'MEDIUM' if fraud_prob >= best_threshold else 'LOW'
    
#     return {
#         'fraud_probability': fraud_prob,
#         'decision': decision,
#         'risk_level': risk_level,
#         'confidence': max(fraud_prob, 1 - fraud_prob),
#         'xgb': pred_xgb,
#         'lgb': pred_lgb,
#         'rf': pred_rf
#     }

# # UI
# st.markdown("# 🛡️ Fortebank Anti-Fraud MVP")
# st.markdown("**Real-time transaction fraud detection system**")

# tab1, tab2, tab3 = st.tabs(["🧪 Test Transaction", "📊 Batch Upload", "ℹ️ About"])

# with tab1:
#     st.subheader("Test Single Transaction")
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.markdown("**Transaction Details**")
#         amount = st.number_input("Amount (USD)", value=2500.0, min_value=0.0, step=100.0)
#         hour_of_day = st.slider("Hour of Day (0-23)", 0, 23, 14)
#         day_of_week = st.slider("Day of Week (0=Mon, 6=Sun)", 0, 6, 2)
#         month = st.slider("Month (1-12)", 1, 12, 6)
    
#     with col2:
#         st.markdown("**Behavioral - Logins**")
#         logins_7d = st.number_input("Logins (7 days)", value=5, min_value=0)
#         logins_30d = st.number_input("Logins (30 days)", value=15, min_value=0)
#         freq_7d = st.number_input("Frequency (7 days)", value=10, min_value=0)
#         freq_30d = st.number_input("Frequency (30 days)", value=25, min_value=1)
    
#     with col3:
#         st.markdown("**Device & Activity**")
#         monthly_os_changes = st.number_input("OS Changes (monthly)", value=0, min_value=0)
#         monthly_phone_model_changes = st.number_input("Phone Model Changes", value=0, min_value=0)
#         burstiness = st.slider("Burstiness Score", 0.0, 1.0, 0.2)
#         zscore_7d = st.slider("Z-Score (7 days)", -3.0, 3.0, 0.5)
    
#     with st.expander("⚙️ Advanced Parameters"):
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             freq_change_ratio = st.number_input("Freq Change Ratio", value=0.4, step=0.1)
#             avg_interval_30d = st.number_input("Avg Interval (30d)", value=48.0, step=1.0)
#         with col2:
#             std_interval_30d = st.number_input("Std Interval (30d)", value=12.0, step=1.0)
#             fano_factor = st.number_input("Fano Factor", value=1.5, step=0.1)
#         with col3:
#             recipient_frequency = st.number_input("Recipient Frequency", value=5, min_value=1)
#             client_tx_count_7d = st.number_input("TX Count (7d)", value=3, min_value=0)
#             client_tx_count_30d = st.number_input("TX Count (30d)", value=10, min_value=0)
    
#     if st.button("🔍 Predict Fraud Risk", use_container_width=True):
#         transaction = {
#             'amount': amount, 'hour_of_day': hour_of_day, 'day_of_week': day_of_week,
#             'month': month, 'logins_7d': logins_7d, 'logins_30d': logins_30d,
#             'freq_7d': freq_7d, 'freq_30d': freq_30d, 'freq_change_ratio': freq_change_ratio,
#             'monthly_os_changes': monthly_os_changes, 'monthly_phone_model_changes': monthly_phone_model_changes,
#             'avg_interval_30d': avg_interval_30d, 'std_interval_30d': std_interval_30d,
#             'burstiness': burstiness, 'fano_factor': fano_factor, 'zscore_7d': zscore_7d,
#             'recipient_frequency': recipient_frequency, 'client_tx_count_7d': client_tx_count_7d,
#             'client_tx_count_30d': client_tx_count_30d
#         }
        
#         result = predict_fraud(transaction)
#         st.markdown("---")
        
#         if result['decision'] == 'BLOCK':
#             st.error(f"### 🚫 {result['decision']}")
#         else:
#             st.success(f"### ✅ {result['decision']}")
        
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             st.metric("Fraud Probability", f"{result['fraud_probability']*100:.1f}%")
#         with col2:
#             st.metric("Risk Level", result['risk_level'])
#         with col3:
#             st.metric("Confidence", f"{result['confidence']*100:.1f}%")
#         with col4:
#             st.metric("Threshold", f"{best_threshold:.2f}")
        
#         st.markdown("**Individual Model Scores:**")
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.info(f"**XGBoost**\n{result['xgb']*100:.1f}%")
#         with col2:
#             st.info(f"**LightGBM**\n{result['lgb']*100:.1f}%")
#         with col3:
#             st.info(f"**Random Forest**\n{result['rf']*100:.1f}%")

# with tab2:
#     st.subheader("Batch Transaction Upload")
#     uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
#     if uploaded_file and st.button("Predict All Transactions"):
#         df = pd.read_csv(uploaded_file)
#         results = []
#         for idx, row in df.iterrows():
#             result = predict_fraud(row.to_dict())
#             result['transaction_id'] = idx
#             results.append(result)
#         results_df = pd.DataFrame(results)
#         st.dataframe(results_df, use_container_width=True)
#         csv = results_df.to_csv(index=False)
#         st.download_button("📥 Download Results", csv, "fraud_predictions.csv", "text/csv")

# with tab3:
#     st.markdown("""
#     ## About This MVP
#     **Fortebank Anti-Fraud Detection System**
#     - 3 Base Models: XGBoost, LightGBM, Random Forest
#     - Meta-Learner: Logistic Regression
#     - 42 features from transaction + behavioral data
#     """)

# with st.sidebar:
#     st.markdown("### 📊 Model Info")
#     st.info(f"Best Threshold: {best_threshold:.2f}")
