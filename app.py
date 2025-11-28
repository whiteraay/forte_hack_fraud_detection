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


# --- LANGUAGE TRANSLATIONS ---
TRANSLATIONS = {
    "en": {
        "title": "🛡️ FORTEBANK ANTI-FRAUD MONITORING DASHBOARD",
        "subtitle": "Powered by Ensemble Machine Learning | Real-Time Risk Assessment",
        "total_transactions": "Total Transactions",
        "fraud_cases": "Fraud Cases",
        "riskiest_hour": "Riskiest Hour",
        "riskiest_day": "Riskiest Day",
        "complete_dataset": "Complete dataset",
        "fraud_rate": "fraud rate",
        "fraud_risk_analysis": "FRAUD RISK ANALYSIS",
        "hourly_fraud_distribution": "Hourly Fraud Risk Distribution",
        "daily_fraud_patterns": "Daily Fraud Risk Patterns",
        "hour_of_day": "Hour of Day",
        "fraud_rate_percent": "Fraud Rate (%)",
        "day_of_week": "Day of Week",
        "peak_risk_hour": "Peak Risk Hour",
        "peak_risk_day": "Peak Risk Day",
        "detailed_risk_statistics": "DETAILED RISK STATISTICS",
        "hourly_breakdown": "Hourly Breakdown",
        "daily_breakdown": "Daily Breakdown",
        "hour": "Hour",
        "fraud_cases_col": "Fraud Cases",
        "total_tx": "Total Tx",
        "avg_amount": "Avg Amount",
        "day": "Day",
        "transaction_assessment": "TRANSACTION ASSESSMENT",
        "manual_assessment": "Manual Assessment",
        "batch_assessment": "Batch Assessment",
        "manual_transaction_title": "Manual Transaction Risk Assessment",
        "manual_transaction_desc": "Assess the risk level of an individual transaction using behavioral and transaction data",
        "transaction_details": "Transaction Details",
        "amount_kzt": "Amount (KZT)",
        "date": "Date",
        "hour_0_23": "Hour (0-23)",
        "behavioral_data": "Behavioral Data",
        "logins_7_days": "Logins (7 days)",
        "logins_30_days": "Logins (30 days)",
        "os_changes_monthly": "OS Changes (monthly)",
        "device_activity": "Device Activity",
        "phone_changes_monthly": "Phone Changes (monthly)",
        "avg_interval_30d": "Avg Interval (30d)",
        "std_interval_30d": "Std Interval (30d)",
        "advanced_parameters": "⚙️ Advanced Parameters",
        "frequency_7d": "Frequency (7d)",
        "frequency_30d": "Frequency (30d)",
        "freq_change_ratio": "Freq Change Ratio",
        "burstiness": "Burstiness",
        "fano_factor": "Fano Factor",
        "z_score_7d": "Z-Score (7d)",
        "assess_risk": "Assess Risk",
        "assessment_complete": "Assessment Complete",
        "risk_level": "Risk Level",
        "fraud_probability": "Fraud Probability",
        "status": "Status",
        "model_probabilities": "Model Probabilities",
        "batch_title": "Batch File Upload & Processing",
        "batch_desc": "Upload and assess multiple transactions at once using CSV or Excel format",
        "upload_file": "Upload transaction file (CSV or XLSX)",
        "file_loaded": "File loaded successfully",
        "preview_first_5": "Preview (First 5 rows)",
        "file_statistics": "File Statistics",
        "total_rows": "Total Rows",
        "total_columns": "Total Columns",
        "data_types": "Data Types",
        "missing_values": "Missing Values",
        "preview_data": "Preview Data",
        "process_batch_now": "⚡ Process Batch Now",
        "processing": "Processing transactions",
        "batch_complete": "Batch Processing Complete",
        "summary": "Summary",
        "processed_transactions": "Processed",
        "high_risk_blocked": "(BLOCKED)",
        "low_risk_approved": "(APPROVED)",
        "detailed_results": "Detailed Results",
        "download_results": "📥 Download Results (CSV)",
        "txn_id": "Txn ID",
        "amount": "Amount (KZT)",
        "xgboost": "XGBoost",
        "lightgbm": "LightGBM",
        "rf": "RF",
        "no_transactions": "No transactions successfully processed",
        "error_processing": "Error processing file",
        "ensure_correct_format": "Please ensure the file format is correct",
        "copyright": "© 2025 Magnat Team | Anti-Fraud Detection System",
        "powered_by": "Powered by Ensemble Machine Learning | XGBoost • LightGBM • Random Forest",
        "data_loading_error": "Data Loading Error",
        "ensure_files": "Please ensure the following files are in the same directory as this script",
        "file_encoding": "Both files should be encoded in cp1251 format and separated by semicolons (;)",
        "model_error": "Model Error: models.pkl not found",
        "ensure_models": "Please ensure models.pkl is in the same directory as this script",
    },
    "ru": {
        "title": "🛡️ МОНИТОРИНГ ПРОТИВОМОШЕННИЧЕСКОЙ ДЕЯТЕЛЬНОСТИ FORTEBANK",
        "subtitle": "Ансамблевое машинное обучение | Оценка риска в реальном времени",
        "total_transactions": "Всего транзакций",
        "fraud_cases": "Случаи мошенничества",
        "riskiest_hour": "Самый рискованный час",
        "riskiest_day": "Самый рискованный день",
        "complete_dataset": "Полный набор данных",
        "fraud_rate": "уровень мошенничества",
        "fraud_risk_analysis": "АНАЛИЗ РИСКА МОШЕННИЧЕСТВА",
        "hourly_fraud_distribution": "Почасовое распределение риска мошенничества",
        "daily_fraud_patterns": "Дневные паттерны риска мошенничества",
        "hour_of_day": "Час дня",
        "fraud_rate_percent": "Уровень мошенничества (%)",
        "day_of_week": "День недели",
        "peak_risk_hour": "Час пик риска",
        "peak_risk_day": "День пик риска",
        "detailed_risk_statistics": "ДЕТАЛЬНАЯ СТАТИСТИКА РИСКА",
        "hourly_breakdown": "Почасовой разрез",
        "daily_breakdown": "Дневной разрез",
        "hour": "Час",
        "fraud_cases_col": "Случаи мошенничества",
        "total_tx": "Всего Tx",
        "avg_amount": "Средняя сумма",
        "day": "День",
        "transaction_assessment": "ОЦЕНКА ТРАНЗАКЦИИ",
        "manual_assessment": "Ручная оценка",
        "batch_assessment": "Пакетная оценка",
        "manual_transaction_title": "Ручная оценка риска транзакции",
        "manual_transaction_desc": "Оцените риск отдельной транзакции с учетом поведенческих и транзакционных данных",
        "transaction_details": "Детали транзакции",
        "amount_kzt": "Сумма (KZT)",
        "date": "Дата",
        "hour_0_23": "Час (0-23)",
        "behavioral_data": "Поведенческие данные",
        "logins_7_days": "Входы (7 дней)",
        "logins_30_days": "Входы (30 дней)",
        "os_changes_monthly": "Изменения ОС (в месяц)",
        "device_activity": "Активность устройства",
        "phone_changes_monthly": "Изменения телефона (в месяц)",
        "avg_interval_30d": "Средний интервал (30д)",
        "std_interval_30d": "Ст. отклонение (30д)",
        "advanced_parameters": "⚙️ Дополнительные параметры",
        "frequency_7d": "Частота (7 дней)",
        "frequency_30d": "Частота (30 дней)",
        "freq_change_ratio": "Соотношение изменения частоты",
        "burstiness": "Показатель всплесков",
        "fano_factor": "Фактор Фано",
        "z_score_7d": "Z-скор (7д)",
        "assess_risk": "Оценить риск",
        "assessment_complete": "Оценка завершена",
        "risk_level": "Уровень риска",
        "fraud_probability": "Вероятность мошенничества",
        "status": "Статус",
        "model_probabilities": "Вероятности модели",
        "batch_title": "Пакетная загрузка и обработка",
        "batch_desc": "Загрузите и оцените множество транзакций сразу в формате CSV или Excel",
        "upload_file": "Загрузите файл транзакций (CSV или XLSX)",
        "file_loaded": "Файл успешно загружен",
        "preview_first_5": "Предпросмотр (первые 5 строк)",
        "file_statistics": "Статистика файла",
        "total_rows": "Всего строк",
        "total_columns": "Всего столбцов",
        "data_types": "Типы данных",
        "missing_values": "Пропущенные значения",
        "preview_data": "Предпросмотр данных",
        "process_batch_now": "⚡ Обработать пакет",
        "processing": "Обработка транзакций",
        "batch_complete": "Пакетная обработка завершена",
        "summary": "Итоговый отчет",
        "processed_transactions": "Обработано",
        "high_risk_blocked": "(ЗАБЛОКИРОВАНО)",
        "low_risk_approved": "(ОДОБРЕНО)",
        "detailed_results": "Подробные результаты",
        "download_results": "📥 Скачать результаты (CSV)",
        "txn_id": "ID Txn",
        "amount": "Сумма (KZT)",
        "xgboost": "XGBoost",
        "lightgbm": "LightGBM",
        "rf": "RF",
        "no_transactions": "Ни одна транзакция не обработана успешно",
        "error_processing": "Ошибка обработки файла",
        "ensure_correct_format": "Убедитесь, что формат файла верен",
        "copyright": "© 2025 Magnat Team | Система обнаружения мошенничества",
        "powered_by": "Ансамблевые модели | XGBoost • LightGBM • Random Forest",
        "data_loading_error": "Ошибка загрузки данных",
        "ensure_files": "Убедитесь, что следующие файлы находятся в том же каталоге:",
        "file_encoding": "Оба файла должны быть закодированы в формате cp1251 и разделены точками с запятой (;)",
        "model_error": "Ошибка модели: models.pkl не найден",
        "ensure_models": "Убедитесь, что models.pkl находится в том же каталоге, что и сценарий",
    },
    "kz": {
        "title": "🛡️ FORTEBANK АЛАЯҚТЫҚТЫ БАҚЫЛАУ ДАШБОРДЫ",
        "subtitle": "Ансамбльдік машиналық оқыту | Тәуекелді нақты уақыттан бағалау",
        "total_transactions": "Жалпы транзакциялар",
        "fraud_cases": "Алаяқтық жағдайлары",
        "riskiest_hour": "Ең қауіпті сағат",
        "riskiest_day": "Ең қауіпті күн",
        "complete_dataset": "Толық деректер жиынтығы",
        "fraud_rate": "алаяқтық мөлшері",
        "fraud_risk_analysis": "АЛАЯҚТЫҚ ТӘУЕКЕЛІН ТАЛДАУ",
        "hourly_fraud_distribution": "Сағаттық тәуекел үлестірімі",
        "daily_fraud_patterns": "Күндік тәуекел үлгілері",
        "hour_of_day": "Күндің сағаты",
        "fraud_rate_percent": "Алаяқтық мөлшері (%)",
        "day_of_week": "Апта күні",
        "peak_risk_hour": "Пик тәуекел сағаты",
        "peak_risk_day": "Пик тәуекел күні",
        "detailed_risk_statistics": "ЕГЖЕЙ-ТЕГЖЕЙЛІ ТӘУЕКЕЛ СТАТИСТИКАСЫ",
        "hourly_breakdown": "Сағаттық бөлініс",
        "daily_breakdown": "Күндік бөлініс",
        "hour": "Сағат",
        "fraud_cases_col": "Алаяқтық жағдайлары",
        "total_tx": "Жалпы Tx",
        "avg_amount": "Орталық сома",
        "day": "Күн",
        "transaction_assessment": "ТРАНЗАКЦИЯНЫ БАҒАЛАУ",
        "manual_assessment": "Қолмен бағалау",
        "batch_assessment": "Топтық бағалау",
        "manual_transaction_title": "Транзакцияны қолмен тәуекелге бағалау",
        "manual_transaction_desc": "Жеке транзакцияның тәуекелін мінез-құлық және транзакциялық деректер арқылы бағалаңыз",
        "transaction_details": "Транзакция деректері",
        "amount_kzt": "Сома (KZT)",
        "date": "Күні",
        "hour_0_23": "Сағат (0-23)",
        "behavioral_data": "Мінез-құлық деректері",
        "logins_7_days": "Кірулер (7 күн)",
        "logins_30_days": "Кірулер (30 күн)",
        "os_changes_monthly": "ОС өзгерістері (ай сайын)",
        "device_activity": "Құрылғы қызметтілігі",
        "phone_changes_monthly": "Телефон өзгерістері (ай сайын)",
        "avg_interval_30d": "Орт. интервал (30 күн)",
        "std_interval_30d": "Ст. ауытқу (30 күн)",
        "advanced_parameters": "⚙️ Қосымша параметрлер",
        "frequency_7d": "Жиілігі (7 күн)",
        "frequency_30d": "Жиілігі (30 күн)",
        "freq_change_ratio": "Жиілік өзгеру қатынасы",
        "burstiness": "Дайын коэффициенті",
        "fano_factor": "Фано факторы",
        "z_score_7d": "Z-балл (7 күн)",
        "assess_risk": "Тәуекелді бағалау",
        "assessment_complete": "Бағалау аяқталды",
        "risk_level": "Тәуекел деңгейі",
        "fraud_probability": "Алаяқтық ықтималдығы",
        "status": "Күй",
        "model_probabilities": "Модель ықтималдықтары",
        "batch_title": "Топтық файлды жүктеу және өңдеу",
        "batch_desc": "CSV немесе Excel форматында бірде-бір көптеген транзакцияларды жүктеп және бағалаңыз",
        "upload_file": "Транзакция файлын жүктеңіз (CSV немесе XLSX)",
        "file_loaded": "Файл сәтті жүктелді",
        "preview_first_5": "Алдын ала қарау (алғашқы 5 қатар)",
        "file_statistics": "Файл статистикасы",
        "total_rows": "Жалпы қатарлар",
        "total_columns": "Жалпы бағаналар",
        "data_types": "Деректер түрлері",
        "missing_values": "Болмау мәндері",
        "preview_data": "Деректерді алдын ала қарау",
        "process_batch_now": "⚡ Топтықты өңдеу",
        "processing": "Транзакциялар өңделіп жатыр",
        "batch_complete": "Топтық өңдеу аяқталды",
        "summary": "Қорытынды",
        "processed_transactions": "Өңделген",
        "high_risk_blocked": "(БЛОКТАЛҒАН)",
        "low_risk_approved": "(БЕКІТІЛГЕН)",
        "detailed_results": "Егжей-тегжейлі нәтижелер",
        "download_results": "📥 Нәтижелерді жүктеу (CSV)",
        "txn_id": "Txn ID",
        "amount": "Сома (KZT)",
        "xgboost": "XGBoost",
        "lightgbm": "LightGBM",
        "rf": "RF",
        "no_transactions": "Ешқандай транзакция сәтті өңделмеді",
        "error_processing": "Файлды өңдеу қатесі",
        "ensure_correct_format": "Файл форматы дұрыс екеніне көз жеткізіңіз",
        "copyright": "© 2025 Magnat Team | Алаяқтықты анықтау жүйесі",
        "powered_by": "Ансамбьль модельдері | XGBoost • LightGBM • Random Forest",
        "data_loading_error": "Деректерді жүктеу қатесі",
        "ensure_files": "Төмендегі файлдар сценарий каталогында екеніне көз жеткізіңіз",
        "file_encoding": "Екі файл да cp1251 кодталу форматында болуы және нүктелі-үтінмен (;) бөлінуі керек",
        "model_error": "Модель қатесі: models.pkl табылмады",
        "ensure_models": "models.pkl сценарий каталогында екеніне көз жеткізіңіз",
    }
}


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
    }

    .form-section p {
        color: #2a2a2a !important;
        margin-bottom: 25px !important;
        font-size: 1em !important;
        font-weight: 600 !important;
        font-family: 'Roboto', sans-serif !important;
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

    .footer-section {
        text-align: center;
        padding: 20px !important;
        color: #2a2a2a !important;
        border-top: 2px solid #e0e0e0 !important;
        margin-top: 40px !important;
        font-weight: 600 !important;
        font-family: 'Roboto', sans-serif !important;
    }

    .plotly svg text {
        color: #000000 !important;
        fill: #000000 !important;
    }
    
    .plotly text {
        color: #000000 !important;
        fill: #000000 !important;
    }

    @media (max-width: 768px) {
        .header-section h1 {
            font-size: 2em !important;
        }
    }
    </style>
""", unsafe_allow_html=True)


# --- LANGUAGE SELECTOR IN TOP RIGHT ---
col_lang1, col_lang2 = st.columns([0.85, 0.15])
with col_lang2:
    selected_lang = st.radio(
        "🌐",
        options=["en", "ru", "kz"],
        format_func=lambda x: {"en": "EN", "ru": "РУ", "kz": "ҚЗ"}[x],
        horizontal=True,
        label_visibility="collapsed",
        key="lang_selector"
    )

t = TRANSLATIONS[selected_lang]


# --- SVG ICON DEFINITIONS ---
def get_icon_svg(icon_type, size=20):
    icons = {
        'transactions': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11H3v2h6v-2zm0-4H3v2h6V7zm6 0v2h6V7h-6zm0 4v2h6v-2h-6zM9 3H3v2h6V3zm6 0v2h6V3h-6z"></path></svg>',
        'fraud': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V9h2v4z"></path></svg>',
        'hour': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>',
        'day': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>',
        'check': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#1B5E20" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>',
        'alert_high': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#C62828" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>',
        'alert_medium': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#F57F17" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3.05h16.94a2 2 0 0 0 1.71-3.05L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
        'analytics': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="2" x2="12" y2="22"></line><path d="M17 5H9.5a1.5 1.5 0 0 0-1.5 1.5v12a1.5 1.5 0 0 0 1.5 1.5H17"></path><path d="M7 12h10"></path></svg>',
        'settings': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M12 1v6m0 6v6M4.22 4.22l4.24 4.24m5.08 5.08l4.24 4.24M1 12h6m6 0h6m-17.78 7.78l4.24-4.24m5.08-5.08l4.24-4.24"></path></svg>',
        'upload': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>',
        'shield': f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#6B1731" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
    }
    return icons.get(icon_type, '')


# --- UTILITY FUNCTIONS ---
def read_csv_with_auto_encoding(file_obj):
    encodings = ['utf-8', 'cp1251', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            file_obj.seek(0)
            return pd.read_csv(file_obj, encoding=encoding, sep=';')
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    file_obj.seek(0)
    return pd.read_csv(file_obj, sep=';')


# --- MODEL LOADING ---
@st.cache_resource
def load_models():
    try:
        with open('models.pkl', 'rb') as f:
            models = pickle.load(f)
            if "scaler" not in models:
                from sklearn.preprocessing import StandardScaler
                models["scaler"] = StandardScaler()
            if "best_threshold" not in models:
                models["best_threshold"] = 0.35
            return models
    except FileNotFoundError:
        return None


# --- DATA LOADING ---
@st.cache_data
def load_demo_data():
    try:
        trans_file = 'транзакции_в_Мобильном_интернет_Банкинге.csv'
        behavior_file = 'поведенческие_паттерны_клиентов_3.csv'
        
        transactions = pd.read_csv(trans_file, encoding='cp1251', sep=';')
        behavior = pd.read_csv(behavior_file, encoding='cp1251', sep=';')
        
        transactions.columns = [
            'cst_dim_id', 'transdate', 'transdatetime', 'amount', 'docno', 'direction', 'target'
        ]
        behavior.columns = [
            'transdate', 'cst_dim_id', 'monthly_os_changes', 'monthly_phone_model_changes',
            'last_phone_model', 'last_os', 'logins_7d', 'logins_30d', 'freq_7d', 'freq_30d',
            'freq_change_ratio', 'logins_ratio_7_30', 'avg_interval_30d', 'std_interval_30d',
            'var_interval_30d', 'ewm_interval_7d', 'burstiness', 'fano_factor', 'zscore_7d'
        ]
        
        transactions['cst_dim_id'] = pd.to_numeric(transactions['cst_dim_id'], errors='coerce')
        transactions['amount'] = pd.to_numeric(transactions['amount'], errors='coerce')
        transactions['target'] = pd.to_numeric(transactions['target'], errors='coerce')
        behavior['cst_dim_id'] = pd.to_numeric(behavior['cst_dim_id'], errors='coerce')
        
        merged = transactions.merge(behavior, on=['cst_dim_id', 'transdate'], how='left')
        merged = merged[merged['cst_dim_id'].notna()].reset_index(drop=True)
        
        for col in merged.select_dtypes(include=[np.number]).columns:
            if col not in ['cst_dim_id', 'target']:
                merged[col] = merged[col].fillna(merged[col].median())
        
        return merged
    except Exception as e:
        return pd.DataFrame()


# --- FEATURE ENGINEERING ---
def prepare_features_for_prediction(row_dict, scaler, demo_data_ref):
    try:
        amount = float(row_dict.get("amount", 0)) or 0
        hour_of_day = int(row_dict.get("hour_of_day", 12)) or 12
        day_of_week = int(row_dict.get("day_of_week", 0)) or 0
        month = int(row_dict.get("month", 6)) or 6

        logins_7d = float(row_dict.get("logins_7d", 5)) or 5
        logins_30d = float(row_dict.get("logins_30d", 20)) or 20
        freq_7d = float(row_dict.get("freq_7d", 10)) or 10
        freq_30d = float(row_dict.get("freq_30d", 25)) or 25
        freq_change_ratio = float(row_dict.get("freq_change_ratio", 0.4)) or 0.4

        monthly_os_changes = float(row_dict.get("monthly_os_changes", 0)) or 0
        monthly_phone_model_changes = float(row_dict.get("monthly_phone_model_changes", 0)) or 0
        avg_interval_30d = float(row_dict.get("avg_interval_30d", 48)) or 48
        std_interval_30d = float(row_dict.get("std_interval_30d", 12)) or 12
        burstiness = float(row_dict.get("burstiness", 0.2)) or 0.2
        fano_factor = float(row_dict.get("fano_factor", 1.5)) or 1.5
        zscore_7d = float(row_dict.get("zscore_7d", 0.5)) or 0.5

        recipient_frequency = float(row_dict.get("recipient_frequency", 1)) or 1
        client_tx_count_7d = float(row_dict.get("client_tx_count_7d", 5)) or 5
        client_tx_count_30d = float(row_dict.get("client_tx_count_30d", 20)) or 20

        amount_log = np.log1p(max(amount, 0))
        is_weekend = 1 if day_of_week >= 5 else 0
        device_instability = (monthly_os_changes + monthly_phone_model_changes) / 2
        login_surge_ratio = freq_7d / (freq_30d + 1e-5)
        is_inactive_user = 1 if logins_30d < 5 else 0
        session_interval_anomaly = 1 if abs(zscore_7d) > 2 else 0
        login_burstiness_high = 1 if burstiness > 0.3 else 0
        recent_device_change = 1 if monthly_phone_model_changes > 0 else 0

        amount_median = demo_data_ref["amount"].median() if not demo_data_ref.empty else 1000
        amount_p75 = demo_data_ref["amount"].quantile(0.75) if not demo_data_ref.empty else 3000

        device_instability_x_amount = device_instability * (1 if amount > amount_median else 0)
        inactive_x_large_tx = is_inactive_user * (1 if amount > amount_p75 else 0)
        anomaly_timing = ((1 if (hour_of_day < 8 or hour_of_day >= 17) else 0) * session_interval_anomaly)

        features = [
            amount_log, hour_of_day, is_weekend, recipient_frequency, client_tx_count_7d,
            client_tx_count_30d, device_instability, login_surge_ratio, is_inactive_user,
            session_interval_anomaly, login_burstiness_high, recent_device_change,
            monthly_os_changes, monthly_phone_model_changes, logins_7d, logins_30d,
            freq_7d, freq_change_ratio, avg_interval_30d, std_interval_30d,
            burstiness, fano_factor, zscore_7d, device_instability_x_amount,
            inactive_x_large_tx, anomaly_timing,
        ]

        dow_encoded = [1 if day_of_week == i else 0 for i in range(2, 7)]
        features.extend(dow_encoded)

        month_encoded = [1 if month == i else 0 for i in range(2, 12)]
        features.extend(month_encoded)

        if amount <= 500:
            amount_encoded = [1, 0, 0]
        elif amount <= 1500:
            amount_encoded = [0, 1, 0]
        elif amount <= 3000:
            amount_encoded = [0, 0, 1]
        else:
            amount_encoded = [0, 0, 0]
        features.extend(amount_encoded)

        X = np.array(features).reshape(1, -1)
        if scaler is not None:
            try:
                X_scaled = scaler.transform(X)
            except:
                X_scaled = X
        else:
            X_scaled = X

        return X_scaled
    except Exception as e:
        return None


# --- ENSEMBLE FRAUD PREDICTION ---
def predict_fraud_ensemble(X_scaled, models_dict):
    try:
        if X_scaled is None:
            return None

        xgb_model = models_dict.get("xgb")
        lgb_model = models_dict.get("lgb")
        rf_model = models_dict.get("rf")
        meta_learner = models_dict.get("meta_learner")
        best_threshold = models_dict.get("best_threshold", 0.35)

        if not all([xgb_model, lgb_model, rf_model, meta_learner]):
            return None

        pred_xgb = xgb_model.predict_proba(X_scaled)[:, 1][0]
        pred_lgb = lgb_model.predict_proba(X_scaled)[:, 1][0]
        pred_rf = rf_model.predict_proba(X_scaled)[:, 1][0]

        meta_input = np.array([[pred_xgb, pred_lgb, pred_rf]])
        fraud_prob = meta_learner.predict_proba(meta_input)[:, 1][0]

        if fraud_prob >= best_threshold:
            risk_level = "HIGH"
            status = "BLOCKED"
            color = "#C62828"
        else:
            risk_level = "LOW"
            status = "APPROVED"
            color = "#1B5E20"

        return {
            "fraud_probability": fraud_prob * 100,
            "risk_level": risk_level,
            "status": status,
            "color": color,
            "xgb_prob": pred_xgb * 100,
            "lgb_prob": pred_lgb * 100,
            "rf_prob": pred_rf * 100,
            "best_threshold": best_threshold * 100,
        }
    except Exception as e:
        return None


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


# --- LOAD MODELS AND DATA ---
models_dict = load_models()
demo_data = load_demo_data()


# --- MAIN LAYOUT ---
if models_dict is None:
    st.error(f"❌ {t['model_error']}")
    st.info(f"ℹ️ {t['ensure_models']}")
    st.stop()


if not demo_data.empty:
    # HEADER
    st.markdown(f"""
        <div class="header-section">
            <h1>{t['title']}</h1>
            <p>{t['subtitle']}</p>
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
                    <div class="metric-label">{get_icon_svg('transactions', 18)} {t['total_transactions']}</div>
                    <div class="metric-value">{total_tx:,}</div>
                    <div class="metric-delta">{get_icon_svg('check', 14)} {t['complete_dataset']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{get_icon_svg('alert_high', 18)} {t['fraud_cases']}</div>
                    <div class="metric-value">{int(total_fraud):,}</div>
                    <div class="metric-delta">{get_icon_svg('check', 14)} {fraud_rate:.2f}% {t['fraud_rate']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{get_icon_svg('hour', 18)} {t['riskiest_hour']}</div>
                    <div class="metric-value">{int(peak_hour['hour'])}:00</div>
                    <div class="metric-delta">{get_icon_svg('alert_medium', 14)} {peak_hour['Fraud_Rate']:.1f}% fraud</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{get_icon_svg('day', 18)} {t['riskiest_day']}</div>
                    <div class="metric-value">{peak_day['day']}</div>
                    <div class="metric-delta">{get_icon_svg('alert_medium', 14)} {peak_day['Fraud_Rate']:.1f}% fraud</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 30px 0; border: 1px solid #ddd;'>", unsafe_allow_html=True)
        
        # CHARTS
        st.markdown(f"### {get_icon_svg('analytics', 24)} {t['fraud_risk_analysis']}", unsafe_allow_html=True)
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown(f"#### {get_icon_svg('analytics', 20)} {t['hourly_fraud_distribution']}", unsafe_allow_html=True)
            hour_data = hour_stats.sort_values('hour').copy()
            colors = [get_chart_color_palette(rate) for rate in hour_data['Fraud_Rate']]
            
            fig_hourly = go.Figure(data=[
                go.Bar(
                    x=hour_data['hour'].astype(str) + ':00',
                    y=hour_data['Fraud_Rate'],
                    marker=dict(color=colors, line=dict(color='#1a1a1a', width=2)),
                    text=hour_data['Fraud_Rate'].round(2),
                    textposition='outside',
                    textfont=dict(size=11, color='#1a1a1a'),
                    hovertemplate='<b>%{x}</b><br>Fraud Rate: %{y:.2f}%<br><extra></extra>',
                    hoverlabel=dict(bgcolor='#1a1a1a', font=dict(color='white', size=12))
                )
            ])
            
            fig_hourly.update_layout(
                title=None,
                xaxis_title=f"<b style='color: #1a1a1a;'>{t['hour_of_day']}</b>",
                yaxis_title=f"<b style='color: #1a1a1a;'>{t['fraud_rate_percent']}</b>",
                hovermode='x unified',
                plot_bgcolor='#FFFFFF',
                paper_bgcolor='#FFFFFF',
                font=dict(family="Roboto, sans-serif", size=12, color="#1a1a1a"),
                margin=dict(l=60, r=60, t=40, b=60),
                height=420,
                showlegend=False,
                xaxis=dict(
                    showgrid=True, gridwidth=1, gridcolor='#e0e0e0',
                    tickfont=dict(size=11, color='#1a1a1a')
                ),
                yaxis=dict(
                    showgrid=True, gridwidth=1, gridcolor='#e0e0e0',
                    tickfont=dict(size=11, color='#1a1a1a')
                )
            )
            st.plotly_chart(fig_hourly, use_container_width=True, config={'displayModeBar': False})
            st.info(f"{t['peak_risk_hour']}: **{int(peak_hour['hour'])}:00** - {int(peak_hour['Fraud_Count'])} {t['fraud_cases_col']}")
        
        with col_chart2:
            st.markdown(f"#### {get_icon_svg('day', 20)} {t['daily_fraud_patterns']}", unsafe_allow_html=True)
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
                    textfont=dict(size=11, color='#1a1a1a'),
                    hovertemplate='<b>%{x}</b><br>Fraud Rate: %{y:.2f}%<br><extra></extra>',
                    hoverlabel=dict(bgcolor='#1a1a1a', font=dict(color='white', size=12))
                )
            ])
            
            fig_daily.update_layout(
                title=None,
                xaxis_title=f"<b style='color: #1a1a1a;'>{t['day_of_week']}</b>",
                yaxis_title=f"<b style='color: #1a1a1a;'>{t['fraud_rate_percent']}</b>",
                hovermode='x unified',
                plot_bgcolor='#FFFFFF',
                paper_bgcolor='#FFFFFF',
                font=dict(family="Roboto, sans-serif", size=12, color="#1a1a1a"),
                margin=dict(l=60, r=60, t=40, b=60),
                height=420,
                showlegend=False,
                xaxis=dict(
                    showgrid=True, gridwidth=1, gridcolor='#e0e0e0',
                    tickfont=dict(size=11, color='#1a1a1a')
                ),
                yaxis=dict(
                    showgrid=True, gridwidth=1, gridcolor='#e0e0e0',
                    tickfont=dict(size=11, color='#1a1a1a')
                )
            )
            st.plotly_chart(fig_daily, use_container_width=True, config={'displayModeBar': False})
            st.info(f"{t['peak_risk_day']}: **{peak_day['day']}** - {int(peak_day['Fraud_Count'])} {t['fraud_cases_col']}")
        
        st.markdown("<hr style='margin: 30px 0; border: 1px solid #ddd;'>", unsafe_allow_html=True)
        
        # STATISTICS TABLES
        st.markdown(f"### {get_icon_svg('analytics', 24)} {t['detailed_risk_statistics']}", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs([t['hourly_breakdown'], t['daily_breakdown']])
        
        with tab1:
            hour_display = hour_stats[['hour', 'Fraud_Count', 'Total_Count', 'Fraud_Rate', 'Avg_Amount']].copy()
            hour_display.columns = [t['hour'], t['fraud_cases_col'], t['total_tx'], f"{t['fraud_rate_percent']}", t['avg_amount']]
            hour_display[t['hour']] = hour_display[t['hour']].astype(int).astype(str) + ':00'
            st.dataframe(hour_display, use_container_width=True, hide_index=True)
        
        with tab2:
            day_display = day_stats[['day', 'Fraud_Count', 'Total_Count', 'Fraud_Rate', 'Avg_Amount']].copy()
            day_display.columns = [t['day'], t['fraud_cases_col'], t['total_tx'], f"{t['fraud_rate_percent']}", t['avg_amount']]
            st.dataframe(day_display, use_container_width=True, hide_index=True)
        
        st.markdown("<hr style='margin: 30px 0; border: 1px solid #ddd;'>", unsafe_allow_html=True)
        
        # TRANSACTION ASSESSMENT
        st.markdown(f"""
            <h2 class="section-title">{get_icon_svg('shield', 24)} {t['transaction_assessment']}</h2>
        """, unsafe_allow_html=True)
        
        assess_tab1, assess_tab2 = st.tabs([t['manual_assessment'], t['batch_assessment']])
        
        # --- MANUAL ASSESSMENT TAB ---
        with assess_tab1:
            st.markdown(f"""
                <div class="form-section">
                    <h3>{get_icon_svg('settings', 18)} {t['manual_transaction_title']}</h3>
                    <p>{t['manual_transaction_desc']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("")  # Spacing
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**{t['transaction_details']}**")
                amount = st.number_input(t['amount_kzt'], value=50000.0, min_value=0.0, step=1000.0, key="amount_manual")
                transdate = st.date_input(t['date'], value=datetime.now().date(), key="date_manual")
                hour_of_day = st.slider(t['hour_0_23'], 0, 23, 14, key="hour_manual")
            
            with col2:
                st.markdown(f"**{t['behavioral_data']}**")
                logins_7d = st.number_input(t['logins_7_days'], value=5, min_value=0, key="logins7d_manual")
                logins_30d = st.number_input(t['logins_30_days'], value=20, min_value=0, key="logins30d_manual")
                monthly_os_changes = st.number_input(t['os_changes_monthly'], value=0, min_value=0, key="oschanges_manual")
            
            with col3:
                st.markdown(f"**{t['device_activity']}**")
                monthly_phone_model_changes = st.number_input(t['phone_changes_monthly'], value=0, min_value=0, key="phonechanges_manual")
                avg_interval_30d = st.number_input(t['avg_interval_30d'], value=48.0, min_value=0.0, key="avginterval_manual")
                std_interval_30d = st.number_input(t['std_interval_30d'], value=12.0, min_value=0.0, key="stdinterval_manual")
            
            st.write("")  # Spacing before button
            
            if st.button(t['assess_risk'], use_container_width=True, key="assess_btn_manual"):
                transaction_dict = {
                    "amount": amount,
                    "hour_of_day": hour_of_day,
                    "day_of_week": transdate.weekday(),
                    "month": transdate.month,
                    "logins_7d": logins_7d,
                    "logins_30d": logins_30d,
                    "freq_7d": 10.0,
                    "freq_30d": 25.0,
                    "freq_change_ratio": 0.4,
                    "monthly_os_changes": monthly_os_changes,
                    "monthly_phone_model_changes": monthly_phone_model_changes,
                    "avg_interval_30d": avg_interval_30d,
                    "std_interval_30d": std_interval_30d,
                    "burstiness": 0.2,
                    "fano_factor": 1.5,
                    "zscore_7d": 0.5,
                    "recipient_frequency": 1,
                    "client_tx_count_7d": logins_7d,
                    "client_tx_count_30d": logins_30d,
                }
                
                X_scaled = prepare_features_for_prediction(transaction_dict, models_dict.get("scaler"), demo_data)
                if X_scaled is not None:
                    result = predict_fraud_ensemble(X_scaled, models_dict)
                    if result:
                        st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%); 
                                        border-left: 6px solid {result['color']}; 
                                        padding: 25px; border-radius: 12px; margin-top: 20px;
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); font-family: 'Roboto', sans-serif;">
                                <h3 style="color: {result['color']}; margin-bottom: 15px; font-family: 'Roboto', sans-serif;">{t['assessment_complete']}</h3>
                                <p style="color: #2a2a2a; font-family: 'Roboto', sans-serif;"><strong>{t['risk_level']}:</strong> <span style="color: {result['color']}; font-size: 1.3em; font-weight: 800; font-family: 'Roboto', sans-serif;">{result['risk_level']}</span></p>
                                <p style="color: #2a2a2a; font-family: 'Roboto', sans-serif;"><strong>{t['fraud_probability']}:</strong> <span style="font-weight: 700; color: {result['color']}; font-family: 'Roboto', sans-serif;">{result['fraud_probability']:.1f}%</span></p>
                                <p style="color: #2a2a2a; font-family: 'Roboto', sans-serif;"><strong>{t['status']}:</strong> <span style="font-weight: 800; color: {result['color']}; font-family: 'Roboto', sans-serif;">⚡ {result['status']}</span></p>
                                <p style="color: #666; font-family: 'Roboto', sans-serif; font-size: 0.9em; margin-top: 15px;">
                                    <strong>{t['model_probabilities']}:</strong> {t['xgboost']}: {result['xgb_prob']:.1f}% | {t['lightgbm']}: {result['lgb_prob']:.1f}% | {t['rf']}: {result['rf_prob']:.1f}%
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
            
            st.write("")  # Spacing before expander
            with st.expander(t['advanced_parameters']):
                st.write("")  # Spacing inside expander
                col1_adv, col2_adv, col3_adv = st.columns(3)
                with col1_adv:
                    st.number_input(t['frequency_7d'], value=10.0, step=0.1, key="f7", disabled=True)
                    st.number_input(t['frequency_30d'], value=25.0, step=0.1, key="f30", disabled=True)
                with col2_adv:
                    st.number_input(t['freq_change_ratio'], value=0.4, step=0.1, key="fcr", disabled=True)
                    st.number_input(t['burstiness'], value=0.2, step=0.1, key="burst", disabled=True)
                with col3_adv:
                    st.number_input(t['fano_factor'], value=1.5, step=0.1, key="fano", disabled=True)
                    st.slider(t['z_score_7d'], -3.0, 3.0, 0.5, key="z", disabled=True)
                st.info("ℹ️ These parameters are pre-set from demo data. To customize, edit transaction details above.")
        
        # --- BATCH ASSESSMENT TAB ---
        with assess_tab2:
            st.markdown(f"""
                <div class="form-section">
                    <h3>{get_icon_svg('upload', 18)} {t['batch_title']}</h3>
                    <p>{t['batch_desc']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("")  # Spacing
            uploaded_file = st.file_uploader(t['upload_file'], type=['csv', 'xlsx'], key="batch_uploader")
            
            if uploaded_file:
                st.success(f"✅ {t['file_loaded']}: **{uploaded_file.name}**")
                st.write("")  # Spacing
                
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = read_csv_with_auto_encoding(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    col_s1, col_s2, col_s3 = st.columns(3)
                    with col_s1:
                        st.metric(t['total_rows'], len(df))
                    with col_s2:
                        st.metric(t['total_columns'], len(df.columns))
                    with col_s3:
                        st.metric(t['missing_values'], df.isnull().sum().sum())
                    
                    st.write("")  # Spacing
                    
                    if st.button(t['process_batch_now'], use_container_width=True, key="process_btn"):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        results = []
                        total_rows = len(df)
                        
                        for idx, row in df.iterrows():
                            try:
                                row_dict = {
                                    "amount": float(row.get("amount", 50000)) if "amount" in row else 50000,
                                    "hour_of_day": int(row.get("hour", 12)) if "hour" in row else 12,
                                    "day_of_week": int(row.get("day_of_week", 0)) if "day_of_week" in row else 0,
                                    "month": int(row.get("month", 6)) if "month" in row else 6,
                                    "logins_7d": float(row.get("logins_7d", 5)) if "logins_7d" in row else 5,
                                    "logins_30d": float(row.get("logins_30d", 20)) if "logins_30d" in row else 20,
                                    "freq_7d": float(row.get("freq_7d", 10)) if "freq_7d" in row else 10,
                                    "freq_30d": float(row.get("freq_30d", 25)) if "freq_30d" in row else 25,
                                    "freq_change_ratio": float(row.get("freq_change_ratio", 0.4)) if "freq_change_ratio" in row else 0.4,
                                    "monthly_os_changes": float(row.get("monthly_os_changes", 0)) if "monthly_os_changes" in row else 0,
                                    "monthly_phone_model_changes": float(row.get("monthly_phone_model_changes", 0)) if "monthly_phone_model_changes" in row else 0,
                                    "avg_interval_30d": float(row.get("avg_interval_30d", 48)) if "avg_interval_30d" in row else 48,
                                    "std_interval_30d": float(row.get("std_interval_30d", 12)) if "std_interval_30d" in row else 12,
                                    "burstiness": float(row.get("burstiness", 0.2)) if "burstiness" in row else 0.2,
                                    "fano_factor": float(row.get("fano_factor", 1.5)) if "fano_factor" in row else 1.5,
                                    "zscore_7d": float(row.get("zscore_7d", 0.5)) if "zscore_7d" in row else 0.5,
                                    "recipient_frequency": float(row.get("recipient_frequency", 1)) if "recipient_frequency" in row else 1,
                                    "client_tx_count_7d": float(row.get("client_tx_count_7d", 5)) if "client_tx_count_7d" in row else 5,
                                    "client_tx_count_30d": float(row.get("client_tx_count_30d", 20)) if "client_tx_count_30d" in row else 20,
                                }
                                
                                X_scaled = prepare_features_for_prediction(row_dict, models_dict.get("scaler"), demo_data)
                                
                                if X_scaled is not None:
                                    prediction = predict_fraud_ensemble(X_scaled, models_dict)
                                    
                                    if prediction:
                                        results.append({
                                            t['txn_id']: f'TXN{idx+1:04d}',
                                            t['amount']: f'{row_dict["amount"]:,.0f}',
                                            t['risk_level']: prediction['risk_level'],
                                            t['fraud_probability']: f"{prediction['fraud_probability']:.1f}%",
                                            t['status']: prediction['status'],
                                            t['xgboost']: f"{prediction['xgb_prob']:.1f}%",
                                            t['lightgbm']: f"{prediction['lgb_prob']:.1f}%",
                                            t['rf']: f"{prediction['rf_prob']:.1f}%",
                                        })
                            except Exception:
                                pass
                            
                            progress = (idx + 1) / total_rows
                            progress_bar.progress(progress)
                            status_text.text(f"{t['processing']}... {idx + 1}/{total_rows}")
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        if len(results) > 0:
                            results_df = pd.DataFrame(results)
                            
                            high_count = len([r for r in results if 'HIGH' in r[t['risk_level']]])
                            low_count = len([r for r in results if 'LOW' in r[t['risk_level']]])
                            
                            st.write("")  # Spacing
                            st.success(f"✅ {t['batch_complete']}\n\n**{t['summary']}:** {len(results)} {t['processed_transactions']}\n- 🔴 {t['high_risk_blocked']}: {high_count}\n- 🟢 {t['low_risk_approved']}: {low_count}")
                            
                            st.write("")  # Spacing
                            st.dataframe(results_df, use_container_width=True, hide_index=True)
                            
                            csv = results_df.to_csv(index=False)
                            st.download_button(
                                label=t['download_results'],
                                data=csv,
                                file_name="fraud_assessment_results.csv",
                                mime="text/csv",
                                key="download_btn",
                                use_container_width=True
                            )
                        else:
                            st.error(f"❌ {t['no_transactions']}")
                
                except Exception as e:
                    st.error(f"{t['error_processing']}: {str(e)}\n\n{t['ensure_correct_format']}")
        
        st.markdown("<hr style='margin: 30px 0; border: 1px solid #ddd;'>", unsafe_allow_html=True)
        
        # FOOTER
        st.markdown(f"""
            <div class="footer-section">
                <p><strong>{t['copyright']}</strong></p>
                <p style="font-size: 0.9em; margin-top: 5px; color: #2a2a2a; font-family: 'Roboto', sans-serif;">{t['powered_by']}</p>
            </div>
        """, unsafe_allow_html=True)

else:
    st.error(t['data_loading_error'])
    st.info(f"ℹ️ {t['ensure_files']}\n- транзакции_в_Мобильном_интернет_Банкинге.csv\n- поведенческие_паттерны_клиентов_3.csv\n\n{t['file_encoding']}")
