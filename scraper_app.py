"""
E-COMMERCE PRODUCT SCRAPER
Web Interface using Streamlit

Run: streamlit run scraper_app.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Page Configuration
st.set_page_config(
    page_title="E-Commerce Product Scraper",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .success-box {
        padding: 1.5rem;
        background: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1.5rem;
        background: #f8d7da;
        border-left: 5px solid #dc3545;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1.5rem;
        background: #d1ecf1;
        border-left: 5px solid #17a2b8;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .spec-table {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🛍️ E-Commerce Product Scraper</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Extract product details and prices from multiple e-commerce websites</p>', unsafe_allow_html=True)

# Sidebar - Website Selection and Info
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Website Selection
    website = st.selectbox(
        "📌 Select Website",
        [
            "Amazon India",
            "Flipkart",
            "IndiaMART",
            "IndustryBuying",
            "Moglix",
            "SKF India",
            "SMC Pneumatics"
        ],
        help="Choose the e-commerce website you want to scrape"
    )
    
    st.divider()
    
    # Info Section
    st.subheader("ℹ️ About")
    st.info("""
    This tool helps you extract:
    - Product specifications
    - Current prices
    - Product details
    
    **Supports:**
    - Single product scraping
    - Bulk product scraping (CSV/Excel)
    """)
    
    st.divider()
    
    # Statistics (Demo)
    st.subheader("📊 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Products Scraped", "0", "0")
    with col2:
        st.metric("Success Rate", "0%", "0%")

# Main Content Area
st.divider()

# Mode Selection
scraping_mode = st.radio(
    "**Choose Scraping Mode:**",
    ["🔍 Single Product URL", "📁 Bulk Upload (CSV/Excel)"],
    horizontal=True,
    help="Select whether you want to scrape one product or multiple products"
)

st.divider()

# Single Product Mode
if scraping_mode == "🔍 Single Product URL":
    st.subheader("Single Product Scraping")
    
    # URL Input
    product_url = st.text_input(
        "**Product URL:**",
        placeholder="Paste product URL here (e.g., https://www.amazon.in/dp/B08X...)",
        help="Enter the full product page URL from the selected website"
    )
    
    # Show example based on selected website
    with st.expander("💡 See URL Format Examples"):
        examples = {
            "Amazon India": "https://www.amazon.in/dp/B08XXXX...",
            "Flipkart": "https://www.flipkart.com/product-name/p/itmxxx...",
            "IndiaMART": "https://www.indiamart.com/proddetail/product-name-xxx.html",
            "IndustryBuying": "https://www.industrybuying.com/product-name-xxx/",
            "Moglix": "https://www.moglix.com/product-name/xxx",
            "SKF India": "https://www.skf.com/in/products/rolling-bearings/...",
            "SMC Pneumatics": "https://www.smcpneumatics.com/product/..."
        }
        st.code(examples.get(website, "URL format"), language="text")
    
    st.markdown("")  # Spacing
    
    # Scrape Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        scrape_button = st.button("🚀 SCRAPE PRODUCT", use_container_width=True)
    
    # Results Section (Demo)
    if scrape_button:
        if not product_url:
            st.markdown('<div class="error-box">❌ <b>Error:</b> Please enter a product URL</div>', unsafe_allow_html=True)
        else:
            # Show loading
            with st.spinner(f"🔄 Scraping product from {website}..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Demo Success Message
                st.markdown('<div class="success-box">✅ <b>Product Successfully Scraped!</b></div>', unsafe_allow_html=True)
                
                # Demo Product Details
                st.markdown("---")
                
                # Product Info
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### 📦 Product Information")
                    st.markdown("**Product Name:** SKF Ball Bearing 6205-2RS1")
                    st.markdown("**Brand:** SKF")
                    st.markdown("**Product Code:** 6205-2RS1")
                
                with col2:
                    st.markdown("### 💰 Pricing")
                    st.markdown("**Current Price:**")
                    st.markdown("## ₹450.00")
                    st.markdown("**Status:** ✅ In Stock")
                
                st.markdown("---")
                
                # Specifications
                st.markdown("### 📋 Product Specifications")
                
                # Demo specifications table
                specs_data = {
                    "Specification": [
                        "Inner Diameter",
                        "Outer Diameter",
                        "Width",
                        "Material",
                        "Seal Type",
                        "Cage Material",
                        "Weight",
                        "Load Rating (Dynamic)"
                    ],
                    "Value": [
                        "25 mm",
                        "52 mm",
                        "15 mm",
                        "Chrome Steel",
                        "2RS1 (Double Rubber Sealed)",
                        "Steel",
                        "0.13 kg",
                        "7800 N"
                    ]
                }
                
                specs_df = pd.DataFrame(specs_data)
                st.dataframe(specs_df, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                
                # Download Section
                st.markdown("### 📥 Download Data")
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    # Create demo CSV data
                    csv_data = specs_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📄 Download as CSV",
                        data=csv_data,
                        file_name=f"product_specs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col2:
                    # Excel download (demo)
                    st.download_button(
                        label="📊 Download as Excel",
                        data=csv_data,  # In real version, this would be Excel format
                        file_name=f"product_specs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.ms-excel",
                        use_container_width=True
                    )
                
                with col3:
                    # JSON download (demo)
                    import json
                    json_data = json.dumps({
                        "product_name": "SKF Ball Bearing 6205-2RS1",
                        "price": 450.00,
                        "currency": "INR",
                        "specifications": specs_data
                    }, indent=2)
                    st.download_button(
                        label="🔧 Download as JSON",
                        data=json_data,
                        file_name=f"product_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )

# Bulk Upload Mode
else:
    st.subheader("Bulk Product Scraping")
    
    st.markdown('<div class="info-box">ℹ️ <b>Upload a CSV or Excel file</b> containing product URLs. The file should have a column named "URL" with product links.</div>', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "**Upload CSV or Excel File:**",
        type=['csv', 'xlsx', 'xls'],
        help="Upload a file with product URLs. Column name should be 'URL'"
    )
    
    # Show template download option
    with st.expander("📝 Download Template File"):
        st.markdown("Use this template to prepare your URLs:")
        
        # Create demo template
        template_data = {
            "URL": [
                "https://www.amazon.in/dp/B08XXXX1",
                "https://www.amazon.in/dp/B08XXXX2",
                "https://www.amazon.in/dp/B08XXXX3"
            ],
            "Product_Name": [
                "Product 1 (Optional)",
                "Product 2 (Optional)",
                "Product 3 (Optional)"
            ]
        }
        template_df = pd.DataFrame(template_data)
        
        st.dataframe(template_df, use_container_width=True, hide_index=True)
        
        # Download template
        template_csv = template_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV Template",
            data=template_csv,
            file_name="product_urls_template.csv",
            mime="text/csv"
        )
    
    st.markdown("")  # Spacing
    
    if uploaded_file:
        # Display uploaded file preview
        st.markdown("### 📄 File Preview")
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.dataframe(df.head(10), use_container_width=True)
            st.info(f"📊 Total products to scrape: **{len(df)}**")
            
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            df = None
    else:
        df = None
    
    st.markdown("")  # Spacing
    
    # Scrape Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        bulk_scrape_button = st.button("🚀 SCRAPE ALL PRODUCTS", use_container_width=True, disabled=(df is None))
    
    # Bulk Results Section (Demo)
    if bulk_scrape_button and df is not None:
        st.markdown("---")
        st.markdown("### 🔄 Scraping Progress")
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Demo scraping simulation
        for i in range(len(df)):
            status_text.text(f"Scraping product {i+1} of {len(df)}...")
            progress_bar.progress((i + 1) / len(df))
            time.sleep(0.1)  # Simulate scraping time
        
        status_text.text("✅ All products scraped successfully!")
        
        st.markdown("---")
        
        # Show results summary
        st.markdown("### 📊 Scraping Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Products", len(df))
        with col2:
            st.metric("Successfully Scraped", len(df))
        with col3:
            st.metric("Failed", 0)
        with col4:
            st.metric("Success Rate", "100%")
        
        st.markdown("---")
        
        # Demo results table
        st.markdown("### 📋 Scraped Products Preview")
        
        results_data = {
            "Product Name": [
                "SKF Ball Bearing 6205",
                "SMC Cylinder CDQ2B32-50D",
                "OMRON Safety Switch D4NL"
            ],
            "Price (₹)": [450.00, 2850.00, 1200.00],
            "Brand": ["SKF", "SMC", "OMRON"],
            "Status": ["In Stock", "In Stock", "Limited Stock"]
        }
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Download bulk results
        st.markdown("### 📥 Download Results")
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📄 Download Full Results (CSV)",
                data=csv_data,
                file_name=f"bulk_scrape_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            st.download_button(
                label="📊 Download Full Results (Excel)",
                data=csv_data,
                file_name=f"bulk_scrape_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.ms-excel",
                use_container_width=True
            )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>⚠️ <b>Note:</b> This is currently a DEMO interface. Scraping functionality will be added once you provide sample product URLs.</p>
    <p>Built with ❤️ using Streamlit | © 2024 Product Scraper Tool</p>
</div>
""", unsafe_allow_html=True)
