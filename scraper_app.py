"""
SKU HARVESTER - COMPLETE PRODUCTION VERSION
============================================
• Single URL + Bulk Upload modes
• Hybrid scraping (requests + Selenium)
• Long format specifications (4 columns)
• Professional engineered UI
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import re
import json

# Try Selenium (optional)
SELENIUM_AVAILABLE = False
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except:
    pass

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="SKU Harvester",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS
# ============================================================================

st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 10px;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
        border-left: 4px solid #3b82f6;
    }
    .success-box {
        background: #dcfce7;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #22c55e;
        margin: 1rem 0;
    }
    .info-box {
        background: #dbeafe;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SCRAPER CLASS
# ============================================================================

class HybridScraper:
    def __init__(self):
        self.driver = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.selenium_sites = ['amazon', 'flipkart']
    
    def init_selenium(self):
        if not SELENIUM_AVAILABLE or self.driver:
            return self.driver is not None
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            return True
        except:
            return False
    
    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def scrape_product(self, material_id, source, url):
        try:
            source_lower = source.lower()
            use_selenium = any(s in source_lower for s in self.selenium_sites)
            
            if use_selenium and SELENIUM_AVAILABLE:
                if self.init_selenium():
                    return self._scrape_selenium(material_id, source, url)
            
            return self._scrape_requests(material_id, source, url)
        except Exception as e:
            return self._error(material_id, source, url, str(e))
    
    def _scrape_requests(self, material_id, source, url):
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            source_lower = source.lower()
            if 'indiamart' in source_lower:
                return self._parse_indiamart(material_id, source, url, soup)
            elif 'industry' in source_lower:
                return self._parse_industrybuying(material_id, source, url, soup)
            else:
                return self._parse_generic(material_id, source, url, soup)
        except Exception as e:
            return self._error(material_id, source, url, f"Request failed: {str(e)}")
    
    def _scrape_selenium(self, material_id, source, url):
        try:
            self.driver.get(url)
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            if 'amazon' in source.lower():
                return self._parse_amazon(material_id, source, url, soup)
            else:
                return self._parse_generic(material_id, source, url, soup)
        except Exception as e:
            return self._error(material_id, source, url, f"Selenium error: {str(e)}")
    
    def _parse_indiamart(self, mid, src, url, soup):
        name = self._get_text(soup, ['h1', '.prd-name', '[itemprop="name"]'])
        price = self._get_price(soup, ['.price', '.pdp-price', '[itemprop="price"]']) or 'Contact Supplier'
        brand = self._get_text(soup, ['.company-name', '[itemprop="brand"]']) or 'N/A'
        
        specs = []
        for container in soup.select('.specifications, .pdp-specifications, .spec-table'):
            for row in container.select('tr'):
                cells = row.select('td, th')
                if len(cells) >= 2:
                    specs.append({
                        'materialId': mid,
                        'product_name': name,
                        'specification_name': cells[0].get_text().strip(),
                        'specification_value': cells[1].get_text().strip()
                    })
            
            for item in container.select('li, div'):
                text = item.get_text().strip()
                if ':' in text and len(text) < 200:
                    parts = text.split(':', 1)
                    if len(parts) == 2:
                        specs.append({
                            'materialId': mid,
                            'product_name': name,
                            'specification_name': parts[0].strip(),
                            'specification_value': parts[1].strip()
                        })
        
        if not name:
            return self._error(mid, src, url, "No product name found")
        
        return self._result(mid, src, url, name, price, brand, 'N/A', specs)
    
    def _parse_industrybuying(self, mid, src, url, soup):
        name = self._get_text(soup, ['h1', '.product-name', '.prd-title'])
        price = self._get_price(soup, ['.price', '.selling-price']) or 'N/A'
        brand = self._get_text(soup, ['.brand', '.manufacturer']) or 'N/A'
        
        specs = []
        spec_table = soup.select_one('.specifications, .spec-table')
        if spec_table:
            for row in spec_table.select('tr'):
                cells = row.select('td, th')
                if len(cells) >= 2:
                    specs.append({
                        'materialId': mid,
                        'product_name': name,
                        'specification_name': cells[0].get_text().strip(),
                        'specification_value': cells[1].get_text().strip()
                    })
        
        if not name:
            return self._error(mid, src, url, "No product name found")
        
        return self._result(mid, src, url, name, price, brand, 'N/A', specs)
    
    def _parse_amazon(self, mid, src, url, soup):
        name = self._get_text(soup, ['#productTitle', 'span#productTitle'])
        price = self._get_price(soup, ['.a-price-whole', '#priceblock_ourprice']) or 'N/A'
        brand_elem = soup.select_one('a#bylineInfo, #bylineInfo')
        brand = brand_elem.get_text().strip().replace('Visit the ', '').replace(' Store', '') if brand_elem else 'N/A'
        
        sku = 'N/A'
        asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
        if asin_match:
            sku = asin_match.group(1)
        
        specs = []
        for section in soup.select('#productDetails_techSpec_section_1, #productDetails_detailBullets_sections1'):
            for row in section.select('tr'):
                cells = row.select('th, td')
                if len(cells) >= 2:
                    specs.append({
                        'materialId': mid,
                        'product_name': name,
                        'specification_name': cells[0].get_text().strip(),
                        'specification_value': cells[1].get_text().strip()
                    })
        
        for bullet in soup.select('#feature-bullets li'):
            text = bullet.get_text().strip()
            if ':' in text:
                parts = text.split(':', 1)
                if len(parts) == 2:
                    specs.append({
                        'materialId': mid,
                        'product_name': name,
                        'specification_name': parts[0].strip(),
                        'specification_value': parts[1].strip()
                    })
        
        if not name:
            return self._error(mid, src, url, "No product name found")
        
        return self._result(mid, src, url, name, price, brand, sku, specs)
    
    def _parse_generic(self, mid, src, url, soup):
        name = self._get_text(soup, ['h1', '.product-name', '[itemprop="name"]'])
        if not name:
            return self._error(mid, src, url, f"Scraper not implemented for {src}")
        return self._result(mid, src, url, name, 'N/A', 'N/A', 'N/A', [])
    
    def _get_text(self, soup, selectors):
        for sel in selectors:
            elem = soup.select_one(sel)
            if elem:
                return elem.get_text().strip()
        return None
    
    def _get_price(self, soup, selectors):
        for sel in selectors:
            elem = soup.select_one(sel)
            if elem:
                text = elem.get_text().strip()
                match = re.search(r'₹\s*[\d,]+\.?\d*|Rs\.?\s*[\d,]+\.?\d*', text)
                if match:
                    return match.group().replace('Rs', '₹').replace(' ', '')
        return None
    
    def _result(self, mid, src, url, name, price, brand, sku, specs):
        return {
            'main': {
                'materialId': mid,
                'source': src,
                'product_url': url,
                'product_name': name,
                'price': price,
                'brand': brand,
                'sku': sku,
                'status': 'Success',
                'error_reason': '',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'specifications': specs
        }
    
    def _error(self, mid, src, url, reason):
        return {
            'main': {
                'materialId': mid,
                'source': src,
                'product_url': url,
                'product_name': 'N/A',
                'price': 'N/A',
                'brand': 'N/A',
                'sku': 'N/A',
                'status': 'Failed',
                'error_reason': reason,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'specifications': []
        }

# ============================================================================
# SESSION STATE
# ============================================================================

if 'total_scraped' not in st.session_state:
    st.session_state.total_scraped = 0
if 'scraping_mode' not in st.session_state:
    st.session_state.scraping_mode = 'single'

# ============================================================================
# UI
# ============================================================================

st.markdown('<h1 class="main-header">⚡ SKU HARVESTER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Industrial Data Extraction Platform</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ System")
    
    st.markdown("#### 🌐 Supported")
    st.markdown("✅ Amazon India")
    st.markdown("✅ Indiamart")
    st.markdown("✅ Industry Buying")
    st.markdown("🔄 Others (Coming Soon)")
    
    st.markdown("---")
    st.metric("Total Processed", st.session_state.total_scraped)

# Dashboard Stats
st.markdown("### 📊 Dashboard")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="stat-card"><h3>0</h3><p>Today</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-card"><h3>3</h3><p>Websites</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-card"><h3>0%</h3><p>Success Rate</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-card"><h3>Fast</h3><p>Hybrid Mode</p></div>', unsafe_allow_html=True)

st.markdown("---")

# Mode Selection
st.markdown("### 🚀 New Scraping Job")

col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Single Product", use_container_width=True):
        st.session_state.scraping_mode = 'single'
with col2:
    if st.button("📁 Bulk Upload", use_container_width=True):
        st.session_state.scraping_mode = 'bulk'

st.markdown("---")

# ============================================================================
# SINGLE MODE
# ============================================================================

if st.session_state.scraping_mode == 'single':
    st.markdown("### 🔍 Single Product Scraping")
    
    # Website selection
    website = st.selectbox(
        "Select Website",
        ["Amazon India", "Indiamart", "Industry Buying", "Moglix", "SKF", "Flipkart", "SMC"]
    )
    
    # URL input
    product_url = st.text_input(
        "Product URL",
        placeholder="Paste product URL here...",
        help="Enter the complete product page URL"
    )
    
    # Email section
    st.markdown("#### 📧 Email Results (Optional - Demo)")
    col1, col2 = st.columns(2)
    with col1:
        email_from = st.text_input("From", placeholder="sender@example.com")
    with col2:
        email_to = st.text_input("To", placeholder="recipient@example.com")
    
    # Scrape button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        scrape_btn = st.button("🚀 SCRAPE PRODUCT", type="primary", use_container_width=True)
    
    if scrape_btn:
        if not product_url:
            st.error("❌ Please enter a URL")
        else:
            with st.spinner("Scraping..."):
                scraper = HybridScraper()
                result = scraper.scrape_product(1, website, product_url)
                scraper.close()
                
                st.session_state.total_scraped += 1
            
            if result['main']['status'] == 'Success':
                st.markdown('<div class="success-box">✅ <b>Product Scraped Successfully!</b></div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown("### 📦 Product")
                    st.write(f"**Name:** {result['main']['product_name']}")
                    st.write(f"**Brand:** {result['main']['brand']}")
                    st.write(f"**SKU:** {result['main']['sku']}")
                with col2:
                    st.markdown("### 💰 Price")
                    st.markdown(f"## {result['main']['price']}")
                
                if result['specifications']:
                    st.markdown("---")
                    st.markdown("### 📋 Specifications")
                    spec_df = pd.DataFrame(result['specifications'])
                    st.dataframe(spec_df[['specification_name', 'specification_value']], use_container_width=True, hide_index=True)
                    
                    csv = spec_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "📥 Download Specifications",
                        csv,
                        f"specs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv"
                    )
                
                if email_from and email_to:
                    st.info(f"📧 Email would be sent to {email_to} (Demo Mode)")
            else:
                st.error(f"❌ Failed: {result['main']['error_reason']}")

# ============================================================================
# BULK MODE
# ============================================================================

else:
    st.markdown("### 📁 Bulk Upload Scraping")
    
    st.markdown("""
    <div class="info-box">
        <b>📋 File Format:</b> materialId | Source | Product URL
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📝 Download Template"):
        template = pd.DataFrame({
            'materialId': ['001', '002', '003'],
            'Source': ['Amazon India', 'Indiamart', 'Industry Buying'],
            'Product URL': [
                'https://www.amazon.in/dp/...',
                'https://www.indiamart.com/proddetail/...',
                'https://www.industrybuying.com/...'
            ]
        })
        st.dataframe(template)
        st.download_button(
            "📥 Download Template",
            template.to_csv(index=False),
            "template.csv"
        )
    
    uploaded_file = st.file_uploader("Upload File", type=['csv', 'xlsx', 'xls'])
    
    # Email section
    st.markdown("#### 📧 Email Results (Optional - Demo)")
    col1, col2 = st.columns(2)
    with col1:
        bulk_email_from = st.text_input("From", placeholder="sender@example.com", key="bulk_from")
    with col2:
        bulk_email_to = st.text_input("To", placeholder="recipient@example.com", key="bulk_to")
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            
            required = ['materialId', 'Source', 'Product URL']
            missing = [c for c in required if c not in df.columns]
            
            if missing:
                st.error(f"❌ Missing: {', '.join(missing)}")
            else:
                st.success("✅ File validated!")
                st.dataframe(df.head(10))
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total", len(df))
                with col2:
                    st.metric("Amazon/Flipkart", len(df[df['Source'].str.lower().str.contains('amazon|flipkart', na=False)]))
                with col3:
                    st.metric("Others", len(df) - len(df[df['Source'].str.lower().str.contains('amazon|flipkart', na=False)]))
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    bulk_scrape_btn = st.button("🚀 SCRAPE ALL", type="primary", use_container_width=True)
                
                if bulk_scrape_btn:
                    st.markdown("---")
                    st.markdown("### 🔄 Scraping...")
                    
                    scraper = HybridScraper()
                    main_results = []
                    all_specs = []
                    
                    progress = st.progress(0)
                    status = st.empty()
                    current = st.empty()
                    
                    for idx, row in df.iterrows():
                        current.info(f"📦 {row['materialId']} - {row['Source']}")
                        status.text(f"{idx + 1}/{len(df)}")
                        
                        result = scraper.scrape_product(row['materialId'], row['Source'], row['Product URL'])
                        main_results.append(result['main'])
                        all_specs.extend(result['specifications'])
                        
                        progress.progress((idx + 1) / len(df))
                        if idx < len(df) - 1:
                            time.sleep(1.5)
                    
                    scraper.close()
                    
                    current.empty()
                    status.text("✅ Complete!")
                    
                    st.session_state.total_scraped += len(df)
                    
                    # Summary
                    st.markdown("---")
                    st.markdown("### 📊 Summary")
                    
                    success = len([r for r in main_results if r['status'] == 'Success'])
                    rate = (success / len(main_results) * 100) if main_results else 0
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total", len(main_results))
                    with col2:
                        st.metric("✅ Success", success)
                    with col3:
                        st.metric("❌ Failed", len(main_results) - success)
                    with col4:
                        st.metric("Rate", f"{rate:.1f}%")
                    
                    # Results
                    st.markdown("---")
                    main_df = pd.DataFrame(main_results)
                    st.dataframe(main_df, use_container_width=True, hide_index=True)
                    
                    # Downloads
                    st.markdown("---")
                    st.markdown("### 📥 Downloads")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        csv_main = main_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "📄 Main Results",
                            csv_main,
                            f"main_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            "text/csv",
                            use_container_width=True
                        )
                    with col2:
                        if all_specs:
                            spec_df = pd.DataFrame(all_specs)
                            csv_specs = spec_df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                "📊 Specifications (Long Format)",
                                csv_specs,
                                f"specs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                "text/csv",
                                use_container_width=True
                            )
                            st.info(f"📊 {len(all_specs)} specification rows")
                        else:
                            st.info("No specifications found")
                    
                    if bulk_email_from and bulk_email_to:
                        st.info(f"📧 Results would be emailed to {bulk_email_to} (Demo)")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 2rem;'>
    <p><b>⚡ SKU Harvester v2.0</b> | Hybrid Extraction Platform</p>
</div>
""", unsafe_allow_html=True)
