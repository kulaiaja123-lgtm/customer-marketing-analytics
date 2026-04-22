import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# ============================================
# KONFIGURASI HALAMAN
# ============================================
st.set_page_config(
    page_title="Customer Marketing Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
# SIDEBAR
# ============================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2922/2922506.png", width=100)
st.sidebar.title("🔧 Filter Data")


# Filter Income
income_filter = st.sidebar.multiselect(
    "💰 Income Category",
    options=sorted(df['Income_Category'].unique()),
    default=sorted(df['Income_Category'].unique())
)

# Filter Spending
spending_filter = st.sidebar.multiselect(
    "🛍️ Spending Category",
    options=sorted(df['Spending_Category'].unique()),
    default=sorted(df['Spending_Category'].unique())
)

# Filter Education
education_filter = st.sidebar.multiselect(
    "🎓 Education",
    options=sorted(df['Education'].unique()),
    default=sorted(df['Education'].unique())
)

# Filter Marital Status
marital_filter = st.sidebar.multiselect(
    "💑 Marital Status",
    options=sorted(df['Marital_Status'].unique()),
    default=sorted(df['Marital_Status'].unique())
)

# Slider Age
age_min, age_max = st.sidebar.slider(
    "📅 Age Range",
    min_value=int(df['Age'].min()),
    max_value=int(df['Age'].max()),
    value=(int(df['Age'].min()), int(df['Age'].max()))
)

# Apply Filter
df_filtered = df[
    (df['Income_Category'].isin(income_filter)) &
    (df['Spending_Category'].isin(spending_filter)) &
    (df['Education'].isin(education_filter)) &
    (df['Marital_Status'].isin(marital_filter)) &
    (df['Age'] >= age_min) &
    (df['Age'] <= age_max)
]

# ============================================
# HEADER
# ============================================
st.markdown('<p class="main-header">🛒 Customer Marketing Analytics</p>', unsafe_allow_html=True)
st.markdown("*Interactive dashboard untuk analisis segmentasi customer dan marketing campaign*")

# ============================================
# KPI CARDS
# ============================================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("👥 Total Customers", f"{len(df_filtered):,}")

with col2:
    st.metric("💵 Avg Income", f"${df_filtered['Income'].mean():,.0f}")

with col3:
    st.metric("🛒 Avg Spending", f"${df_filtered['Total_Spending'].mean():,.0f}")

with col4:
    response_rate = df_filtered['Response'].mean() * 100
    st.metric("📢 Response Rate", f"{response_rate:.1f}%")

with col5:
    avg_age = df_filtered['Age'].mean()
    st.metric("📅 Avg Age", f"{avg_age:.0f} years")

st.divider()

# ============================================
# ROW 1: CHARTS
# ============================================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("💰 Spending by Product Category")
    
    spending_data = df_filtered[['MntWines', 'MntFruits', 'MntMeatProducts', 
                                'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']].sum()
    
    # Rename untuk tampilan lebih baik
    spending_data.index = ['Wines', 'Fruits', 'Meat', 'Fish', 'Sweets', 'Gold']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#8e44ad', '#27ae60', '#c0392b', '#2980b9', '#f39c12', '#f1c40f']
    bars = ax.bar(spending_data.index, spending_data.values, color=colors)
    
    # Tambah label nilai
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=10)
    
    ax.set_ylabel('Total Spending ($)')
    ax.set_title('Total Spending by Product Category')
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col_right:
    st.subheader("📊 Income vs Total Spending")
    
    fig = px.scatter(
        df_filtered, 
        x='Income', 
        y='Total_Spending',
        color='Income_Category',
        size='Total_Purchases',
        hover_data=['Age', 'Total_Children', 'Response'],
        title='Income vs Spending (bubble size = total purchases)',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig.update_traces(marker=dict(opacity=0.7))
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# ROW 2: MORE CHARTS
# ============================================
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("📢 Campaign Response by Income")
    
    response_by_income = df_filtered.groupby('Income_Category')['Response'].agg(['mean', 'count'])
    response_by_income['mean'] = response_by_income['mean'] * 100
    response_by_income = response_by_income.sort_values('mean', ascending=False)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#2ecc71' if x > 15 else '#e74c3c' for x in response_by_income['mean']]
    bars = ax.bar(response_by_income.index, response_by_income['mean'], color=colors)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_ylabel('Response Rate (%)')
    ax.set_title('Campaign Response Rate by Income Category')
    ax.axhline(y=14.9, color='red', linestyle='--', alpha=0.5, label='Overall Average')
    ax.legend()
    st.pyplot(fig)

with col_right2:
    st.subheader("👨‍👩‍👧‍👦 Customer by Marital Status & Children")
    
    marital_children = df_filtered.groupby(['Marital_Status', 'Total_Children']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    marital_children.plot(kind='bar', stacked=True, ax=ax, 
                        colormap='Set3', width=0.8)
    ax.set_ylabel('Number of Customers')
    ax.set_title('Customer Distribution by Marital Status & Children')
    ax.legend(title='Children', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.divider()

# ============================================
# ROW 3: CHANNEL ANALYSIS
# ============================================
st.subheader("🛒 Purchase Channel Analysis")

col_ch1, col_ch2, col_ch3, col_ch4 = st.columns(4)

channels = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases', 'NumDealsPurchases']
channel_names = ['Web', 'Catalog', 'Store', 'Deals']

for col, channel, name in zip([col_ch1, col_ch2, col_ch3, col_ch4], channels, channel_names):
    with col:
        total = df_filtered[channel].sum()
        avg = df_filtered[channel].mean()
        st.metric(f"{name} Purchases", f"{total:,}", f"Avg: {avg:.1f}")

# Channel comparison chart
channel_data = df_filtered[channels].sum()
channel_data.index = channel_names

fig, ax = plt.subplots(figsize=(10, 5))
colors = ['#3498db', '#9b59b6', '#1abc9c', '#e67e22']
wedges, texts, autotexts = ax.pie(channel_data.values, labels=channel_data.index, 
                                    autopct='%1.1f%%', colors=colors, startangle=90)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax.set_title('Purchase Channel Distribution')
st.pyplot(fig)

st.divider()

# ============================================
# INSIGHTS & RECOMMENDATIONS
# ============================================
st.subheader("Key Insights & Recommendations")

st.markdown("""
<div class="insight-box">
    <h4>Key Findings:</h4>
    <ul>
        <li><b>Wine</b> dominates spending ($680K+), followed by <b>Meat Products</b></li>
        <li><b>High Income</b> customers have higher response rates but represent only ~25%</li>
        <li><b>Catalog purchases</b> generate highest value per transaction</li>
        <li>Customers with <b>0-1 children</b> spend significantly more than those with 2+</li>
        <li><b>Response rate 14.9%</b> indicates room for campaign optimization</li>
    </ul>

    <h4>Recommendations:</h4>
    <ul>
        <li><b>Target High-Income + High-Spender</b> with premium wine & meat campaigns</li>
        <li><b>Invest in Catalog channel</b> for high-value customer acquisition</li>
        <li><b>Create "Family-Friendly" bundles</b> for customers with 2+ children</li>
        <li><b>Re-engage low-spender high-income</b> customers with personalized offers</li>
        <li><b>A/B test campaign timing</b> based on Recency data</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================================
# ML PREDICTION SECTION
# ============================================
st.divider()
st.subheader("🤖 AI Prediction: Will This Customer Respond?")

import joblib

try:
    model = joblib.load('response_predictor.pkl')
    
    with st.expander("🔮 Predict Customer Response"):
        col1, col2 = st.columns(2)
        
        with col1:
            pred_age = st.number_input("Age", 18, 100, 45)
            pred_income = st.number_input("Income ($)", 0, 200000, 75000)
            pred_children = st.number_input("Children", 0, 5, 1)
            pred_spending = st.number_input("Total Spending ($)", 0, 5000, 1200)
        
        with col2:
            pred_purchases = st.number_input("Total Purchases", 0, 50, 15)
            pred_recency = st.number_input("Recency (days)", 0, 365, 30)
            pred_web = st.number_input("Web Purchases", 0, 20, 5)
            pred_catalog = st.number_input("Catalog Purchases", 0, 20, 8)
        
        if st.button("🔮 Predict"):
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
                st.success(f"✅ AKAN RESPON! (Confidence: {prob[0][1]*100:.1f}%)")
            else:
                st.error(f"❌ TIDAK RESPON (Confidence: {prob[0][0]*100:.1f}%)")
                
except FileNotFoundError:
    st.info("📝 Run 'python 05_ml_prediction.py' first to train the model")

# ============================================
# DATA TABLE
# ============================================
st.subheader("📋 Customer Data Detail")

# Pilih kolom untuk tampilan
display_cols = ['Id', 'Age', 'Income', 'Income_Category', 'Total_Spending', 
                'Spending_Category', 'Total_Purchases', 'Total_Children',
                'Response', 'Complain', 'Recency']

# Format currency
st.dataframe(
    df_filtered[display_cols].style.format({
        'Income': '${:,.0f}',
        'Total_Spending': '${:,.0f}'
    }),
    use_container_width=True,
    height=400
)

# ============================================
# DOWNLOAD
# ============================================
st.subheader("💾 Export Data")

col_dl1, col_dl2 = st.columns(2)

with col_dl1:
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Filtered Data (CSV)",
        csv,
        "filtered_customers.csv",
        "text/csv"
    )

with col_dl2:
    # Excel dengan multiple sheets
    import io
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_filtered.to_excel(writer, sheet_name='Filtered Data', index=False)
        
        # Summary sheet
        summary = pd.DataFrame({
            'Metric': ['Total Customers', 'Avg Income', 'Avg Spending', 'Response Rate', 'Avg Age'],
            'Value': [len(df_filtered), 
                     f"${df_filtered['Income'].mean():,.0f}",
                     f"${df_filtered['Total_Spending'].mean():,.0f}",
                     f"{df_filtered['Response'].mean()*100:.1f}%",
                     f"{df_filtered['Age'].mean():.0f}"]
        })
        summary.to_excel(writer, sheet_name='Summary', index=False)
    
    st.download_button(
        "📊 Download Report (Excel)",
        buffer.getvalue(),
        "customer_analysis_report.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ============================================
# FOOTER
# ============================================
st.divider()
st.caption("""
    🛠️ Built with Python, Pandas, Matplotlib, Plotly & Streamlit | 
    📊 Data: Customer Personality Analysis (Kaggle) | 
    👤 Created by [Mhd Hanafi Akbar]
""")
