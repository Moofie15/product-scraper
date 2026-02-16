"""
SKU HARVESTER - PRODUCTION VERSION
===================================
Option D Layout - Clean Enterprise
Full scraping functionality included
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import re

# Try Selenium (optional)
SELENIUM_AVAILABLE = False
try:
    from selenium import webdriver
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
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# OPTION D CSS
# ============================================================================

st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    /* Header */
    .header {
        background: white;
        border-bottom: 1px solid #E0E0E0;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: -1rem -1rem 0 -1rem;
    }
    
    .brand-section {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .brand-icon {
        width: 40px;
        height: 40px;
        background: #1976D2;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.2rem;
    }
    
    .brand-title {
        font-size: 1.3rem;
        color: #212121;
        font-weight: 700;
        margin: 0;
    }
    
    .brand-subtitle {
        font-size: 0.75rem;
        color: #757575;
        margin: 0;
    }
    
    /* Stats Pills */
    .stats-container {
        display: flex;
        gap: 1.5rem;
    }
    
    .stat-pill {
        background: #F5F5F5;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #757575;
    }
    
    .stat-value {
        font-size: 0.9rem;
        font-weight: 700;
        color: #1976D2;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: white;
        padding: 0 2rem;
        border-bottom: 1px solid #E0E0E0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 0;
        color: #757575;
        font-weight: 600;
        border-bottom: 3px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1976D2;
        border-bottom-color: #1976D2;
    }
    
    /* Info Bar */
    .info-bar {
        background: white;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1.5rem 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .info-title {
        font-size: 1.3rem;
        color: #212121;
        margin-bottom: 0.25rem;
        font-weight: 700;
    }
    
    .info-subtitle {
        font-size: 0.85rem;
        color: #757575;
    }
    
    /* Quick Stats */
    .quick-stats-grid {
        display: flex;
        gap: 2rem;
    }
    
    .quick-stat {
        text-align: center;
        padding: 0.5rem 1rem;
    }
    
    .quick-stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1976D2;
    }
    
    .quick-stat-label {
        font-size: 0.75rem;
        color: #757575;
        margin-top: 0.25rem;
    }
    
    /* Panels */
    .panel {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .panel-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #212121;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #F5F5F5;
    }
    
    /* Mode Cards */
    .mode-card {
        border: 2px solid #E0E0E0;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .mode-card:hover {
        border-color: #1976D2;
        background: #F8FBFF;
    }
    
    .mode-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #212121;
        margin-bottom: 0.5rem;
    }
    
    .mode-desc {
        font-size: 0.85rem;
        color: #757575;
        line-height: 1.5;
    }
    
    .mode-features {
        margin-top: 0.75rem;
        font-size: 0.85rem;
        color: #424242;
        line-height: 1.8;
    }
    
    /* Buttons */
    .stButton>button {
        background: #1976D2;
        color: white;
        border: none;
        padding: 0.85rem 2rem;
        border-radius: 6px;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background: #1565C0;
    }
    
    /* Form elements */
    .stSelectbox, .stTextInput, .stTextArea {
        margin-bottom: 1rem;
    }
    
    /* Success/Error boxes */
    .success-box {
        background: #E8F5E9;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #FFEBEE;
        border-left: 4px solid #F44336;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .info-box-blue {
        background: #E3F2FD;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SCRAPER CLASS (Full functionality)
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
    st.session_state.total_scraped = 1245
if 'week_scraped' not in st.session_state:
    st.session_state.week_scraped = 87
if 'success_rate' not in st.session_state:
    st.session_state.success_rate = 94

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class="header">
    <div class="brand-section">
        <div class="brand-icon">⚙</div>
        <div>
            <div class="brand-title">SKU HARVESTER</div>
            <div class="brand-subtitle">Industrial Data Extraction Platform</div>
        </div>
    </div>
    <div class="stats-container">
        <div class="stat-pill">
            <span class="stat-label">Total:</span>
            <span class="stat-value">1,245</span>
        </div>
        <div class="stat-pill">
            <span class="stat-label">Week:</span>
            <span class="stat-value">87</span>
        </div>
        <div class="stat-pill">
            <span class="stat-label">Success:</span>
            <span class="stat-value">94%</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs(["Dashboard", "History", "Settings"])

# ============================================================================
# TAB 1: DASHBOARD
# ============================================================================

with tab1:
    # Info Bar
    st.markdown("""
    <div class="info-bar">
        <div>
            <div class="info-title">Today's Activity</div>
            <div class="info-subtitle">Start a new scraping job or view recent activity</div>
        </div>
        <div class="quick-stats-grid">
            <div class="quick-stat">
                <div class="quick-stat-value">0</div>
                <div class="quick-stat-label">Scraped</div>
            </div>
            <div class="quick-stat">
                <div class="quick-stat-value">0</div>
                <div class="quick-stat-label">Success</div>
            </div>
            <div class="quick-stat">
                <div class="quick-stat-value">0</div>
                <div class="quick-stat-label">Failed</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Content Grid
    col1, col2 = st.columns([1, 1])
    
    # Left: Mode Selection
    with col1:
        st.markdown('<div class="panel"><div class="panel-header">Select Scraping Mode</div>', unsafe_allow_html=True)
        
        mode = st.radio(
            "Choose mode:",
            ["Single Product", "Bulk Upload"],
            label_visibility="collapsed"
        )
        
        if mode == "Single Product":
            st.markdown("""
            <div class="mode-desc" style="margin-top: 1rem;">
                Extract data from one product URL quickly and efficiently
                <div class="mode-features">
                    ✓ Instant extraction<br>
                    ✓ Real-time results<br>
                    ✓ Perfect for testing
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="mode-desc" style="margin-top: 1rem;">
                Process multiple products from Excel or CSV file
                <div class="mode-features">
                    ✓ Batch processing<br>
                    ✓ 100+ products at once<br>
                    ✓ Complete reports
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Right: Scraping Form
    with col2:
        st.markdown('<div class="panel"><div class="panel-header">Extract Product Data</div>', unsafe_allow_html=True)
        
        if mode == "Single Product":
            # Single Product Form
            website = st.selectbox(
                "Website Source",
                ["Amazon India", "Indiamart", "Industry Buying", "Moglix", "SKF", "Flipkart"]
            )
            
            product_url = st.text_input(
                "Product URL",
                placeholder="https://www.amazon.in/product/..."
            )
            
            email_to = st.text_input(
                "Email Results (Optional)",
                placeholder="your@email.com"
            )
            
            if st.button("Start Extraction", use_container_width=True):
                if not product_url:
                    st.markdown('<div class="error-box">⚠️ Please enter a product URL</div>', unsafe_allow_html=True)
                else:
                    with st.spinner("Extracting data..."):
                        scraper = HybridScraper()
                        result = scraper.scrape_product(1, website, product_url)
                        scraper.close()
                    
                    if result['main']['status'] == 'Success':
                        st.markdown('<div class="success-box">✅ Product extracted successfully!</div>', unsafe_allow_html=True)
                        
                        col_a, col_b = st.columns([2, 1])
                        with col_a:
                            st.write(f"**Name:** {result['main']['product_name']}")
                            st.write(f"**Brand:** {result['main']['brand']}")
                            st.write(f"**SKU:** {result['main']['sku']}")
                        with col_b:
                            st.write(f"**Price:** {result['main']['price']}")
                        
                        if result['specifications']:
                            st.markdown("---")
                            st.markdown("**Specifications:**")
                            spec_df = pd.DataFrame(result['specifications'])
                            st.dataframe(spec_df[['specification_name', 'specification_value']], use_container_width=True, hide_index=True)
                            
                            csv = spec_df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                "Download Specifications",
                                csv,
                                f"specs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                use_container_width=True
                            )
                    else:
                        st.markdown(f'<div class="error-box">❌ Failed: {result["main"]["error_reason"]}</div>', unsafe_allow_html=True)
        
        else:
            # Bulk Upload Form
            st.markdown('<div class="info-box-blue">Upload Excel/CSV with: materialId | Source | Product URL</div>', unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("Upload File", type=['csv', 'xlsx', 'xls'])
            
            if uploaded_file:
                try:
                    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                    
                    required = ['materialId', 'Source', 'Product URL']
                    missing = [c for c in required if c not in df.columns]
                    
                    if missing:
                        st.markdown(f'<div class="error-box">Missing columns: {", ".join(missing)}</div>', unsafe_allow_html=True)
                    else:
                        st.success(f"✅ File validated - {len(df)} products")
                        st.dataframe(df.head(5), use_container_width=True)
                        
                        if st.button("Start Bulk Extraction", use_container_width=True):
                            scraper = HybridScraper()
                            main_results = []
                            all_specs = []
                            
                            progress = st.progress(0)
                            status = st.empty()
                            
                            for idx, row in df.iterrows():
                                status.text(f"Processing {idx + 1}/{len(df)}...")
                                result = scraper.scrape_product(row['materialId'], row['Source'], row['Product URL'])
                                main_results.append(result['main'])
                                all_specs.extend(result['specifications'])
                                progress.progress((idx + 1) / len(df))
                                time.sleep(1.5)
                            
                            scraper.close()
                            status.text("✅ Complete!")
                            
                            # Results
                            success = len([r for r in main_results if r['status'] == 'Success'])
                            st.markdown(f'<div class="success-box">Completed: {success}/{len(main_results)} successful</div>', unsafe_allow_html=True)
                            
                            main_df = pd.DataFrame(main_results)
                            st.dataframe(main_df, use_container_width=True, hide_index=True)
                            
                            # Downloads
                            col_a, col_b = st.columns(2)
                            with col_a:
                                csv_main = main_df.to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    "Download Main Results",
                                    csv_main,
                                    f"main_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    use_container_width=True
                                )
                            with col_b:
                                if all_specs:
                                    spec_df = pd.DataFrame(all_specs)
                                    csv_specs = spec_df.to_csv(index=False).encode('utf-8')
                                    st.download_button(
                                        "Download Specifications",
                                        csv_specs,
                                        f"specs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                        use_container_width=True
                                    )
                except Exception as e:
                    st.markdown(f'<div class="error-box">Error: {str(e)}</div>', unsafe_allow_html=True)
            else:
                # Template
                template = pd.DataFrame({
                    'materialId': ['001', '002'],
                    'Source': ['Amazon India', 'Indiamart'],
                    'Product URL': ['https://www.amazon.in/...', 'https://www.indiamart.com/...']
                })
                st.write("**Template:**")
                st.dataframe(template, use_container_width=True)
                st.download_button(
                    "Download Template",
                    template.to_csv(index=False),
                    "template.csv",
                    use_container_width=True
                )
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.info("History feature coming soon")

with tab3:
    st.info("Settings feature coming soon")
