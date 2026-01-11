# 📊 Automated Data Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b?logo=streamlit)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-150458?logo=pandas)](https://pandas.pydata.pydata.org/)

A professional data analytics platform built with Python and Streamlit, automating the EDA process, smart data cleaning, and interactive insights visualization. This project focuses on a **code-heavy** approach to optimize analytical performance.

---

## 💡 Key Analytical Insights
*This project distinguishes itself by its ability to extract immediate value from raw data:*

* **Income Paradox Detection:** Through the Correlation Matrix, the system identified a **0.85** correlation between `Years of Experience` and `Salary`, confirming the organization's seniority-based pay scale.
* **Outlier Isolation:** Utilizes the **IQR algorithm** to isolate anomalous data points (e.g., identifying executive salaries vs. staff averages).
* **Smart Imputation:** Automatically distinguishes and applies Mean/Median for numerical data and **Mode** for categorical data, ensuring post-cleaning data integrity.

---

## ✨ Core Features

### 🧹 Smart Data Cleaning
* **Auto-reset Logic:** Automatically refreshes the application state (Session State) upon new file uploads for data consistency.
* **Multi-level Missing Value Handling:** * **Quantitative:** Imputation via Mean/Median to prevent distribution skew.
  * **Qualitative:** Imputation via Mode for categorical columns (e.g., Department, City).
* **Smart Type Conversion:** Detects and corrects formatting errors (e.g., numbers stored as strings).

### 📊 Interactive Visualization (Plotly-powered)
* **Correlation Heatmap:** Visual matrix to identify relationships between variables.
* **Interactive Charts:** Scatter, Bar, and Box Plots with real-time zoom, hover, and filtering capabilities.
* **AI Chart Suggestion:** Recommends the most suitable visualization based on data characteristics.

### 🎯 Advanced Statistical Analysis
* **IQR-based Outlier Detection:** Defines statistical boundaries and lists specific anomalous records.
* **Comprehensive Stats:** Provides a holistic view of distribution, skewness, and central tendency measures.

---

## 🛠️ Tech Stack
* **Language:** Python (Pure code logic)
* **Core Libraries:** Pandas, NumPy, Streamlit, Plotly, Seaborn.
* **Deployment:** Streamlit Cloud.

---

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/phucthinh-ng/automated-data-analytics-platform.git](https://github.com/phucthinh-ng/automated-data-analytics-platform.git)

2. **Environment Setup:**
   ```bash
   pip install -r requirements.txt
3. **Run the App:**
   ```bash
   streamlit run app.py
👤 Author Information
Name: Nguyen Phuc Thinh

Role: Data Analyst / Developer

Skills: Python, DA, SQL, English

GitHub: phucthinh-ng

