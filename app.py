"""
Automated Data Analytics Web Application
=========================================
Ứng dụng phân tích dữ liệu tự động với Streamlit
Author: Data Analyst Portfolio Project
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
import warnings
warnings.filterwarnings('ignore')

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Automated Data Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==================== UTILITY FUNCTIONS ====================

@st.cache_data
def load_data(file):
    """
    Load CSV or Excel file with error handling
    
    Args:
        file: Uploaded file object from Streamlit
    
    Returns:
        pd.DataFrame: Loaded dataframe or None if error
    """
    try:
        if file.name.endswith('.csv'):
            # Try different encodings
            try:
                df = pd.read_csv(file, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file, encoding='latin-1')
        elif file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        else:
            st.error("❌ Định dạng file không được hỗ trợ. Vui lòng upload file CSV hoặc Excel.")
            return None
        
        return df
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc file: {str(e)}")
        return None


def analyze_column_types(df):
    """
    Phân tích và phân loại các cột trong dataframe
    
    Returns:
        dict: Dictionary chứa các loại cột khác nhau
    """
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    return {
        'numeric': numeric_cols,
        'categorical': categorical_cols,
        'datetime': datetime_cols
    }


def clean_data(df, remove_duplicates=True, handle_missing='drop', convert_types=True):
    """
    Smart data cleaning function with enhanced categorical support
    
    Args:
        df: Input dataframe
        remove_duplicates: Có xóa dữ liệu trùng lặp không
        handle_missing: Cách xử lý missing values ('drop', 'fill_mean', 'fill_median', 'fill_mode')
        convert_types: Tự động chuyển đổi kiểu dữ liệu
    
    Returns:
        pd.DataFrame: Cleaned dataframe
        dict: Cleaning statistics with warnings
    """
    df_cleaned = df.copy()
    stats = {
        'original_rows': len(df),
        'original_cols': len(df.columns),
        'duplicates_removed': 0,
        'missing_handled': 0,
        'types_converted': 0,
        'warnings': []
    }
    
    # 1. Remove duplicates
    if remove_duplicates:
        before = len(df_cleaned)
        df_cleaned = df_cleaned.drop_duplicates()
        stats['duplicates_removed'] = before - len(df_cleaned)
    
    # 2. Handle missing values
    if handle_missing == 'drop':
        before = len(df_cleaned)
        df_cleaned = df_cleaned.dropna()
        stats['missing_handled'] = before - len(df_cleaned)
    
    elif handle_missing == 'fill_mean':
        # Only apply to numeric columns
        numeric_cols = df_cleaned.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols_with_nulls = df_cleaned.select_dtypes(include=['object', 'category']).columns[
            df_cleaned.select_dtypes(include=['object', 'category']).isnull().any()
        ].tolist()
        
        for col in numeric_cols:
            if df_cleaned[col].isnull().any():
                df_cleaned[col].fillna(df_cleaned[col].mean(), inplace=True)
                stats['missing_handled'] += 1
        
        # Warning for categorical columns
        if categorical_cols_with_nulls:
            stats['warnings'].append(
                f"⚠️ Phương pháp 'Mean' không áp dụng cho cột dạng chữ: {', '.join(categorical_cols_with_nulls)}. "
                f"Các cột này vẫn còn giá trị thiếu."
            )
    
    elif handle_missing == 'fill_median':
        # Only apply to numeric columns
        numeric_cols = df_cleaned.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols_with_nulls = df_cleaned.select_dtypes(include=['object', 'category']).columns[
            df_cleaned.select_dtypes(include=['object', 'category']).isnull().any()
        ].tolist()
        
        for col in numeric_cols:
            if df_cleaned[col].isnull().any():
                df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)
                stats['missing_handled'] += 1
        
        # Warning for categorical columns
        if categorical_cols_with_nulls:
            stats['warnings'].append(
                f"⚠️ Phương pháp 'Median' không áp dụng cho cột dạng chữ: {', '.join(categorical_cols_with_nulls)}. "
                f"Các cột này vẫn còn giá trị thiếu."
            )
    
    elif handle_missing == 'fill_mode':
        # Apply to ALL columns (both numeric and categorical)
        numeric_filled = 0
        categorical_filled = 0
        
        for col in df_cleaned.columns:
            if df_cleaned[col].isnull().any():
                mode_val = df_cleaned[col].mode()
                if not mode_val.empty:
                    df_cleaned[col].fillna(mode_val[0], inplace=True)
                    stats['missing_handled'] += 1
                    
                    # Track what type of column was filled
                    if df_cleaned[col].dtype in ['int64', 'float64']:
                        numeric_filled += 1
                    else:
                        categorical_filled += 1
        
        if categorical_filled > 0:
            stats['warnings'].append(
                f"ℹ️ Đã điền {categorical_filled} cột dạng chữ và {numeric_filled} cột số bằng giá trị phổ biến nhất (Mode)."
            )
    
    # 3. Auto convert data types (detect numeric columns stored as strings)
    if convert_types:
        for col in df_cleaned.select_dtypes(include=['object']).columns:
            # Try to convert to numeric
            try:
                converted = pd.to_numeric(df_cleaned[col], errors='coerce')
                # If more than 80% can be converted, it's probably numeric
                if converted.notna().sum() / len(df_cleaned) > 0.8:
                    df_cleaned[col] = converted
                    stats['types_converted'] += 1
            except:
                pass
    
    stats['final_rows'] = len(df_cleaned)
    stats['final_cols'] = len(df_cleaned.columns)
    
    return df_cleaned, stats


def detect_outliers(df, column, method='iqr'):
    """
    Detect outliers using IQR method
    
    Args:
        df: Input dataframe
        column: Column name to check for outliers
        method: Detection method (currently supports 'iqr')
    
    Returns:
        pd.DataFrame: Dataframe with outlier information
        dict: Outlier statistics
    """
    if column not in df.columns or df[column].dtype not in ['int64', 'float64']:
        return None, None
    
    data = df[column].dropna()
    
    if method == 'iqr':
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers_mask = (df[column] < lower_bound) | (df[column] > upper_bound)
        outliers_df = df[outliers_mask].copy()
        outliers_df['outlier_reason'] = outliers_df[column].apply(
            lambda x: f"Below {lower_bound:.2f}" if x < lower_bound else f"Above {upper_bound:.2f}"
        )
        
        stats = {
            'total_values': len(data),
            'outliers_count': len(outliers_df),
            'outliers_percentage': (len(outliers_df) / len(data)) * 100,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR
        }
        
        return outliers_df, stats
    
    return None, None


def suggest_chart_type(x_col, y_col, df):
    """
    Gợi ý loại biểu đồ phù hợp dựa trên kiểu dữ liệu
    
    Returns:
        str: Loại biểu đồ được gợi ý
    """
    col_types = analyze_column_types(df)
    
    x_is_numeric = x_col in col_types['numeric']
    y_is_numeric = y_col in col_types['numeric'] if y_col else False
    
    if y_col is None:
        # Single column analysis
        if x_is_numeric:
            return 'histogram'
        else:
            return 'bar'
    else:
        # Two column analysis
        if x_is_numeric and y_is_numeric:
            return 'scatter'
        elif not x_is_numeric and y_is_numeric:
            return 'box'
        elif x_is_numeric and not y_is_numeric:
            return 'box'
        else:
            return 'bar'


def create_visualization(df, chart_type, x_col, y_col=None, color_col=None):
    """
    Tạo biểu đồ tương tác với Plotly
    
    Returns:
        plotly.graph_objects.Figure: Interactive chart
    """
    try:
        if chart_type == 'scatter':
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                           title=f"{y_col} vs {x_col}",
                           template='plotly_white',
                           hover_data=df.columns)
        elif chart_type == 'bar':
            if y_col:
                fig = px.bar(df, x=x_col, y=y_col, color=color_col,
                           title=f"{y_col} by {x_col}",
                           template='plotly_white')
            else:
                value_counts = df[x_col].value_counts().reset_index()
                value_counts.columns = [x_col, 'count']
                fig = px.bar(value_counts, x=x_col, y='count',
                           title=f"Distribution of {x_col}",
                           template='plotly_white')
        elif chart_type == 'box':
            fig = px.box(df, x=x_col, y=y_col, color=color_col,
                        title=f"{y_col} Distribution by {x_col}",
                        template='plotly_white')
        elif chart_type == 'histogram':
            fig = px.histogram(df, x=x_col, color=color_col,
                             title=f"Distribution of {x_col}",
                             template='plotly_white')
        elif chart_type == 'line':
            fig = px.line(df, x=x_col, y=y_col, color=color_col,
                         title=f"{y_col} over {x_col}",
                         template='plotly_white')
        else:
            return None
        
        fig.update_layout(
            height=500,
            hovermode='closest',
            showlegend=True
        )
        
        return fig
    except Exception as e:
        st.error(f"❌ Lỗi khi tạo biểu đồ: {str(e)}")
        return None


def create_correlation_heatmap(df):
    """
    Tạo correlation heatmap cho các cột numeric
    
    Returns:
        plotly.graph_objects.Figure: Heatmap
    """
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    
    if len(numeric_df.columns) < 2:
        return None
    
    corr_matrix = numeric_df.corr()
    
    fig = px.imshow(corr_matrix,
                    text_auto='.2f',
                    aspect='auto',
                    color_continuous_scale='RdBu_r',
                    title='Ma trận tương quan (Correlation Matrix)',
                    labels=dict(color="Correlation"))
    
    fig.update_layout(height=600)
    
    return fig


def convert_df_to_csv(df):
    """
    Convert dataframe to CSV for download
    """
    return df.to_csv(index=False).encode('utf-8')


# ==================== MAIN APPLICATION ====================

def main():
    # Header
    st.markdown('<div class="main-header">📊 Automated Data Analytics Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Phân tích dữ liệu tự động với AI-powered insights</div>', unsafe_allow_html=True)
    
    # ==================== SIDEBAR ====================
    with st.sidebar:
        st.header("⚙️ Cấu hình")
        
        # File upload
        st.subheader("📁 Upload Dữ liệu")
        uploaded_file = st.file_uploader(
            "Chọn file CSV hoặc Excel",
            type=['csv', 'xlsx', 'xls'],
            help="Hỗ trợ định dạng: CSV, Excel (.xlsx, .xls)"
        )
        
        # Initialize session state
        if 'df_original' not in st.session_state:
            st.session_state.df_original = None
        if 'df_cleaned' not in st.session_state:
            st.session_state.df_cleaned = None
        if 'cleaning_stats' not in st.session_state:
            st.session_state.cleaning_stats = None
        if 'last_uploaded_file' not in st.session_state:
            st.session_state.last_uploaded_file = None
        
        # Load data and auto-reset on new file
        if uploaded_file is not None:
            # Check if this is a new file
            current_file_name = uploaded_file.name
            
            if st.session_state.last_uploaded_file != current_file_name:
                # New file detected - reset cleaned data
                st.session_state.df_cleaned = None
                st.session_state.cleaning_stats = None
                st.session_state.last_uploaded_file = current_file_name
                
                # Load the new file
                df = load_data(uploaded_file)
                if df is not None:
                    st.session_state.df_original = df
                    st.success(f"✅ Đã tải {len(df)} dòng, {len(df.columns)} cột")
            elif st.session_state.df_original is None:
                # First time loading
                df = load_data(uploaded_file)
                if df is not None:
                    st.session_state.df_original = df
                    st.success(f"✅ Đã tải {len(df)} dòng, {len(df.columns)} cột")
        
        # Data cleaning options (only show if data is loaded)
        if st.session_state.df_original is not None:
            st.divider()
            st.subheader("🧹 Tùy chọn làm sạch")
            
            remove_dupes = st.checkbox("Xóa dữ liệu trùng lặp", value=True)
            
            missing_method = st.selectbox(
                "Xử lý giá trị thiếu",
                options=['drop', 'fill_mean', 'fill_median', 'fill_mode'],
                format_func=lambda x: {
                    'drop': 'Xóa dòng có giá trị thiếu',
                    'fill_mean': 'Điền giá trị trung bình (chỉ số)',
                    'fill_median': 'Điền giá trị trung vị (chỉ số)',
                    'fill_mode': 'Điền giá trị phổ biến nhất (số & chữ)'
                }[x]
            )
            
            auto_convert = st.checkbox("Tự động chuyển đổi kiểu dữ liệu", value=True)
            
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                clean_btn = st.button("🚀 Clean", type="primary", use_container_width=True)
            with col2:
                reset_btn = st.button("🔄 Reset", type="secondary", use_container_width=True)
            
            if clean_btn:
                with st.spinner("Đang xử lý..."):
                    df_cleaned, stats = clean_data(
                        st.session_state.df_original,
                        remove_duplicates=remove_dupes,
                        handle_missing=missing_method,
                        convert_types=auto_convert
                    )
                    st.session_state.df_cleaned = df_cleaned
                    st.session_state.cleaning_stats = stats
                    st.success("✅ Hoàn thành!")
                    
                    # Show warnings if any
                    if stats.get('warnings'):
                        for warning in stats['warnings']:
                            st.warning(warning)
            
            if reset_btn:
                st.session_state.df_cleaned = None
                st.session_state.cleaning_stats = None
                st.success("✅ Đã reset về dữ liệu gốc!")
                st.rerun()
    
    # ==================== MAIN CONTENT ====================
    if st.session_state.df_original is None:
        # Welcome screen
        st.info("👈 Vui lòng upload file dữ liệu từ sidebar để bắt đầu phân tích")
        
        st.markdown("### ✨ Tính năng nổi bật")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🧹 Smart Cleaning**
            - Tự động phát hiện missing values
            - Loại bỏ dữ liệu trùng lặp
            - Chuyển đổi kiểu dữ liệu thông minh
            """)
        
        with col2:
            st.markdown("""
            **📊 Interactive Charts**
            - Biểu đồ tương tác với Plotly
            - Gợi ý biểu đồ tự động
            - Ma trận tương quan
            """)
        
        with col3:
            st.markdown("""
            **🎯 Advanced Analytics**
            - Phát hiện outliers (IQR)
            - Thống kê mô tả chi tiết
            - Xuất dữ liệu đã làm sạch
            """)
        
        return
    
    # Get working dataframe
    df_work = st.session_state.df_cleaned if st.session_state.df_cleaned is not None else st.session_state.df_original
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Tổng quan dữ liệu",
        "🧹 Làm sạch dữ liệu", 
        "📊 Phân tích trực quan",
        "🎯 Thống kê nâng cao"
    ])
    
    # ==================== TAB 1: DATA OVERVIEW ====================
    with tab1:
        st.header("📋 Tổng quan dữ liệu")
        
        # Basic metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Số dòng", f"{len(df_work):,}")
        with col2:
            st.metric("Số cột", len(df_work.columns))
        with col3:
            st.metric("Giá trị thiếu", f"{df_work.isnull().sum().sum():,}")
        with col4:
            memory_mb = df_work.memory_usage(deep=True).sum() / 1024**2
            st.metric("Bộ nhớ", f"{memory_mb:.2f} MB")
        
        st.divider()
        
        # Column types
        col_types = analyze_column_types(df_work)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Phân loại cột")
            st.write(f"**Numeric:** {len(col_types['numeric'])} cột")
            st.write(f"**Categorical:** {len(col_types['categorical'])} cột")
            st.write(f"**Datetime:** {len(col_types['datetime'])} cột")
        
        with col2:
            st.subheader("🔍 Thông tin chi tiết")
            buffer = StringIO()
            df_work.info(buf=buffer)
            st.text(buffer.getvalue())
        
        st.divider()
        
        # Data preview
        st.subheader("👀 Xem trước dữ liệu")
        st.dataframe(df_work.head(20), use_container_width=True)
        
        # Basic statistics
        st.subheader("📈 Thống kê mô tả")
        st.dataframe(df_work.describe(), use_container_width=True)
    
    # ==================== TAB 2: DATA CLEANING ====================
    with tab2:
        st.header("🧹 Làm sạch dữ liệu")
        
        if st.session_state.df_cleaned is not None:
            # Show cleaning statistics
            stats = st.session_state.cleaning_stats
            
            st.success("✅ Dữ liệu đã được làm sạch!")
            
            # Display warnings if any
            if stats.get('warnings'):
                for warning in stats['warnings']:
                    if "⚠️" in warning:
                        st.warning(warning)
                    else:
                        st.info(warning)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Dòng bị xóa", f"{stats['original_rows'] - stats['final_rows']:,}")
            with col2:
                st.metric("Dữ liệu trùng lặp", stats['duplicates_removed'])
            with col3:
                st.metric("Cột được chuyển đổi", stats['types_converted'])
            
            st.divider()
            
            # Before/After comparison
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Trước khi làm sạch")
                st.write(f"Dòng: {stats['original_rows']:,}")
                st.write(f"Cột: {stats['original_cols']}")
                st.write(f"Missing values: {st.session_state.df_original.isnull().sum().sum():,}")
                
                with st.expander("Xem chi tiết missing values"):
                    missing_df = pd.DataFrame({
                        'Column': st.session_state.df_original.columns,
                        'Missing Count': st.session_state.df_original.isnull().sum().values,
                        'Missing %': (st.session_state.df_original.isnull().sum().values / len(st.session_state.df_original) * 100).round(2)
                    })
                    missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
                    st.dataframe(missing_df, use_container_width=True)
            
            with col2:
                st.subheader("✨ Sau khi làm sạch")
                st.write(f"Dòng: {stats['final_rows']:,}")
                st.write(f"Cột: {stats['final_cols']}")
                st.write(f"Missing values: {st.session_state.df_cleaned.isnull().sum().sum():,}")
                
                if st.session_state.df_cleaned.isnull().sum().sum() > 0:
                    with st.expander("Xem chi tiết missing values"):
                        missing_df = pd.DataFrame({
                            'Column': st.session_state.df_cleaned.columns,
                            'Missing Count': st.session_state.df_cleaned.isnull().sum().values,
                            'Missing %': (st.session_state.df_cleaned.isnull().sum().values / len(st.session_state.df_cleaned) * 100).round(2)
                        })
                        missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
                        st.dataframe(missing_df, use_container_width=True)
        else:
            st.info("👈 Sử dụng sidebar để cấu hình và thực hiện làm sạch dữ liệu")
            
            # Show current data quality issues
            st.subheader("⚠️ Các vấn đề chất lượng dữ liệu hiện tại")
            
            col1, col2 = st.columns(2)
            with col1:
                duplicates = st.session_state.df_original.duplicated().sum()
                st.metric("Dòng trùng lặp", duplicates)
            
            with col2:
                missing = st.session_state.df_original.isnull().sum().sum()
                st.metric("Giá trị thiếu", missing)
            
            # Missing values detail
            if missing > 0:
                st.subheader("📊 Chi tiết giá trị thiếu")
                missing_df = pd.DataFrame({
                    'Column': st.session_state.df_original.columns,
                    'Missing Count': st.session_state.df_original.isnull().sum().values,
                    'Missing %': (st.session_state.df_original.isnull().sum().values / len(st.session_state.df_original) * 100).round(2)
                })
                missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
                
                fig = px.bar(missing_df, x='Column', y='Missing %',
                           title='Phần trăm giá trị thiếu theo cột',
                           template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 3: VISUALIZATION ====================
    with tab3:
        st.header("📊 Phân tích trực quan")
        
        col_types = analyze_column_types(df_work)
        
        # Chart builder
        st.subheader("🎨 Tạo biểu đồ tương tác")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            chart_type = st.selectbox(
                "Loại biểu đồ",
                options=['scatter', 'bar', 'box', 'histogram', 'line'],
                format_func=lambda x: {
                    'scatter': 'Scatter Plot',
                    'bar': 'Bar Chart',
                    'box': 'Box Plot',
                    'histogram': 'Histogram',
                    'line': 'Line Chart'
                }[x]
            )
        
        with col2:
            x_col = st.selectbox("Trục X", options=df_work.columns)
        
        with col3:
            if chart_type != 'histogram':
                y_col = st.selectbox("Trục Y (optional)", options=[None] + list(df_work.columns))
            else:
                y_col = None
        
        # Color option
        color_col = st.selectbox("Màu theo cột (optional)", options=[None] + col_types['categorical'])
        
        # Suggest chart type
        if x_col:
            suggested = suggest_chart_type(x_col, y_col, df_work)
            st.info(f"💡 Gợi ý: Với sự kết hợp cột này, biểu đồ **{suggested}** có thể phù hợp nhất")
        
        # Create chart
        if st.button("🎨 Tạo biểu đồ", type="primary"):
            fig = create_visualization(df_work, chart_type, x_col, y_col, color_col)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Correlation heatmap
        if len(col_types['numeric']) >= 2:
            st.subheader("🔥 Ma trận tương quan")
            
            if st.checkbox("Hiển thị Heatmap", value=False):
                fig = create_correlation_heatmap(df_work)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show top correlations
                    numeric_df = df_work[col_types['numeric']]
                    corr_matrix = numeric_df.corr()
                    
                    # Get top positive correlations
                    corr_pairs = []
                    for i in range(len(corr_matrix.columns)):
                        for j in range(i+1, len(corr_matrix.columns)):
                            corr_pairs.append({
                                'Column 1': corr_matrix.columns[i],
                                'Column 2': corr_matrix.columns[j],
                                'Correlation': corr_matrix.iloc[i, j]
                            })
                    
                    corr_df = pd.DataFrame(corr_pairs).sort_values('Correlation', ascending=False, key=abs)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Top 5 tương quan dương:**")
                        st.dataframe(corr_df.head(5), use_container_width=True)
                    
                    with col2:
                        st.write("**Top 5 tương quan âm:**")
                        st.dataframe(corr_df.tail(5), use_container_width=True)
    
    # ==================== TAB 4: ADVANCED STATISTICS ====================
    with tab4:
        st.header("🎯 Thống kê nâng cao")
        
        # Outlier detection
        st.subheader("🔍 Phát hiện Outliers (Phương pháp IQR)")
        
        numeric_cols = col_types['numeric']
        
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("Chọn cột để phân tích outliers", options=numeric_cols)
            
            if st.button("🔎 Phát hiện Outliers", type="primary"):
                outliers_df, stats = detect_outliers(df_work, selected_col)
                
                if outliers_df is not None and stats is not None:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Tổng số giá trị", f"{stats['total_values']:,}")
                    with col2:
                        st.metric("Số Outliers", f"{stats['outliers_count']:,}")
                    with col3:
                        st.metric("Phần trăm", f"{stats['outliers_percentage']:.2f}%")
                    
                    st.divider()
                    
                    # Show IQR statistics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**📊 Thống kê IQR:**")
                        st.write(f"Q1 (25%): {stats['Q1']:.2f}")
                        st.write(f"Q3 (75%): {stats['Q3']:.2f}")
                        st.write(f"IQR: {stats['IQR']:.2f}")
                    
                    with col2:
                        st.write("**📏 Ngưỡng Outlier:**")
                        st.write(f"Lower Bound: {stats['lower_bound']:.2f}")
                        st.write(f"Upper Bound: {stats['upper_bound']:.2f}")
                    
                    # Boxplot
                    fig = px.box(df_work, y=selected_col,
                               title=f"Box Plot - {selected_col}",
                               template='plotly_white')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show outliers table
                    if len(outliers_df) > 0:
                        st.subheader("⚠️ Danh sách Outliers")
                        st.dataframe(outliers_df, use_container_width=True)
                    else:
                        st.success("✅ Không phát hiện outliers trong cột này!")
        else:
            st.warning("⚠️ Không có cột numeric để phân tích outliers")
        
        st.divider()
        
        # Export data
        st.subheader("💾 Xuất dữ liệu")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Xuất dữ liệu gốc:**")
            csv_original = convert_df_to_csv(st.session_state.df_original)
            st.download_button(
                label="📥 Download Original Data (CSV)",
                data=csv_original,
                file_name='original_data.csv',
                mime='text/csv'
            )
        
        with col2:
            if st.session_state.df_cleaned is not None:
                st.write("**Xuất dữ liệu đã làm sạch:**")
                csv_cleaned = convert_df_to_csv(st.session_state.df_cleaned)
                st.download_button(
                    label="📥 Download Cleaned Data (CSV)",
                    data=csv_cleaned,
                    file_name='cleaned_data.csv',
                    mime='text/csv'
                )
            else:
                st.info("Chưa có dữ liệu đã làm sạch")


# ==================== RUN APPLICATION ====================
if __name__ == "__main__":
    main()
