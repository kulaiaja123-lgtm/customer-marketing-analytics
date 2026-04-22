import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# ============================================
# KONFIGURASI HALAMAN
# ============================================
st.set_page_config(
    page_title="Customer Marketing Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS PROFESIONAL
# ============================================
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-subtitle {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 3px solid #667eea;
    }
    
    .kpi-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
    }
    
    .kpi-label {
        font-size: 0.85rem;
        color: #7f8c8d;
        margin-top: 0.5rem;
    }
    
    /* Insight Box */
    .insight-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .insight-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    .finding-item {
        padding: 0.5rem;
        margin: 0.5rem 0;
        background: white;
        border-radius: 8px;
        border-left: 4px solid #e74c3c;
    }
    
    .rec-item {
        padding: 0.5rem;
        margin: 0.5rem 0;
        background: white;
        border-radius: 8px;
        border-left: 4px solid #27ae60;
    }
    
    /* Chart container */
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        background: #2c3e50;
        color: white;
        border-radius: 10px;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('customer_clean.csv')
        return df
    except FileNotFoundError:
        st.error("❌ File 'customer_clean.csv' tidak ditemukan!")
        st.info("Pastikan file data ada di folder yang sama dengan app.py")
        st.stop()

df = load_data()

# ============================================
# SIDEBAR FILTERS
# ============================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2922/2922506.png", width=80)
    st.markdown("## 🔧 Filter Dashboard")
    st.markdown("---")
    
    # Filter Income
    income_filter = st.multiselect(
        "💰 Income Category",
        options=sorted(df['Income_Category'].unique()),
        default=sorted(df['Income_Category'].unique())
    )
    
    # Filter Spending
    spending_filter = st.multiselect(
        "🛍️ Spending Category",
        options=sorted(df['Spending_Category'].unique()),
        default=sorted(df['Spending_Category'].unique())
    )
    
    # Filter Education
    education_filter = st.multiselect(
        "🎓 Education",
        options=sorted(df['Education'].unique()),
        default=sorted(df['Education'].unique())
    )
    
    # Filter Marital Status
    marital_filter = st.multiselect(
        "💑 Marital Status",
        options=sorted(df['Marital_Status'].unique()),
        default=sorted(df['Marital_Status'].unique())
    )
    
    # Slider Age
    age_min, age_max = st.slider(
        "📅 Age Range",
        min_value=int(df['Age'].min()),
        max_value=int(df['Age'].max()),
        value=(int(df['Age'].min()), int(df['Age'].max()))
    )
    
    st.markdown("---")
    st.caption("💡 **Tips:** Gunakan filter untuk segmentasi customer")

# Apply Filter
df_filtered = df[
    (df['Income_Category'].isin(income_filter)) &
    (df['Spending_Category'].isin(spending_filter)) &
    (df['Education'].isin(education_filter)) &
    (df['Marital_Status'].isin(marital_filter)) &
    (df['Age'] >= age_min) &
    (df['Age'] <= age_max)
]

# Cek data kosong
if len(df_filtered) == 0:
    st.warning("⚠️ Tidak ada data dengan filter yang dipilih. Silakan ubah filter.")
    st.stop()

# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">📊 Customer Marketing Analytics</div>
    <div class="dashboard-subtitle">Professional Customer Segmentation & Campaign Performance Dashboard</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# KPI METRICS
# ============================================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{len(df_filtered):,}</div>
        <div class="kpi-label">👥 Total Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">${df_filtered['Income'].mean():,.0f}</div>
        <div class="kpi-label">💰 Avg Income</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">${df_filtered['Total_Spending'].mean():,.0f}</div>
        <div class="kpi-label">🛒 Avg Spending</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    response_rate = df_filtered['Response'].mean() * 100
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{response_rate:.1f}%</div>
        <div class="kpi-label">📢 Response Rate</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{df_filtered['Age'].mean():.0f}</div>
        <div class="kpi-label">📅 Avg Age</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================
# ROW 1: CHARTS
# ============================================
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 💰 Spending by Product Category")
    
    spending_data = df_filtered[['MntWines', 'MntFruits', 'MntMeatProducts', 
                                'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']].sum()
    
    spending_data.index = ['🍷 Wines', '🍎 Fruits', '🥩 Meat', '🐟 Fish', '🍬 Sweets', '🥇 Gold']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#9b59b6', '#2ecc71', '#e74c3c', '#3498db', '#f39c12', '#f1c40f']
    bars = ax.bar(range(len(spending_data)), spending_data.values, color=colors)
    ax.set_xticks(range(len(spending_data)))
    ax.set_xticklabels(spending_data.index, rotation=45, ha='right')
    ax.set_ylabel('Total Spending ($)', fontsize=12)
    ax.set_title('Total Spending by Product Category', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    for i, (bar, val) in enumerate(zip(bars, spending_data.values)):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                f'${val:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)

with col_right:
    st.markdown("### 📊 Income vs Spending Analysis")
    
    fig = px.scatter(
        df_filtered, 
        x='Income', 
        y='Total_Spending',
        color='Income_Category',
        size='Total_Purchases',
        hover_data=['Age', 'Total_Children', 'Response', 'Education'],
        title='Income vs Spending Correlation',
        color_discrete_sequence=px.colors.qualitative.Set1,
        labels={'Income': 'Annual Income ($)', 'Total_Spending': 'Total Spending ($)'}
    )
    fig.update_layout(
        title_font_size=14,
        title_font_family="Arial",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_traces(marker=dict(opacity=0.6, line=dict(width=1, color='DarkSlateGrey')))
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# ROW 2: CHARTS
# ============================================
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.markdown("### 📢 Response Rate by Income")
    
    response_by_income = df_filtered.groupby('Income_Category')['Response'].agg(['mean', 'count'])
    response_by_income['mean'] = response_by_income['mean'] * 100
    response_by_income = response_by_income.sort_values('mean', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#27ae60' if x > response_rate else '#e74c3c' for x in response_by_income['mean']]
    bars = ax.barh(range(len(response_by_income)), response_by_income['mean'], color=colors)
    ax.set_yticks(range(len(response_by_income)))
    ax.set_yticklabels(response_by_income.index)
    ax.set_xlabel('Response Rate (%)', fontsize=12)
    ax.set_title('Campaign Response Rate by Income Category', fontsize=14, fontweight='bold')
    ax.axvline(x=response_rate, color='blue', linestyle='--', alpha=0.7, 
               label=f'Average: {response_rate:.1f}%')
    
    for i, (bar, val) in enumerate(zip(bars, response_by_income['mean'])):
        ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')
    
    ax.legend()
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

with col_right2:
    st.markdown("### 👨‍👩‍👧‍👦 Customer Demographics")
    
    marital_children = df_filtered.groupby(['Marital_Status', 'Total_Children']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    marital_children.plot(kind='bar', stacked=True, ax=ax, 
                         colormap='Set2', width=0.8, edgecolor='black')
    ax.set_ylabel('Number of Customers', fontsize=12)
    ax.set_xlabel('Marital Status', fontsize=12)
    ax.set_title('Customer Distribution by Marital Status & Children', fontsize=14, fontweight='bold')
    ax.legend(title='Number of Children', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

# ============================================
# ROW 3: CHANNEL ANALYSIS
# ============================================
st.markdown("### 🛒 Purchase Channel Performance")

col_ch1, col_ch2, col_ch3, col_ch4 = st.columns(4)

channels = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases', 'NumDealsPurchases']
channel_names = ['🌐 Web', '📖 Catalog', '🏪 Store', '🎯 Deals']
channel_icons = ['💻', '📚', '🏬', '🏷️']

for col, channel, name, icon in zip([col_ch1, col_ch2, col_ch3, col_ch4], 
                                      channels, channel_names, channel_icons):
    with col:
        total = df_filtered[channel].sum()
        avg = df_filtered[channel].mean()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-label">{icon} {name}</div>
            <div style="font-size: 0.8rem; color: #7f8c8d;">Avg: {avg:.1f} per customer</div>
        </div>
        """, unsafe_allow_html=True)

# Channel pie chart
st.markdown("#### Channel Distribution")
channel_data = df_filtered[channels].sum()
channel_data.index = channel_names

if channel_data.sum() > 0:
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#3498db', '#9b59b6', '#1abc9c', '#e67e22']
    wedges, texts, autotexts = ax.pie(channel_data.values, labels=channel_data.index, 
                                      autopct='%1.1f%%', colors=colors, startangle=90,
                                      textprops={'fontsize': 12, 'fontweight': 'bold'})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    ax.set_title('Purchase Channel Distribution', fontsize=14, fontweight='bold', pad=20)
    st.pyplot(fig)

st.markdown("---")

# ============================================
# INSIGHTS & RECOMMENDATIONS (FIXED VERSION)
# ============================================
st.markdown("### 💡 Strategic Insights & Actionable Recommendations")

# Calculate dynamic insights
top_spending_category = spending_data.idxmax()
wine_spending = spending_data.get('🍷 Wines', 0)
meat_spending = spending_data.get('🥩 Meat', 0)
high_income_response = response_by_income[response_by_income.index == 'High'].values[0] if 'High' in response_by_income.index else 0

# Create insights container
st.markdown('<div class="insight-container">', unsafe_allow_html=True)

# Key Findings Section
st.markdown("#### 🔍 Key Findings")
findings = [
    f"• <b>Wine</b> dominates spending (${wine_spending:,.0f}+), followed by <b>Meat Products</b> (${meat_spending:,.0f})",
    f"• <b>High Income</b> customers have higher response rates ({high_income_response:.1f}%) but represent only ~{len(df_filtered[df_filtered['Income_Category']=='High'])/len(df_filtered)*100:.0f}% of customers",
    "• <b>Catalog purchases</b> generate highest value per transaction",
    "• Customers with <b>0-1 children</b> spend significantly more than those with 2+ children",
    f"• <b>Response rate {response_rate:.1f}%</b> indicates room for campaign optimization"
]

for finding in findings:
    st.markdown(f'<div class="finding-item">{finding}</div>', unsafe_allow_html=True)

st.markdown("---")

# Recommendations Section
st.markdown("#### 🎯 Recommendations")
recommendations = [
    "• <b>Target High-Income + High-Spender</b> segment with premium wine & meat campaigns",
    "• <b>Invest in Catalog Channel</b> for high-value customer acquisition and retention",
    "• <b>Create \"Family-Friendly\" bundles</b> and promotions for customers with 2+ children",
    "• <b>Re-engage low-spender high-income</b> customers with personalized offers and loyalty programs",
    "• <b>A/B test campaign timing</b> based on Recency data to optimize response rates"
]

for rec in recommendations:
    st.markdown(f'<div class="rec-item">{rec}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================
# ML PREDICTION SECTION
# ============================================
st.markdown("### 🤖 AI Customer Response Predictor")

try:
    import joblib
    model = joblib.load('response_predictor.pkl')
    
    with st.expander("🔮 Predict Customer Response (Click to expand)"):
        st.markdown("**Input customer profile below:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pred_age = st.slider("Age", 18, 100, 45)
            pred_income = st.number_input("Annual Income ($)", min_value=0, max_value=200000, value=75000, step=5000)
            pred_children = st.selectbox("Number of Children", [0, 1, 2, 3, 4, 5], index=1)
            pred_spending = st.number_input("Total Spending ($)", min_value=0, max_value=5000, value=1200, step=100)
        
        with col2:
            pred_purchases = st.number_input("Total Purchases (all channels)", min_value=0, max_value=100, value=15)
            pred_recency = st.slider("Recency (days since last purchase)", 0, 365, 30)
            pred_web = st.number_input("Web Purchases", min_value=0, max_value=30, value=5)
            pred_catalog = st.number_input("Catalog Purchases", min_value=0, max_value=30, value=8)
        
        if st.button("🔮 Predict Response Probability", use_container_width=True):
            input_data = pd.DataFrame([{
                'Age': pred_age,
                'Income': pred_income,
                'Total_Children': pred_children,
                'Total_Spending': pred_spending,
                'Total_Purchases': pred_purchases,
                'Recency': pred_recency,
                'NumWebPurchases': pred_web,
                'NumCatalogPurchases': pred_catalog,
                'NumStorePurchases': 2,
                'NumDealsPurchases': 0,
                'NumWebVisitsMonth': 3,
                'Complain': 0
            }])
            
            pred = model.predict(input_data)
            prob = model.predict_proba(input_data)
            
            if pred[0] == 1:
                st.success(f"### ✅ Customer LIKELY TO RESPOND!")
                st.metric("Confidence Level", f"{prob[0][1]*100:.1f}%")
            else:
                st.error(f"### ❌ Customer UNLIKELY TO RESPOND")
                st.metric("Confidence Level", f"{prob[0][0]*100:.1f}%")
                
except FileNotFoundError:
    st.info("📝 **Model not available:** Run 'python 05_ml_prediction.py' first to train the prediction model.")
except Exception as e:
    st.warning(f"⚠️ Model loading error: {str(e)}")

st.markdown("---")

# ============================================
# DATA TABLE
# ============================================
st.markdown("### 📋 Customer Data Explorer")

# Pilih kolom untuk tampilan
display_cols = ['Id', 'Age', 'Income', 'Income_Category', 'Total_Spending', 
                'Spending_Category', 'Total_Purchases', 'Total_Children',
                'Response', 'Complain', 'Recency']

# Pastikan kolom yang diminta ada
available_cols = [col for col in display_cols if col in df_filtered.columns]

# Tampilkan dengan styling
st.dataframe(
    df_filtered[available_cols].style
    .format({'Income': '${:,.0f}', 'Total_Spending': '${:,.0f}'})
    .background_gradient(subset=['Income', 'Total_Spending'], cmap='Blues')
    .highlight_max(subset=['Response'], color='lightgreen')
    .highlight_min(subset=['Response'], color='lightcoral'),
    use_container_width=True,
    height=400
)

st.markdown("---")

# ============================================
# EXPORT DATA
# ============================================
st.markdown("### 💾 Export Analysis")

col_dl1, col_dl2 = st.columns(2)

with col_dl1:
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download CSV",
        csv,
        "customer_analysis_data.csv",
        "text/csv",
        use_container_width=True
    )

with col_dl2:
    try:
        import io
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_filtered.to_excel(writer, sheet_name='Raw Data', index=False)
            
            # Summary sheet
            summary_data = {
                'Metric': ['Total Customers', 'Avg Income', 'Avg Spending', 'Response Rate', 'Avg Age',
                          'Avg Children', 'Avg Recency', 'Total Web Purchases', 'Total Catalog Purchases',
                          'Total Store Purchases', 'Total Deals Purchases'],
                'Value': [len(df_filtered), 
                         f"${df_filtered['Income'].mean():,.0f}",
                         f"${df_filtered['Total_Spending'].mean():,.0f}",
                         f"{df_filtered['Response'].mean()*100:.1f}%",
                         f"{df_filtered['Age'].mean():.0f}",
                         f"{df_filtered['Total_Children'].mean():.1f}",
                         f"{df_filtered['Recency'].mean():.0f} days",
                         f"{df_filtered['NumWebPurchases'].sum():,}",
                         f"{df_filtered['NumCatalogPurchases'].sum():,}",
                         f"{df_filtered['NumStorePurchases'].sum():,}",
                         f"{df_filtered['NumDealsPurchases'].sum():,}"]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Response by category
            response_by_income_df = pd.DataFrame(response_by_income)
            response_by_income_df.to_excel(writer, sheet_name='Response by Income')
        
        st.download_button(
            "📊 Download Excel Report",
            buffer.getvalue(),
            "customer_analysis_report.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    except Exception as e:
        st.warning(f"Excel export not available: {str(e)}")

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    🛠️ Built with Python, Streamlit, Pandas, Matplotlib & Plotly | 
    📊 Data: Customer Personality Analysis | 
    👤 Created by Mhd Hanafi Akbar
</div>
""", unsafe_allow_html=True)
