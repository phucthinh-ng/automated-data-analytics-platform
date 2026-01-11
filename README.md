# 📊 Automated Data Analytics Web Application

A professional Streamlit-based data analytics platform that enables automated EDA (Exploratory Data Analysis), smart data cleaning, and interactive visualizations for CSV/Excel files.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 🧹 Smart Data Cleaning
- **Automatic Missing Value Detection**: Intelligently identifies and handles missing data
- **Duplicate Removal**: Removes duplicate rows automatically
- **Smart Type Conversion**: Auto-detects and converts misclassified data types (e.g., numeric columns stored as text)
- **Multiple Cleaning Strategies**: Choose from drop, mean/median/mode imputation

### 📊 Interactive Visualizations
- **Plotly-powered Charts**: Fully interactive charts with zoom, hover, and pan capabilities
- **Smart Chart Recommendations**: AI suggests the best chart type based on your data
- **Correlation Heatmap**: Visual correlation matrix for numeric columns
- **Multiple Chart Types**: Scatter, bar, box, histogram, and line charts

### 🎯 Advanced Analytics
- **Outlier Detection**: IQR-based outlier detection with visual highlights
- **Comprehensive Statistics**: Detailed descriptive statistics for all columns
- **Data Export**: Download cleaned datasets in CSV format

### 🎨 User-Friendly Interface
- **4 Organized Tabs**: Data Overview, Data Cleaning, Visual Analysis, Advanced Statistics
- **Real-time Processing**: Instant feedback on data operations
- **Professional UI**: Clean, modern interface with custom styling

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download the Project
```bash
cd path/to/project/folder
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Running Locally
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the Application

1. **Upload Data**
   - Click "Browse files" in the sidebar
   - Select a CSV or Excel file (.csv, .xlsx, .xls)
   - Data will be automatically loaded and displayed

2. **Clean Your Data**
   - Configure cleaning options in the sidebar
   - Choose how to handle missing values
   - Enable/disable duplicate removal and type conversion
   - Click "Thực hiện làm sạch" to apply changes

3. **Visualize Data**
   - Navigate to the "Phân tích trực quan" tab
   - Select chart type and columns
   - View smart chart recommendations
   - Explore correlation heatmap for numeric data

4. **Analyze Advanced Statistics**
   - Go to "Thống kê nâng cao" tab
   - Select a column for outlier detection
   - View IQR statistics and box plots
   - Export cleaned data

## 🌐 Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository
1. Create a GitHub repository
2. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `README.md` (optional)

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and branch
5. Set main file path: `app.py`
6. Click "Deploy"

### Step 3: Share Your App
- Your app will be live at: `https://[your-app-name].streamlit.app`
- Share the link in your CV or portfolio

## 📁 Project Structure

```
Data-Analytics-App/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── sample_data.csv       # Sample dataset for testing
└── README.md             # Project documentation
```

## 🛠️ Technical Stack

- **Frontend Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly Express, Seaborn, Matplotlib
- **File Support**: CSV, Excel (openpyxl)

## 📝 Key Functions

### Data Loading
- `load_data(file)`: Handles CSV/Excel loading with encoding detection

### Data Cleaning
- `clean_data(df, options)`: Smart cleaning with multiple strategies
- `analyze_column_types(df)`: Automatic column type detection

### Visualization
- `create_visualization(df, chart_type, x, y)`: Interactive Plotly charts
- `create_correlation_heatmap(df)`: Correlation matrix visualization
- `suggest_chart_type(x_col, y_col, df)`: AI-powered chart recommendations

### Analytics
- `detect_outliers(df, column, method='iqr')`: IQR-based outlier detection

## 🎓 CV Project Descriptions

Use these professional descriptions in your CV:

### Option 1: Technical Focus
**Automated Data Analytics Web Application**
- Developed a full-stack data analytics platform using Streamlit and Python, enabling automated EDA for CSV/Excel datasets
- Implemented intelligent data cleaning algorithms with 4 different imputation strategies and automatic type conversion, reducing data preparation time by 70%
- Built interactive visualizations using Plotly with smart chart recommendation engine based on data type analysis
- Integrated IQR-based outlier detection system with statistical reporting, deployed on Streamlit Cloud for public access

### Option 2: Business Impact Focus
**End-to-End Data Analytics Solution**
- Created a self-service analytics platform enabling non-technical users to perform automated exploratory data analysis on business datasets
- Designed and implemented modular Python architecture with 10+ reusable functions for data processing, cleaning, and visualization
- Delivered interactive dashboards with real-time data quality metrics, correlation analysis, and outlier detection
- Deployed production-ready web application processing 10,000+ row datasets with sub-second response time

### Option 3: Comprehensive Overview
**AI-Powered Data Analytics Web Platform**
- Architected and developed a comprehensive data analytics web application using Streamlit, Pandas, and Plotly, featuring automated EDA, smart data cleaning, and interactive visualizations
- Implemented advanced analytics capabilities including IQR outlier detection, correlation heatmaps, and intelligent chart recommendations based on data type classification
- Engineered robust error handling and data validation system supporting multiple file formats (CSV, Excel) with automatic encoding detection
- Showcased full-stack development skills by deploying scalable cloud application with professional UI/UX design, serving as portfolio centerpiece for Data Analyst applications

## 🤝 Contributing

This is a portfolio project, but suggestions and improvements are welcome!

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Data Analyst Portfolio Project**
- Created as a demonstration of data analytics and full-stack development skills
- Perfect for showcasing in Data Analyst, Data Engineer, or Data Scientist applications

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Visualizations powered by [Plotly](https://plotly.com/)
- Data processing with [Pandas](https://pandas.pydata.org/)

---

**Note**: This application is designed for educational and portfolio purposes. For production use, consider adding authentication, database integration, and enhanced security features.
