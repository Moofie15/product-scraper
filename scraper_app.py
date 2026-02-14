"""
SKU HARVESTER
=============
Industrial-Grade Product Data Extraction Platform

A professional tool for extracting, processing, and analyzing
e-commerce product data at scale.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import json

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="SKU Harvester",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - INDUSTRIAL-TECH HYBRID DESIGN
# ============================================================================

st.markdown("""
<style>
    /* Global Styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Header - Industrial Tech Style */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1a237e 0%, #0d47a1 50%, #01579b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.3rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    .sub-header {
        text-align: center;
        color: #546e7a;
        font-size: 1rem;
        margin-bottom: 2rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Industrial Stat Cards */
    .stat-card {
        background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1976d2;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, rgba(25, 118, 210, 0.1) 0%, transparent 100%);
        border-radius: 0 8px 0 100%;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.2);
        border-left-color: #ff6f00;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1976d2 0%, #0d47a1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1;
    }
    
    .stat-label {
        color: #546e7a;
        font-size: 0.75rem;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Action Buttons - Industrial Style */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
        color: white;
        font-size: 1rem;
        font-weight: 700;
        padding: 0.8rem 1.5rem;
        border-radius: 6px;
        border: none;
        box-shadow: 0 2px 8px rgba(25, 118, 210, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
        box-shadow: 0 4px 16px rgba(25, 118, 210, 0.4);
        transform: translateY(-2px);
    }
    
    /* Primary Action Button */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #ff6f00 0%, #f57c00 100%);
        box-shadow: 0 2px 8px rgba(255, 111, 0, 0.3);
    }
    
    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(135deg, #f57c00 0%, #ef6c00 100%);
        box-shadow: 0 4px 16px rgba(255, 111, 0, 0.4);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1565c0;
        margin: 2rem 0 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 2px solid #e3f2fd;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Info Boxes - Tech Style */
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #1976d2;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #ff6f00;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1.5rem;
        border-radius: 6px;
        border-left: 4px solid #43a047;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(67, 160, 71, 0.2);
    }
    
    /* Tooltip Text */
    .tooltip-text {
        font-size: 0.8rem;
        color: #78909c;
        font-style: italic;
        margin-top: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    
    /* Upload Section - Industrial Box */
    .upload-section {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 1.5rem 0;
        border: 1px solid #e0e0e0;
    }
    
    /* Sidebar - Tech Industrial */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #eceff1 0%, #cfd8dc 100%);
        border-right: 2px solid #90a4ae;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #263238;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9rem;
    }
    
    /* Website Chips */
    .website-chip {
        display: inline-block;
        background: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        transition: all 0.2s;
    }
    
    .website-chip:hover {
        box-shadow: 0 2px 6px rgba(25, 118, 210, 0.2);
        border-color: #1976d2;
        transform: translateY(-1px);
    }
    
    /* Data Table Styling */
    .dataframe {
        border: 1px solid #e0e0e0 !important;
        border-radius: 6px !important;
        overflow: hidden !important;
    }
    
    /* Progress Bar - Industrial */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1976d2, #ff6f00) !important;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #90a4ae, transparent);
    }
    
    /* Mode Selection Cards */
    .mode-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
        border: 2px solid #e0e0e0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .mode-card:hover {
        border-color: #1976d2;
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.2);
        transform: translateY(-2px);
    }
    
    .mode-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .mode-title {
        font-weight: 700;
        color: #263238;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
        color: #1565c0;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

if 'total_scraped' not in st.session_state:
    st.session_state.total_scraped = 0
if 'success_rate' not in st.session_state:
    st.session_state.success_rate = 0
if 'jobs_completed' not in st.session_state:
    st.session_state.jobs_completed = 0
if 'scraping_mode' not in st.session_state:
    st.session_state.scraping_mode = 'single'

# ============================================================================
# SUPPORTED WEBSITES DATABASE
# ============================================================================

SUPPORTED_WEBSITES = {
    "Amazon India": {
        "icon": "🛒",
        "color": "#FF9900",
        "pattern": "amazon.in",
        "category": "Marketplace"
    },
    "Flipkart": {
        "icon": "🏪",
        "color": "#2874F0",
        "pattern": "flipkart.com",
        "category": "Marketplace"
    },
    "IndiaMART": {
        "icon": "🏭",
        "color": "#4CAF50",
        "pattern": "indiamart.com",
        "category": "B2B"
    },
    "IndustryBuying": {
        "icon": "🔧",
        "color": "#E91E63",
        "pattern": "industrybuying.com",
        "category": "Industrial"
    },
    "Moglix": {
        "icon": "⚙️",
        "color": "#FF5722",
        "pattern": "moglix.com",
        "category": "Industrial"
    },
    "SKF India": {
        "icon": "⚡",
        "color": "#1565C0",
        "pattern": "skf.com",
        "category": "Technical"
    },
    "SMC Pneumatics": {
        "icon": "🔩",
        "color": "#43A047",
        "pattern": "smcpneumatics.com",
        "category": "Technical"
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def detect_website(url):
    """Auto-detect website from URL"""
    url_lower = url.lower()
    for website, info in SUPPORTED_WEBSITES.items():
        if info['pattern'] in url_lower:
            return website
    return "Unknown"

def validate_bulk_upload(df):
    """Validate uploaded file structure"""
    required_columns = ['RefNo', 'SKUSource', 'SKU Link']
    
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        return False, f"❌ Missing required columns: {', '.join(missing_cols)}"
    
    for col in required_columns:
        if df[col].isnull().any():
            return False, f"❌ Column '{col}' contains empty values"
    
    return True, "✅ File structure validated successfully"

def scrape_product_demo(url, website):
    """Demo scraping function"""
    time.sleep(0.3)
    
    demo_products = {
        "Amazon India": {
            "product_name": "SKF Deep Groove Ball Bearing 6205",
            "brand": "SKF",
            "price": "₹1,250.00",
            "availability": "In Stock",
            "specs": {
                "Inner Diameter": "25 mm",
                "Outer Diameter": "52 mm",
                "Width": "15 mm",
                "Material": "Chrome Steel",
                "Seal Type": "Open",
                "Weight": "0.13 kg",
                "Load Rating": "7800 N"
            }
        },
        "Flipkart": {
            "product_name": "SMC Pneumatic Cylinder CDQ2B32-50D",
            "brand": "SMC Corporation",
            "price": "₹2,850.00",
            "availability": "In Stock",
            "specs": {
                "Bore Size": "32 mm",
                "Stroke Length": "50 mm",
                "Operating Pressure": "1.0 MPa",
                "Material": "Aluminum Alloy",
                "Port Size": "M5",
                "Weight": "0.45 kg",
                "Mount Type": "Basic"
            }
        },
        "Default": {
            "product_name": "Industrial Component - Standard Grade",
            "brand": "Generic",
            "price": "₹999.00",
            "availability": "In Stock",
            "specs": {
                "Type": "Standard Industrial",
                "Material": "Steel/Aluminum",
                "Grade": "Industrial",
                "Weight": "0.5 kg"
            }
        }
    }
    
    data = demo_products.get(website, demo_products["Default"])
    data.update({
        'url': url,
        'website': website,
        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': '✅ Success'
    })
    
    return data

# ============================================================================
# HEADER
# ============================================================================

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-header">⚙️ SKU HARVESTER</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Industrial-Grade Data Extraction Platform</p>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - CONTROL PANEL
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ CONTROL PANEL")
    st.markdown("---")
    
    # System Status
    st.markdown("#### 🔌 SYSTEM STATUS")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Status:**")
        st.success("🟢 ONLINE")
    with col2:
        st.markdown("**Mode:**")
        st.info("📊 DEMO")
    
    st.markdown("---")
    
    # Supported Platforms
    st.markdown("#### 🌐 SUPPORTED PLATFORMS")
    
    categories = {}
    for website, info in SUPPORTED_WEBSITES.items():
        category = info['category']
        if category not in categories:
            categories[category] = []
        categories[category].append((website, info['icon']))
    
    for category, sites in categories.items():
        with st.expander(f"📁 {category}"):
            for site, icon in sites:
                st.markdown(f"{icon} **{site}**")
    
    st.markdown("---")
    
    # Performance Metrics
    st.markdown("#### 📊 PERFORMANCE")
    st.metric("Total Extracted", st.session_state.total_scraped, delta=None)
    st.metric("Jobs Completed", st.session_state.jobs_completed, delta=None)
    st.metric("Success Rate", f"{st.session_state.success_rate}%", delta=None)
    
    st.markdown("---")
    
    # Documentation
    with st.expander("📖 DOCUMENTATION"):
        st.markdown("""
        **Quick Start:**
        1. Select extraction mode
        2. Input data source
        3. Configure parameters
        4. Execute extraction
        
        **File Format:**
        - RefNo: Reference ID
        - SKUSource: Platform name
        - SKU Link: Product URL
        """)
    
    with st.expander("🛠️ SUPPORT"):
        st.markdown("""
        **Technical Support:**
        📧 support@skuharvester.tech
        📞 +91-XXXX-XXXXXX
        🌐 docs.skuharvester.tech
        """)

# ============================================================================
# DASHBOARD
# ============================================================================

st.markdown('<p class="section-header">📊 SYSTEM DASHBOARD</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <p class="stat-number">""" + str(st.session_state.total_scraped) + """</p>
        <p class="stat-label">📦 TOTAL EXTRACTIONS</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <p class="stat-number">""" + str(st.session_state.success_rate) + """%</p>
        <p class="stat-label">✅ SUCCESS RATE</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <p class="stat-number">""" + str(st.session_state.jobs_completed) + """</p>
        <p class="stat-label">⚡ JOBS EXECUTED</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <p class="stat-number">7</p>
        <p class="stat-label">🌐 PLATFORMS ACTIVE</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# MODE SELECTION
# ============================================================================

st.markdown('<p class="section-header">🔧 EXTRACTION MODE</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("🎯 SINGLE URL EXTRACTION", use_container_width=True):
        st.session_state.scraping_mode = 'single'
    st.markdown('<p class="tooltip-text">💡 Extract data from individual product URL</p>', unsafe_allow_html=True)

with col2:
    if st.button("📦 BATCH PROCESSING", use_container_width=True):
        st.session_state.scraping_mode = 'bulk'
    st.markdown('<p class="tooltip-text">💡 Process multiple URLs from uploaded file</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# SINGLE URL MODE
# ============================================================================

if st.session_state.scraping_mode == 'single':
    
    st.markdown('<p class="section-header">🎯 SINGLE URL EXTRACTION</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    # Platform Selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_website = st.selectbox(
            "🌐 TARGET PLATFORM",
            list(SUPPORTED_WEBSITES.keys()),
            help="Select the e-commerce platform"
        )
        st.markdown('<p class="tooltip-text">💡 Choose the source platform for extraction</p>', unsafe_allow_html=True)
    
    with col2:
        icon = SUPPORTED_WEBSITES[selected_website]['icon']
        st.markdown(f"<div style='text-align: center; font-size: 4rem; padding-top: 0.5rem;'>{icon}</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # URL Input
    product_url = st.text_input(
        "🔗 PRODUCT URL",
        placeholder=f"Enter {selected_website} product URL...",
        help="Full product page URL including https://"
    )
    st.markdown('<p class="tooltip-text">💡 Paste the complete product page link</p>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Email Configuration
    st.markdown("#### 📧 NOTIFICATION SETTINGS (Optional)")
    col1, col2 = st.columns(2)
    
    with col1:
        email_from = st.text_input(
            "Sender Address",
            placeholder="sender@company.com",
            help="Email sender address"
        )
    
    with col2:
        email_to = st.text_input(
            "Recipient Address",
            placeholder="recipient@company.com",
            help="Email recipient address"
        )
    
    st.markdown('<p class="tooltip-text">💡 Results will be emailed after extraction (Demo Mode)</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Execute Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        execute_btn = st.button("⚡ EXECUTE EXTRACTION", use_container_width=True, type="primary")
    
    if execute_btn:
        if not product_url:
            st.error("❌ ERROR: Product URL required")
        else:
            with st.spinner(f'⚙️ Executing extraction from {selected_website}...'):
                progress_bar = st.progress(0)
                status = st.empty()
                
                steps = [
                    "Initializing connection...",
                    "Establishing secure link...",
                    "Loading product data...",
                    "Extracting specifications...",
                    "Processing price information...",
                    "Validating data integrity...",
                    "Finalizing extraction..."
                ]
                
                for i, step in enumerate(steps):
                    status.text(f"⚙️ {step}")
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(0.2)
                
                product_data = scrape_product_demo(product_url, selected_website)
                st.session_state.total_scraped += 1
                st.session_state.jobs_completed += 1
                st.session_state.success_rate = 100
            
            st.markdown('<div class="success-box"><b>✅ EXTRACTION COMPLETE</b><br>Product data successfully extracted and validated</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Results Display
            st.markdown("### 📋 EXTRACTION RESULTS")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 📦 PRODUCT INFORMATION")
                st.markdown(f"**Name:** {product_data['product_name']}")
                st.markdown(f"**Brand:** {product_data['brand']}")
                st.markdown(f"**Platform:** {product_data['website']}")
                st.markdown(f"**Availability:** {product_data['availability']}")
                st.markdown(f"**Extracted:** {product_data['scraped_at']}")
                st.markdown(f"**Status:** {product_data['status']}")
            
            with col2:
                st.markdown("#### 💰 PRICING DATA")
                st.markdown(f"<h1 style='color: #1565c0; font-weight: 800;'>{product_data['price']}</h1>", unsafe_allow_html=True)
                st.success("✅ Price Verified")
            
            st.markdown("---")
            
            # Specifications Table
            st.markdown("### 🔧 TECHNICAL SPECIFICATIONS")
            
            specs_df = pd.DataFrame(
                list(product_data['specs'].items()),
                columns=['Parameter', 'Value']
            )
            
            st.dataframe(specs_df, use_container_width=True, hide_index=True)
            
            # Email Notification
            if email_from and email_to:
                st.markdown(f"""
                <div class="info-box">
                    📧 <b>NOTIFICATION STATUS:</b><br>
                    Results would be sent from <b>{email_from}</b> to <b>{email_to}</b><br>
                    <i>(Email functionality in demo mode)</i>
                </div>
                """, unsafe_allow_html=True)
            
            # Export Options
            st.markdown("---")
            st.markdown("### 💾 EXPORT OPTIONS")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv_data = specs_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📄 EXPORT CSV",
                    data=csv_data,
                    file_name=f"extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                json_data = json.dumps(product_data, indent=2)
                st.download_button(
                    label="🔧 EXPORT JSON",
                    data=json_data,
                    file_name=f"extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col3:
                st.download_button(
                    label="📊 EXPORT EXCEL",
                    data=csv_data,
                    file_name=f"extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.ms-excel",
                    use_container_width=True
                )

# ============================================================================
# BULK PROCESSING MODE
# ============================================================================

elif st.session_state.scraping_mode == 'bulk':
    
    st.markdown('<p class="section-header">📦 BATCH PROCESSING</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    # Format Information
    st.markdown("""
    <div class="info-box">
        <b>📋 REQUIRED FILE FORMAT:</b><br>
        <b>Column 1:</b> RefNo (Reference Number/ID)<br>
        <b>Column 2:</b> SKUSource (Platform Name)<br>
        <b>Column 3:</b> SKU Link (Product URL)
    </div>
    """, unsafe_allow_html=True)
    
    # Template Download
    with st.expander("📥 DOWNLOAD TEMPLATE"):
        st.markdown("Standard batch processing template:")
        
        template_data = {
            "RefNo": ["REF-2024-001", "REF-2024-002", "REF-2024-003"],
            "SKUSource": ["Amazon India", "Flipkart", "SKF India"],
            "SKU Link": [
                "https://www.amazon.in/dp/B08XXXX1",
                "https://www.flipkart.com/product/p/itmxxx",
                "https://www.skf.com/in/products/..."
            ]
        }
        
        template_df = pd.DataFrame(template_data)
        st.dataframe(template_df, use_container_width=True, hide_index=True)
        
        template_csv = template_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DOWNLOAD TEMPLATE",
            data=template_csv,
            file_name="sku_harvester_template.csv",
            mime="text/csv"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # File Upload
    st.markdown("#### 📤 FILE UPLOAD")
    uploaded_file = st.file_uploader(
        "Select batch processing file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload CSV or Excel file with required columns"
    )
    st.markdown('<p class="tooltip-text">💡 Drag and drop or click to browse files</p>', unsafe_allow_html=True)
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            is_valid, message = validate_bulk_upload(df)
            
            if not is_valid:
                st.error(message)
                df = None
            else:
                st.success(message)
                
                df['Detected_Platform'] = df['SKU Link'].apply(detect_website)
                
                st.markdown("#### 🔍 FILE PREVIEW & VALIDATION")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 TOTAL ENTRIES", len(df))
                with col2:
                    valid = len(df[df['Detected_Platform'] != 'Unknown'])
                    st.metric("✅ VALIDATED", valid)
                with col3:
                    invalid = len(df[df['Detected_Platform'] == 'Unknown'])
                    st.metric("⚠️ UNKNOWN", invalid)
                
                # Platform Distribution
                st.markdown("#### 🌐 PLATFORM DISTRIBUTION")
                platform_counts = df['Detected_Platform'].value_counts()
                
                cols = st.columns(min(len(platform_counts), 4))
                for idx, (platform, count) in enumerate(platform_counts.items()):
                    with cols[idx % 4]:
                        icon = SUPPORTED_WEBSITES.get(platform, {}).get('icon', '❓')
                        st.metric(f"{icon} {platform}", count)
        
        except Exception as e:
            st.error(f"❌ FILE ERROR: {str(e)}")
            df = None
    else:
        df = None
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Email Configuration
    st.markdown("#### 📧 NOTIFICATION SETTINGS (Optional)")
    col1, col2 = st.columns(2)
    
    with col1:
        bulk_email_from = st.text_input("Sender", placeholder="sender@company.com", key="bulk_from")
    with col2:
        bulk_email_to = st.text_input("Recipient", placeholder="recipient@company.com", key="bulk_to")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Execute Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        bulk_execute = st.button(
            "⚡ EXECUTE BATCH PROCESSING",
            use_container_width=True,
            type="primary",
            disabled=(df is None)
        )
    
    if bulk_execute and df is not None:
        st.markdown("---")
        st.markdown("### ⚙️ BATCH PROCESSING STATUS")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        current_item = st.empty()
        
        results = []
        
        for idx, row in df.iterrows():
            current_item.info(f"⚙️ Processing: {row['RefNo']} | Platform: {row['SKUSource']}")
            status_text.text(f"Progress: {idx + 1}/{len(df)} items")
            
            try:
                product_data = scrape_product_demo(row['SKU Link'], row['SKUSource'])
                product_data['RefNo'] = row['RefNo']
                results.append(product_data)
            except Exception as e:
                results.append({
                    'RefNo': row['RefNo'],
                    'status': '❌ Failed',
                    'error': str(e)
                })
            
            progress_bar.progress((idx + 1) / len(df))
        
        current_item.empty()
        status_text.text("✅ Batch processing completed")
        
        st.session_state.total_scraped += len(results)
        st.session_state.jobs_completed += 1
        success_count = len([r for r in results if '✅' in r.get('status', '')])
        st.session_state.success_rate = int((success_count / len(results)) * 100)
        
        st.markdown("---")
        
        # Results Summary
        st.markdown("### 📊 PROCESSING SUMMARY")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("PROCESSED", len(results))
        with col2:
            st.metric("SUCCESSFUL", success_count)
        with col3:
            failed = len(results) - success_count
            st.metric("FAILED", failed)
        with col4:
            rate = (success_count / len(results) * 100) if results else 0
            st.metric("SUCCESS RATE", f"{rate:.1f}%")
        
        st.markdown("---")
        
        # Results Table
        st.markdown("### 📋 EXTRACTION RESULTS")
        results_df = pd.DataFrame(results)
        st.dataframe(results_df, use_container_width=True, hide_index=True)
        
        # Email Notification
        if bulk_email_from and bulk_email_to:
            st.markdown(f"""
            <div class="info-box">
                📧 <b>NOTIFICATION:</b> Results would be sent from {bulk_email_from} to {bulk_email_to} (Demo Mode)
            </div>
            """, unsafe_allow_html=True)
        
        # Export Options
        st.markdown("---")
        st.markdown("### 💾 EXPORT RESULTS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv_results = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📄 EXPORT FULL RESULTS (CSV)",
                data=csv_results,
                file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            json_results = json.dumps(results, indent=2)
            st.download_button(
                label="🔧 EXPORT FULL RESULTS (JSON)",
                data=json_results,
                file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
<div style='text-align: center; color: #546e7a; padding: 2rem; font-size: 0.85rem;'>
    <p style='font-weight: 600; text-transform: uppercase; letter-spacing: 1px;'>⚠️ DEMO MODE ACTIVE</p>
    <p style='margin-top: 0.5rem;'>
        Current version displays placeholder data for demonstration purposes<br>
        Provide sample product URLs to enable production-grade data extraction
    </p>
    <p style='margin-top: 1.5rem; font-size: 0.8rem; color: #78909c;'>
        ⚙️ <b>SKU HARVESTER</b> v1.0.0 | Industrial-Grade Data Extraction Platform<br>
        Built with precision engineering | © 2024 All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)
