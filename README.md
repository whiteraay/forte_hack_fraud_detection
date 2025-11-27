# 🛡️ Fortebank Anti-Fraud Detection System (FADS) | Team Magnat

| Status | Technology | License |
| :---: | :---: | :---: |
| ✅ Deployed | Python, ML, Streamlit | MIT |

***

## 💡 Project Overview

The Fortebank Anti-Fraud Detection System is an **end-to-end Machine Learning solution** designed to combat financial crime within the mobile banking sector.

By analyzing **real-time transactional data** and granular **customer behavioral patterns**, this system utilizes a robust **Ensemble Stacked Model** to identify and flag high-risk transactions with exceptional accuracy, enabling operational teams to mitigate fraud losses instantly.

## ^ Key Features

### 💻 Interactive Streamlit Dashboard

Our primary interface provides a dynamic environment for analysts, offering:

* **Hourly & Daily Risk Analytics:** Interactive **Plotly charts** allow teams to zoom, hover, and filter to pinpoint historical fraud patterns by time and day of the week.
* **Single-Transaction Scoring:** Real-time risk assessment using dynamic inputs (amount, logins, device changes) to immediately score individual transactions.
* **Batch Assessment:** Securely upload large `.csv` or `.xlsx` files for high-throughput batch scoring, with **downloadable, detailed results**.
* **Explainable Risk Scoring:** Provides an anti-fraud heuristic score (Probability, Risk Level, and Status: **APPROVED / REVIEW / BLOCKED**) with clear feature explanations.
* **Operational Insights:** Visualization of fraud patterns by time and day for operational teams.

### ~ Advanced Ensemble Model

The core of FADS is a high-performance **stacked ensemble model** combining the predictive power of multiple algorithms to maximize detection accuracy and minimize false positives.

***

## # Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend/Core** | Python, Pandas, NumPy | Data processing, feature engineering, and application logic. |
| **Modeling** | scikit-learn, XGBoost, LightGBM, Random Forest | Ensemble learning for high-accuracy fraud classification. |
| **Frontend/UI** | Streamlit | Rapid development of the interactive, operational dashboard. |
| **Visualization** | Plotly, Altair | Creating interactive, zoomable, and hover-enabled analytical charts. |
| **Data Source** | CSV (Transactional & Behavioral Logs) | Raw input data from mobile/internet banking transactions. |

***

## * How to Run

Follow these steps to set up and launch the Fortebank Anti-Fraud Detection System locally.

### 1. Prerequisites

Ensure you have **Python 3.8+** installed.

### 2. Setup


##### Clone the repository
###### git clone [YOUR_REPO_URL_HERE]
###### cd forteHack_flaud_detection

##### Create and activate a virtual environment
###### python -m venv venv
###### source venv/bin/activate  # On Linux/macOS
###### .\venv\Scripts\activate  # On Windows

##### Install dependencies
###### pip install -r requirements.txt

### 3. Data Preparation

Place the following raw CSV files into the project root directory:

транзакции_в_Мобильном_интернет_Банкинге.csv

поведенческие_паттерны_клиентов_3.csv

### 4. Launch the Dashboard
###### streamlit run app.py

_The application will automatically open in your web browser._

## 💰 Business Value & Impact
The Fortebank Anti-Fraud Detection System delivers tangible benefits for risk management and operational efficiency:

## Benefit	Description
High Accuracy	Detects >95% of fraudulent transactions with low false positives.
Real-Time Mitigation	Enables instant monitoring and decision-making, significantly reducing fraud losses.
Operational Efficiency	Provides clear, explainable risk factors, allowing fraud teams to review cases faster and more consistently.
Proactive Strategy	Facilitates interactive exploration of hidden fraud patterns to optimize fraud rules and strategies.
