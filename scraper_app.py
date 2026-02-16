"""
SKU HARVESTER - Industrial Data Extraction Platform
===================================================
Zoho-inspired UI with professional industrial theme
User-friendly interface for non-tech industrial users
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="SKU Harvester",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ZOHO-INSPIRED CSS
# ============================================================================

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header */
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1565C0;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .header-icon {
        font-size: 2.5rem;
    }
    
    /* Dashboard Cards */
    .dashboard-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .dashboard-card.blue {
        background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%);
    }
    
    .dashboard-card.orange {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
    }
    
    .dashboard-card.green {
        background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
    }
    
    .dashboard-card.purple {
        background: linear-gradient(135deg, #7E57C2 0%, #9575CD 100%);
    }
    
    .card-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .card-label {
        font-size: 0.9rem;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .card-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    /* Action Cards */
    .action-card {
        background: white;
        border: 2px solid #E0E0E0;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s;
        cursor: pointer;
        height: 100%;
    }
    
    .action-card:hover {
        border-color: #1565C0;
        box-shadow: 0 8px 24px rgba(21, 101, 192, 0.15);
        transform: translateY(-5px);
    }
    
    .action-card-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
    }
    
    .action-card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #212121;
        margin-bottom: 0.5rem;
    }
    
    .action-card-subtitle {
        color: #1565C0;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .action-card-features {
        text-align: left;
        color: #757575;
        font-size: 0.9rem;
        line-height: 1.8;
        margin-bottom: 1.5rem;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(21, 101, 192, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #0D47A1 0%, #1565C0 100%);
        box-shadow: 0 6px 12px rgba(21, 101, 192, 0.4);
        transform: translateY(-2px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F5F7FA 0%, #E8EAF6 100%);
        padding: 1rem 0;
    }
    
    [data-testid="stSidebar"] .sidebar-content {
        padding: 0 1rem;
    }
    
    .sidebar-section {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .sidebar-title {
        font-weight: 700;
        color: #1565C0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .sidebar-item {
        padding: 0.5rem 0;
        color: #424242;
        font-size: 0.9rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #F0F0F0;
    }
    
    .sidebar-item:last-child {
        border-bottom: none;
    }
    
    .sidebar-count {
        background: #E3F2FD;
        color: #1565C0;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* Recent Activity */
    .activity-item {
        background: white;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .activity-item.failed {
        border-left-color: #F44336;
    }
    
    .activity-item.pending {
        border-left-color: #FF9800;
    }
    
    .activity-title {
        font-weight: 600;
        color: #212121;
        margin-bottom: 0.25rem;
    }
    
    .activity-time {
        font-size: 0.8rem;
        color: #757575;
    }
    
    /* Info Box */
    .info-box {
        background: #E3F2FD;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #E8F5E9;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #FFF3E0;
        border-left: 4px solid #FF9800;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    /* Divider */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #1565C0, transparent);
        margin: 2rem 0;
    }
    
    /* Section Header */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #212121;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    /* User Profile */
    .user-profile {
        background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .user-avatar {
        width: 60px;
        height: 60px;
        background: white;
        color: #1565C0;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0 auto 0.75rem auto;
    }
    
    .user-name {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.25rem;
    }
    
    .user-email {
        font-size: 0.85rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'total_scraped' not in st.session_state:
    st.session_state.total_scraped = 1245
if 'week_scraped' not in st.session_state:
    st.session_state.week_scraped = 87
if 'today_scraped' not in st.session_state:
    st.session_state.today_scraped = 0
if 'success_rate' not in st.session_state:
    st.session_state.success_rate = 94
if 'mode' not in st.session_state:
    st.session_state.mode = 'home'

# Website counts (demo data)
website_counts = {
    'Amazon': 456,
    'Indiamart': 334,
    'Industry Buying': 187,
    'Moglix': 98,
    'SKF': 76,
    'Flipkart': 54,
    'SMC': 40
}

# Collections (demo data)
collections = {
    'Bearings': 145,
    'Pneumatics': 87,
    'Electrical': 203,
    'Safety': 56
}

# Recent activity (demo data)
recent_activity = [
    {'product': 'HP Laptop', 'website': 'Amazon', 'time': '5 mins ago', 'status': 'success'},
    {'product': 'Ball Bearing SKF 6205', 'website': 'Indiamart', 'time': '12 mins ago', 'status': 'success'},
    {'product': 'Pneumatic Cylinder', 'website': 'Moglix', 'time': '1 hour ago', 'status': 'failed'},
    {'product': 'Safety Gloves', 'website': 'Industry Buying', 'time': '2 hours ago', 'status': 'success'},
]

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    # User Profile
    st.markdown("""
    <div class="user-profile">
        <div class="user-avatar">AK</div>
        <div class="user-name">Aditya Kumar</div>
        <div class="user-email">aditya@company.com</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview Stats
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">📊 OVERVIEW</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-item"><span>Total Scraped</span><span class="sidebar-count">{st.session_state.total_scraped:,}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-item"><span>This Week</span><span class="sidebar-count">{st.session_state.week_scraped}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-item"><span>Success Rate</span><span class="sidebar-count">{st.session_state.success_rate}%</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">🔍 SCRAPING</div>', unsafe_allow_html=True)
    if st.button("▸ New Scrape Job", use_container_width=True):
        st.session_state.mode = 'home'
    if st.button("▸ Bulk Upload", use_container_width=True):
        st.session_state.mode = 'bulk'
    st.markdown('</div>', unsafe_allow_html=True)
    
    # History
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">📜 HISTORY</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-item"><span>▸ Recent</span><span class="sidebar-count">24</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-item"><span>▸ This Week</span><span class="sidebar-count">87</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-item"><span>▸ This Month</span><span class="sidebar-count">342</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-item"><span>▸ All Time</span><span class="sidebar-count">1,245</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Brands
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">🏷️ BRANDS SCRAPED</div>', unsafe_allow_html=True)
    for brand, count in website_counts.items():
        st.markdown(f'<div class="sidebar-item"><span>☑ {brand}</span><span class="sidebar-count">{count}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Collections
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">📂 SAVED COLLECTIONS</div>', unsafe_allow_html=True)
    for collection, count in collections.items():
        st.markdown(f'<div class="sidebar-item"><span>▸ {collection}</span><span class="sidebar-count">{count}</span></div>', unsafe_allow_html=True)
    if st.button("+ New Collection", use_container_width=True):
        st.info("Collection feature coming soon!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bottom Actions
    st.markdown("---")
    if st.button("⚙️ Settings", use_container_width=True):
        st.info("Settings panel coming soon!")
    if st.button("🆘 Help & Support", use_container_width=True):
        st.info("Help documentation coming soon!")
    if st.button("📤 Export Data", use_container_width=True):
        st.info("Export feature coming soon!")

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

# Header
st.markdown('<div class="main-header"><span class="header-icon">🏭</span> SKU HARVESTER</div>', unsafe_allow_html=True)
st.markdown("**Industrial Data Extraction Platform** - Extract product specifications from multiple e-commerce sources")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================================
# HOME / DASHBOARD
# ============================================================================

if st.session_state.mode == 'home':
    # Dashboard Stats
    st.markdown('<div class="section-header">📊 Dashboard - Today\'s Activity</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="dashboard-card blue">
            <div class="card-icon">🎯</div>
            <div class="card-number">{st.session_state.today_scraped}</div>
            <div class="card-label">Scraped Today</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="dashboard-card green">
            <div class="card-icon">✅</div>
            <div class="card-number">{st.session_state.today_scraped}</div>
            <div class="card-label">Successful</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="dashboard-card orange">
            <div class="card-icon">⚠️</div>
            <div class="card-number">0</div>
            <div class="card-label">Failed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="dashboard-card purple">
            <div class="card-icon">🚀</div>
            <div class="card-number">{st.session_state.success_rate}%</div>
            <div class="card-label">Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Action Cards
    st.markdown('<div class="section-header">🚀 Start New Scraping Job</div>', unsafe_allow_html=True)
    st.markdown("Choose how you want to extract product data:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="action-card">
            <div class="action-card-icon">🔍</div>
            <div class="action-card-title">SINGLE PRODUCT</div>
            <div class="action-card-subtitle">⚡ Quick & Simple</div>
            <div class="action-card-features">
                <strong>Perfect for:</strong><br>
                • Quick product lookups<br>
                • Testing new URLs<br>
                • Single item extraction<br>
                • Instant results
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶ START SINGLE SCRAPE", use_container_width=True, key="single"):
            st.session_state.mode = 'single'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="action-card">
            <div class="action-card-icon">📁</div>
            <div class="action-card-title">BULK UPLOAD</div>
            <div class="action-card-subtitle">💼 Multiple Products</div>
            <div class="action-card-features">
                <strong>Perfect for:</strong><br>
                • Large product catalogs<br>
                • Batch processing<br>
                • 100+ products at once<br>
                • Excel/CSV uploads
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶ START BULK SCRAPE", use_container_width=True, key="bulk"):
            st.session_state.mode = 'bulk'
            st.rerun()
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown('<div class="section-header">📜 Recent Activity</div>', unsafe_allow_html=True)
    
    for activity in recent_activity:
        status_class = 'failed' if activity['status'] == 'failed' else ''
        status_icon = '✅' if activity['status'] == 'success' else '⚠️'
        st.markdown(f"""
        <div class="activity-item {status_class}">
            <div class="activity-title">{status_icon} {activity['website']} - {activity['product']}</div>
            <div class="activity-time">🕐 {activity['time']}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# SINGLE PRODUCT MODE
# ============================================================================

elif st.session_state.mode == 'single':
    st.markdown('<div class="section-header">🔍 Single Product Scraping</div>', unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.mode = 'home'
        st.rerun()
    
    st.markdown('<div class="info-box">💡 <strong>How it works:</strong> Paste a product URL below, select the website, and click scrape to extract all product details and specifications instantly.</div>', unsafe_allow_html=True)
    
    # Website selection
    col1, col2 = st.columns([2, 1])
    with col1:
        website = st.selectbox(
            "🌐 Select Website Source",
            ["Amazon India", "Indiamart", "Industry Buying", "Moglix", "SKF India", "Flipkart", "SMC Pneumatics"],
            help="Choose which e-commerce website you're scraping from"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"📊 Previously scraped: **{website_counts.get(website.replace(' India', '').replace(' Pneumatics', ''), 0)}** products")
    
    # URL input
    product_url = st.text_input(
        "🔗 Product URL",
        placeholder="https://www.amazon.in/product-name/dp/B0XXXXXXXXX",
        help="Paste the complete product page URL here"
    )
    
    # Example URLs
    with st.expander("💡 See Example URLs"):
        st.code("Amazon: https://www.amazon.in/HP-Laptop/dp/B0F5B1N9SJ")
        st.code("Indiamart: https://www.indiamart.com/proddetail/ball-bearing-12345.html")
        st.code("Industry Buying: https://www.industrybuying.com/product-name-ABC123")
    
    # Email section (optional)
    st.markdown("---")
    st.markdown("### 📧 Email Results (Optional)")
    col1, col2 = st.columns(2)
    with col1:
        email_from = st.text_input("From", placeholder="your@email.com")
    with col2:
        email_to = st.text_input("To", placeholder="recipient@email.com")
    
    st.markdown('<div class="info-box">ℹ️ Email feature is currently in demo mode. Results will be shown on screen and available for download.</div>', unsafe_allow_html=True)
    
    # Scrape button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        scrape_btn = st.button("🚀 SCRAPE PRODUCT NOW", use_container_width=True, type="primary")
    
    # Placeholder for scraping results
    if scrape_btn:
        if not product_url:
            st.markdown('<div class="warning-box">⚠️ <strong>Missing URL:</strong> Please enter a product URL to continue.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">🔄 <strong>Scraping functionality will be added here...</strong><br>Waiting for website-specific scraping logic based on your examples.</div>', unsafe_allow_html=True)
            st.info(f"Ready to scrape: {website}\nURL: {product_url}")

# ============================================================================
# BULK UPLOAD MODE
# ============================================================================

elif st.session_state.mode == 'bulk':
    st.markdown('<div class="section-header">📁 Bulk Upload Scraping</div>', unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.mode = 'home'
        st.rerun()
    
    st.markdown('<div class="info-box">💡 <strong>How it works:</strong> Upload an Excel or CSV file with multiple product URLs. The system will scrape all products and provide a comprehensive report.</div>', unsafe_allow_html=True)
    
    # File format info
    st.markdown("### 📋 Required File Format")
    st.markdown("""
    Your file must contain these columns:
    - **materialId** - Your reference number/ID
    - **Source** - Website name (Amazon, Indiamart, etc.)
    - **Product URL** - Full product page URL
    """)
    
    # Template download
    with st.expander("📝 Download Template File"):
        template_df = pd.DataFrame({
            'materialId': ['001', '002', '003'],
            'Source': ['Amazon India', 'Indiamart', 'Industry Buying'],
            'Product URL': [
                'https://www.amazon.in/product/dp/XXXXXXXXXX',
                'https://www.indiamart.com/proddetail/product-12345.html',
                'https://www.industrybuying.com/product-ABC123'
            ]
        })
        st.dataframe(template_df, use_container_width=True)
        
        csv = template_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Template (CSV)",
            csv,
            "sku_harvester_template.csv",
            "text/csv",
            use_container_width=True
        )
    
    # File upload
    st.markdown("---")
    st.markdown("### 📤 Upload Your File")
    uploaded_file = st.file_uploader(
        "Drop your Excel or CSV file here",
        type=['csv', 'xlsx', 'xls'],
        help="Upload a file with materialId, Source, and Product URL columns"
    )
    
    # Email section
    st.markdown("---")
    st.markdown("### 📧 Email Results (Optional)")
    col1, col2 = st.columns(2)
    with col1:
        bulk_email_from = st.text_input("From", placeholder="your@email.com", key="bulk_from")
    with col2:
        bulk_email_to = st.text_input("To", placeholder="recipient@email.com", key="bulk_to")
    
    # Process file if uploaded
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            
            required_cols = ['materialId', 'Source', 'Product URL']
            missing = [c for c in required_cols if c not in df.columns]
            
            if missing:
                st.markdown(f'<div class="warning-box">⚠️ <strong>Missing Columns:</strong> Your file is missing: {", ".join(missing)}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box">✅ <strong>File Validated Successfully!</strong> Your file structure is correct.</div>', unsafe_allow_html=True)
                
                st.markdown("### 📄 File Preview")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Stats
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📦 Total Products", len(df))
                with col2:
                    unique_sources = df['Source'].nunique()
                    st.metric("🌐 Websites", unique_sources)
                with col3:
                    st.metric("⏱️ Est. Time", f"{len(df) * 2} sec")
                with col4:
                    st.metric("💾 Output Size", "2 CSV files")
                
                # Website breakdown
                st.markdown("### 🏷️ Website Breakdown")
                source_counts = df['Source'].value_counts()
                for source, count in source_counts.items():
                    st.markdown(f"**{source}:** {count} products")
                
                # Scrape button
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    bulk_scrape_btn = st.button("🚀 START BULK SCRAPING", use_container_width=True, type="primary")
                
                if bulk_scrape_btn:
                    st.markdown('<div class="info-box">🔄 <strong>Bulk scraping functionality will be added here...</strong><br>Waiting for website-specific scraping logic based on your examples.</div>', unsafe_allow_html=True)
                    st.info(f"Ready to scrape {len(df)} products from {unique_sources} websites")
        
        except Exception as e:
            st.markdown(f'<div class="warning-box">⚠️ <strong>Error Reading File:</strong> {str(e)}</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #757575; padding: 2rem;'>
    <p style='font-weight: 600; color: #1565C0; font-size: 1.1rem;'>🏭 SKU HARVESTER</p>
    <p style='font-size: 0.9rem;'>Industrial Data Extraction Platform | Built for Industrial Procurement Teams</p>
    <p style='font-size: 0.85rem; margin-top: 1rem;'>
        Currently waiting for website-specific scraping logic<br>
        UI is ready - Scraping functions will be added based on your examples
    </p>
</div>
""", unsafe_allow_html=True)
