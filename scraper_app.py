"""
SKU HARVESTER
=============
Professional web scraping tool for e-commerce product data extraction

Features:
- Single URL & Bulk scraping
- Multi-website support
- Email notifications (demo)
- Beautiful modern UI
- Progress tracking
- Data export
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
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - MODERN DESIGN
# ============================================================================

st.markdown("""
<style>
    /* Main Theme */
    :root {
        --primary-color: #2E7D32;
        --secondary-color: #66BB6A;
        --accent-color: #FFA726;
        --background: #F5F7FA;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .sub-header {
        text-align: center;
        color: #5F6368;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Card Styling */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
        border-left: 4px solid #2E7D32;
        transition: transform 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2E7D32;
        margin: 0;
    }
    
    .stat-label {
        color: #5F6368;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4);
        background: linear-gradient(135deg, #1B5E20 0%, #4CAF50 100%);
    }
    
    /* Section Styling */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2E7D32;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #66BB6A;
    }
    
    /* Info Boxes */
    .info-box {
        background: #E8F5E9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #FFF3E0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FF9800;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #E8F5E9;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
    }
    
    /* Tooltip Styling */
    .tooltip-text {
        font-size: 0.85rem;
        color: #757575;
        font-style: italic;
        margin-top: 0.3rem;
    }
    
    /* Upload Section */
    .upload-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin: 1.5rem 0;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #E8F5E9 0%, #F1F8E9 100%);
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #66BB6A, transparent);
    }
    
    /* Data Table */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #2E7D32, #66BB6A);
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

# ============================================================================
# SUPPORTED WEBSITES
# ============================================================================

SUPPORTED_WEBSITES = {
    "Amazon India": {
        "icon": "🛒",
        "color": "#FF9900",
        "pattern": "amazon.in"
    },
    "Flipkart": {
        "icon": "🏪",
        "color": "#2874F0",
        "pattern": "flipkart.com"
    },
    "IndiaMART": {
        "icon": "🏭",
        "color": "#4CAF50",
        "pattern": "indiamart.com"
    },
    "IndustryBuying": {
        "icon": "🔧",
        "color": "#E91E63",
        "pattern": "industrybuying.com"
    },
    "Moglix": {
        "icon": "⚙️",
        "color": "#FF5722",
        "pattern": "moglix.com"
    },
    "SKF India": {
        "icon": "⚡",
        "color": "#1565C0",
        "pattern": "skf.com"
    },
    "SMC Pneumatics": {
        "icon": "🔩",
        "color": "#43A047",
        "pattern": "smcpneumatics.com"
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
    
    # Check if all required columns exist
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        return False, f"Missing columns: {', '.join(missing_cols)}"
    
    # Check for empty values
    for col in required_columns:
        if df[col].isnull().any():
            return False, f"Column '{col}' contains empty values"
    
    return True, "File structure is valid"

def scrape_product_demo(url, website):
    """Demo scraping function - returns placeholder data"""
    time.sleep(0.5)  # Simulate scraping delay
    
    # Demo data based on website
    demo_data = {
        "Amazon India": {
            "product_name": "Industrial Ball Bearing Set",
            "brand": "SKF",
            "price": "₹1,250.00",
            "specs": {
                "Material": "Chrome Steel",
                "Inner Diameter": "25mm",
                "Outer Diameter": "52mm",
                "Weight": "0.15kg"
            }
        },
        "Flipkart": {
            "product_name": "Premium Pneumatic Cylinder",
            "brand": "SMC",
            "price": "₹2,850.00",
            "specs": {
                "Bore Size": "32mm",
                "Stroke Length": "50mm",
                "Operating Pressure": "1.0 MPa",
                "Material": "Aluminum"
            }
        },
        "Default": {
            "product_name": "Industrial Component",
            "brand": "Generic",
            "price": "₹999.00",
            "specs": {
                "Type": "Standard",
                "Material": "Steel",
                "Grade": "Industrial"
            }
        }
    }
    
    data = demo_data.get(website, demo_data["Default"])
    data['url'] = url
    data['website'] = website
    data['scraped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['status'] = 'Success'
    
    return data

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<h1 class="main-header">🌾 SKU HARVESTER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Professional E-Commerce Data Extraction Platform</p>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - SETTINGS & INFO
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    st.markdown("---")
    
    # Website Selection
    st.markdown("#### 🌐 Supported Websites")
    
    for website, info in SUPPORTED_WEBSITES.items():
        st.markdown(f"{info['icon']} **{website}**")
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("#### 📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total SKUs", st.session_state.total_scraped)
    with col2:
        st.metric("Jobs", st.session_state.jobs_completed)
    
    st.markdown("---")
    
    # Help Section
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        **Single URL Mode:**
        1. Select website
        2. Paste product URL
        3. Click Scrape
        
        **Bulk Mode:**
        1. Download template
        2. Fill with your data
        3. Upload file
        4. Click Scrape All
        
        **File Format:**
        - Column 1: RefNo
        - Column 2: SKUSource
        - Column 3: SKU Link
        """)
    
    with st.expander("🆘 Support"):
        st.markdown("""
        **Need Help?**
        
        Contact: support@skuharvester.com
        
        Documentation: [View Docs](#)
        """)

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

st.markdown('<p class="section-header">📊 Dashboard</p>', unsafe_allow_html=True)

# Dashboard Stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <p class="stat-number">0</p>
        <p class="stat-label">Total SKUs Scraped</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <p class="stat-number">0%</p>
        <p class="stat-label">Success Rate</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <p class="stat-number">0</p>
        <p class="stat-label">Jobs Today</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <p class="stat-number">7</p>
        <p class="stat-label">Websites Supported</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# SCRAPING MODE SELECTION
# ============================================================================

st.markdown('<p class="section-header">🚀 New Scraping Job</p>', unsafe_allow_html=True)

# Mode Selection with Icons
col1, col2 = st.columns(2)

with col1:
    single_mode = st.button("🔍 Single URL Scraping", use_container_width=True)
    st.markdown('<p class="tooltip-text">Extract data from one product URL at a time</p>', unsafe_allow_html=True)

with col2:
    bulk_mode = st.button("📁 Bulk Upload Scraping", use_container_width=True)
    st.markdown('<p class="tooltip-text">Upload CSV/Excel file with multiple URLs</p>', unsafe_allow_html=True)

# Set mode based on button clicks
if 'scraping_mode' not in st.session_state:
    st.session_state.scraping_mode = 'single'

if single_mode:
    st.session_state.scraping_mode = 'single'
if bulk_mode:
    st.session_state.scraping_mode = 'bulk'

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# SINGLE URL MODE
# ============================================================================

if st.session_state.scraping_mode == 'single':
    
    st.markdown("### 🔍 Single URL Scraping")
    
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    # Website Selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_website = st.selectbox(
            "🌐 Select Website",
            list(SUPPORTED_WEBSITES.keys()),
            help="Choose the e-commerce platform"
        )
        st.markdown('<p class="tooltip-text">Select the website source</p>', unsafe_allow_html=True)
    
    with col2:
        website_icon = SUPPORTED_WEBSITES[selected_website]['icon']
        st.markdown(f"<h1 style='text-align: center; font-size: 4rem;'>{website_icon}</h1>", unsafe_allow_html=True)
    
    # URL Input
    product_url = st.text_input(
        "🔗 Product URL",
        placeholder=f"Paste {selected_website} product URL here...",
        help="Full product page URL"
    )
    st.markdown('<p class="tooltip-text">Enter the complete product page link</p>', unsafe_allow_html=True)
    
    # Email Section
    st.markdown("#### 📧 Email Results (Optional)")
    col1, col2 = st.columns(2)
    
    with col1:
        email_from = st.text_input(
            "From Email",
            placeholder="sender@example.com",
            help="Sender email address"
        )
    
    with col2:
        email_to = st.text_input(
            "To Email",
            placeholder="recipient@example.com",
            help="Recipient email address"
        )
    
    st.markdown('<p class="tooltip-text">Email results will be sent after scraping completes</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Scrape Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        scrape_btn = st.button("🚀 START SCRAPING", use_container_width=True, type="primary")
    
    # Scraping Logic
    if scrape_btn:
        if not product_url:
            st.error("❌ Please enter a product URL")
        else:
            # Progress
            with st.spinner(f'🔄 Scraping from {selected_website}...'):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate scraping steps
                steps = [
                    "Connecting to website...",
                    "Loading page...",
                    "Extracting product data...",
                    "Parsing specifications...",
                    "Collecting price information...",
                    "Finalizing data..."
                ]
                
                for i, step in enumerate(steps):
                    status_text.text(f"⏳ {step}")
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(0.3)
                
                # Get data
                product_data = scrape_product_demo(product_url, selected_website)
                
                # Update session state
                st.session_state.total_scraped += 1
                st.session_state.jobs_completed += 1
            
            # Success message
            st.markdown('<div class="success-box">✅ <b>Product Successfully Scraped!</b></div>', unsafe_allow_html=True)
            
            # Display Results
            st.markdown("---")
            st.markdown("### 📦 Product Information")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Product Name:** {product_data['product_name']}")
                st.markdown(f"**Brand:** {product_data['brand']}")
                st.markdown(f"**Website:** {product_data['website']}")
                st.markdown(f"**Scraped At:** {product_data['scraped_at']}")
            
            with col2:
                st.markdown("### 💰 Price")
                st.markdown(f"<h2 style='color: #2E7D32;'>{product_data['price']}</h2>", unsafe_allow_html=True)
                st.markdown("**Status:** ✅ In Stock")
            
            # Specifications
            st.markdown("---")
            st.markdown("### 📋 Specifications")
            
            specs_df = pd.DataFrame(
                list(product_data['specs'].items()),
                columns=['Specification', 'Value']
            )
            
            st.dataframe(specs_df, use_container_width=True, hide_index=True)
            
            # Email Notification Demo
            if email_from and email_to:
                st.info(f"📧 Email would be sent from {email_from} to {email_to} (Demo Mode)")
            
            # Download Options
            st.markdown("---")
            st.markdown("### 📥 Download Data")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv_data = specs_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📄 Download CSV",
                    data=csv_data,
                    file_name=f"sku_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                json_data = json.dumps(product_data, indent=2)
                st.download_button(
                    label="🔧 Download JSON",
                    data=json_data,
                    file_name=f"sku_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col3:
                # Excel would go here in real implementation
                st.download_button(
                    label="📊 Download Excel",
                    data=csv_data,
                    file_name=f"sku_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.ms-excel",
                    use_container_width=True
                )

# ============================================================================
# BULK UPLOAD MODE
# ============================================================================

elif st.session_state.scraping_mode == 'bulk':
    
    st.markdown("### 📁 Bulk Upload Scraping")
    
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    # Info Box
    st.markdown("""
    <div class="info-box">
        <b>📋 Required File Format:</b><br>
        • Column 1: <b>RefNo</b> (Your reference number)<br>
        • Column 2: <b>SKUSource</b> (Website name)<br>
        • Column 3: <b>SKU Link</b> (Product URL)
    </div>
    """, unsafe_allow_html=True)
    
    # Template Download
    with st.expander("📝 Download Template File"):
        st.markdown("Use this template to prepare your bulk upload:")
        
        template_data = {
            "RefNo": ["REF001", "REF002", "REF003"],
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
            label="📥 Download CSV Template",
            data=template_csv,
            file_name="sku_harvester_template.csv",
            mime="text/csv"
        )
    
    # File Upload
    st.markdown("#### 📤 Upload Your File")
    uploaded_file = st.file_uploader(
        "Choose CSV or Excel file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload file with RefNo, SKUSource, and SKU Link columns"
    )
    st.markdown('<p class="tooltip-text">Drag and drop or click to browse</p>', unsafe_allow_html=True)
    
    if uploaded_file:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Validate file structure
            is_valid, message = validate_bulk_upload(df)
            
            if not is_valid:
                st.error(f"❌ {message}")
                df = None
            else:
                st.success(f"✅ {message}")
                
                # Auto-detect websites
                df['Detected_Website'] = df['SKU Link'].apply(detect_website)
                
                # Show preview with validation
                st.markdown("#### 📄 File Preview & Validation")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Total Products", len(df))
                with col2:
                    valid_urls = len(df[df['Detected_Website'] != 'Unknown'])
                    st.metric("✅ Valid URLs", valid_urls)
                with col3:
                    invalid_urls = len(df[df['Detected_Website'] == 'Unknown'])
                    st.metric("⚠️ Unknown URLs", invalid_urls)
                
                # Website breakdown
                st.markdown("#### 🌐 Website Breakdown")
                website_counts = df['Detected_Website'].value_counts()
                
                cols = st.columns(len(website_counts))
                for idx, (website, count) in enumerate(website_counts.items()):
                    with cols[idx]:
                        icon = SUPPORTED_WEBSITES.get(website, {}).get('icon', '❓')
                        st.metric(f"{icon} {website}", count)
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            df = None
    else:
        df = None
    
    # Email Section
    st.markdown("#### 📧 Email Results (Optional)")
    col1, col2 = st.columns(2)
    
    with col1:
        bulk_email_from = st.text_input(
            "From Email",
            placeholder="sender@example.com",
            key="bulk_from"
        )
    
    with col2:
        bulk_email_to = st.text_input(
            "To Email",
            placeholder="recipient@example.com",
            key="bulk_to"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Scrape Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        bulk_scrape_btn = st.button(
            "🚀 START BULK SCRAPING",
            use_container_width=True,
            type="primary",
            disabled=(df is None)
        )
    
    # Bulk Scraping Logic
    if bulk_scrape_btn and df is not None:
        st.markdown("---")
        st.markdown("### 🔄 Scraping Progress")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        current_product = st.empty()
        
        results = []
        
        # Scrape each product
        for idx, row in df.iterrows():
            current_product.info(f"📦 Scraping: {row['RefNo']} - {row['SKUSource']}")
            status_text.text(f"Processing {idx + 1} of {len(df)}...")
            
            # Scrape
            try:
                product_data = scrape_product_demo(row['SKU Link'], row['SKUSource'])
                product_data['RefNo'] = row['RefNo']
                results.append(product_data)
            except Exception as e:
                results.append({
                    'RefNo': row['RefNo'],
                    'status': 'Failed',
                    'error': str(e)
                })
            
            progress_bar.progress((idx + 1) / len(df))
        
        current_product.empty()
        status_text.text("✅ All products scraped successfully!")
        
        # Update session state
        st.session_state.total_scraped += len(results)
        st.session_state.jobs_completed += 1
        
        st.markdown("---")
        
        # Results Summary
        st.markdown("### 📊 Scraping Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Processed", len(results))
        with col2:
            success_count = len([r for r in results if r.get('status') == 'Success'])
            st.metric("Successful", success_count)
        with col3:
            failed_count = len([r for r in results if r.get('status') == 'Failed'])
            st.metric("Failed", failed_count)
        with col4:
            success_rate = (success_count / len(results) * 100) if results else 0
            st.metric("Success Rate", f"{success_rate:.1f}%")
        
        st.markdown("---")
        
        # Results Table
        st.markdown("### 📋 Scraped Products")
        
        results_df = pd.DataFrame(results)
        st.dataframe(results_df, use_container_width=True, hide_index=True)
        
        # Email notification demo
        if bulk_email_from and bulk_email_to:
            st.info(f"📧 Results would be emailed from {bulk_email_from} to {bulk_email_to} (Demo Mode)")
        
        # Download Results
        st.markdown("---")
        st.markdown("### 📥 Download Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv_results = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📄 Download Full Results (CSV)",
                data=csv_results,
                file_name=f"bulk_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            json_results = json.dumps(results, indent=2)
            st.download_button(
                label="🔧 Download Full Results (JSON)",
                data=json_results,
                file_name=f"bulk_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
<div style='text-align: center; color: #757575; padding: 2rem;'>
    <p style='font-size: 0.9rem;'>⚠️ <b>Demo Version</b> - Currently showing placeholder data</p>
    <p style='font-size: 0.85rem; margin-top: 0.5rem;'>
        Provide sample product URLs from your target websites to enable real scraping functionality
    </p>
    <p style='margin-top: 1.5rem; font-size: 0.85rem;'>
        🌾 <b>SKU Harvester</b> v1.0 | Built with ❤️ using Streamlit | © 2024
    </p>
</div>
""", unsafe_allow_html=True)
