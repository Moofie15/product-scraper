"""
SKU HARVESTER - HYBRID PRODUCTION VERSION
==========================================
Hybrid scraping: Requests for simple sites, Selenium for complex sites
Auto-generates specifications in LONG FORMAT
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

# Try to import Selenium (optional)
SELENIUM_AVAILABLE = False
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except:
    pass

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="SKU Harvester",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
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
        border: none;
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
# HYBRID SCRAPER CLASS
# ============================================================================

class HybridScraper:
    """
    Hybrid scraper: requests for simple sites, Selenium for complex
    """
    
    def __init__(self):
        self.driver = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Define which sites use which method
        self.selenium_sites = ['amazon', 'flipkart']
        self.requests_sites = ['indiamart', 'industry', 'moglix', 'skf', 'smc']
    
    def init_selenium(self):
        """Initialize Selenium if available"""
        if not SELENIUM_AVAILABLE:
            return False
        
        if self.driver is None:
            try:
                options = Options()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                
                self.driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    options=options
                )
                return True
            except:
                return False
        return True
    
    def close_selenium(self):
        """Close Selenium driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def scrape_product(self, material_id, source, url):
        """
        Main scraping router
        """
        try:
            source_lower = source.lower()
            
            # Determine method
            use_selenium = any(site in source_lower for site in self.selenium_sites)
            
            if use_selenium:
                if not SELENIUM_AVAILABLE or not self.init_selenium():
                    # Fallback to requests
                    return self._scrape_with_requests(material_id, source, url)
                return self._scrape_with_selenium(material_id, source, url)
            else:
                return self._scrape_with_requests(material_id, source, url)
                
        except Exception as e:
            return self._create_error_result(material_id, source, url, f"Error: {str(e)}")
    
    def _scrape_with_requests(self, material_id, source, url):
        """Scrape using requests + BeautifulSoup"""
        try:
            source_lower = source.lower()
            
            # Make request
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Route to appropriate parser
            if 'indiamart' in source_lower:
                return self._parse_indiamart(material_id, source, url, soup)
            elif 'industry' in source_lower:
                return self._parse_industrybuying(material_id, source, url, soup)
            elif 'amazon' in source_lower:
                return self._parse_amazon_requests(material_id, source, url, soup)
            else:
                return self._parse_generic(material_id, source, url, soup)
                
        except requests.Timeout:
            return self._create_error_result(material_id, source, url, "Timeout - Page took too long")
        except requests.RequestException as e:
            return self._create_error_result(material_id, source, url, f"Network error: {str(e)}")
        except Exception as e:
            return self._create_error_result(material_id, source, url, f"Parse error: {str(e)}")
    
    def _scrape_with_selenium(self, material_id, source, url):
        """Scrape using Selenium"""
        try:
            self.driver.get(url)
            time.sleep(3)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            source_lower = source.lower()
            if 'amazon' in source_lower:
                return self._parse_amazon_selenium(material_id, source, url, soup)
            else:
                return self._parse_generic(material_id, source, url, soup)
                
        except Exception as e:
            return self._create_error_result(material_id, source, url, f"Selenium error: {str(e)}")
    
    def _parse_indiamart(self, material_id, source, url, soup):
        """Parse Indiamart page"""
        # Product name
        product_name = None
        for selector in ['h1', '.prd-name', '.pdp-heading', '[itemprop="name"]']:
            elem = soup.select_one(selector)
            if elem:
                product_name = elem.get_text().strip()
                break
        
        # Price
        price = 'Contact Supplier'
        for selector in ['.price', '.pdp-price', '[itemprop="price"]', '.prc']:
            elem = soup.select_one(selector)
            if elem:
                price_text = elem.get_text().strip()
                if '₹' in price_text or 'Rs' in price_text:
                    price = self._clean_price(price_text)
                break
        
        # Brand
        brand = 'N/A'
        for selector in ['.company-name', '.brand', '[itemprop="brand"]']:
            elem = soup.select_one(selector)
            if elem:
                brand = elem.get_text().strip()
                break
        
        # Specifications
        specifications = []
        
        # Try to find specification tables/lists
        spec_containers = soup.select('.specifications, .pdp-specifications, .prod-spec, .spec-table')
        
        for container in spec_containers:
            # Try table rows
            rows = container.select('tr')
            for row in rows:
                cells = row.select('td, th')
                if len(cells) >= 2:
                    spec_name = cells[0].get_text().strip()
                    spec_value = cells[1].get_text().strip()
                    if spec_name and spec_value and len(spec_name) < 100:
                        specifications.append({
                            'materialId': material_id,
                            'product_name': product_name,
                            'specification_name': spec_name,
                            'specification_value': spec_value
                        })
            
            # Try list items with colon separator
            items = container.select('li, .spec-item, div')
            for item in items:
                text = item.get_text().strip()
                if ':' in text and len(text) < 200:
                    parts = text.split(':', 1)
                    if len(parts) == 2:
                        spec_name = parts[0].strip()
                        spec_value = parts[1].strip()
                        if spec_name and spec_value:
                            specifications.append({
                                'materialId': material_id,
                                'product_name': product_name,
                                'specification_name': spec_name,
                                'specification_value': spec_value
                            })
        
        if not product_name:
            return self._create_error_result(material_id, source, url, "Could not extract product name")
        
        return {
            'main': {
                'materialId': material_id,
                'source': source,
                'product_url': url,
                'product_name': product_name,
                'price': price,
                'brand': brand,
                'sku': 'N/A',
                'status': 'Success',
                'error_reason': '',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'specifications': specifications
        }
    
    def _parse_industrybuying(self, material_id, source, url, soup):
        """Parse Industry Buying page"""
        # Product name
        product_name = None
        for selector in ['h1', '.product-name', '.prd-title', 'h1.title']:
            elem = soup.select_one(selector)
            if elem:
                product_name = elem.get_text().strip()
                break
        
        # Price
        price = 'N/A'
        for selector in ['.price', '.selling-price', '.product-price', '.prc']:
            elem = soup.select_one(selector)
            if elem:
                price = self._clean_price(elem.get_text())
                break
        
        # Brand
        brand = 'N/A'
        for selector in ['.brand', '.manufacturer', '.brand-name']:
            elem = soup.select_one(selector)
            if elem:
                brand = elem.get_text().strip()
                break
        
        # Specifications
        specifications = []
        spec_table = soup.select_one('.specifications, .product-specifications, .spec-table')
        
        if spec_table:
            rows = spec_table.select('tr')
            for row in rows:
                cells = row.select('td, th')
                if len(cells) >= 2:
                    specifications.append({
                        'materialId': material_id,
                        'product_name': product_name,
                        'specification_name': cells[0].get_text().strip(),
                        'specification_value': cells[1].get_text().strip()
                    })
        
        if not product_name:
            return self._create_error_result(material_id, source, url, "Could not extract product name")
        
        return {
            'main': {
                'materialId': material_id,
                'source': source,
                'product_url': url,
                'product_name': product_name,
                'price': price,
                'brand': brand,
                'sku': 'N/A',
                'status': 'Success',
                'error_reason': '',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'specifications': specifications
        }
    
    def _parse_amazon_requests(self, material_id, source, url, soup):
        """Parse Amazon with requests (limited)"""
        # This will be basic - Selenium version is better
        product_name = None
        title_elem = soup.select_one('#productTitle, span#productTitle')
        if title_elem:
            product_name = title_elem.get_text().strip()
        
        price = 'N/A'
        price_elem = soup.select_one('.a-price-whole, #priceblock_ourprice')
        if price_elem:
            price = self._clean_price(price_elem.get_text())
        
        specifications = []
        # Amazon specs are usually JavaScript-loaded, so this will be limited
        
        if not product_name:
            return self._create_error_result(material_id, source, url, "Amazon requires Selenium for full data")
        
        return {
            'main': {
                'materialId': material_id,
                'source': source,
                'product_url': url,
                'product_name': product_name,
                'price': price,
                'brand': 'N/A',
                'sku': 'N/A',
                'status': 'Partial',
                'error_reason': 'Limited data (Selenium recommended)',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'specifications': specifications
        }
    
    def _parse_amazon_selenium(self, material_id, source, url, soup):
        """Parse Amazon with Selenium (full)"""
        # Product name
        product_name = None
        for selector in ['#productTitle', 'span#productTitle', 'h1.product-title']:
            elem = soup.select_one(selector)
            if elem:
                product_name = elem.get_text().strip()
                break
        
        # Price
        price = 'N/A'
        for selector in ['.a-price-whole', 'span.a-price-whole', '#priceblock_ourprice']:
            elem = soup.select_one(selector)
            if elem:
                price = self._clean_price(elem.get_text())
                break
        
        # Brand
        brand = 'N/A'
        brand_elem = soup.select_one('a#bylineInfo, #bylineInfo')
        if brand_elem:
            brand = brand_elem.get_text().strip().replace('Visit the ', '').replace(' Store', '')
        
        # SKU/ASIN
        sku = 'N/A'
        asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
        if asin_match:
            sku = asin_match.group(1)
        
        # Specifications
        specifications = []
        
        # Technical details table
        tech_sections = soup.select('#productDetails_techSpec_section_1, #productDetails_detailBullets_sections1, .prodDetTable')
        for section in tech_sections:
            rows = section.select('tr')
            for row in rows:
                cells = row.select('th, td')
                if len(cells) >= 2:
                    spec_name = cells[0].get_text().strip()
                    spec_value = cells[1].get_text().strip()
                    if spec_name and spec_value:
                        specifications.append({
                            'materialId': material_id,
                            'product_name': product_name,
                            'specification_name': spec_name,
                            'specification_value': spec_value
                        })
        
        # Feature bullets
        bullets = soup.select('#feature-bullets li, .a-unordered-list li')
        for bullet in bullets:
            text = bullet.get_text().strip()
            if ':' in text:
                parts = text.split(':', 1)
                if len(parts) == 2:
                    specifications.append({
                        'materialId': material_id,
                        'product_name': product_name,
                        'specification_name': parts[0].strip(),
                        'specification_value': parts[1].strip()
                    })
        
        if not product_name:
            return self._create_error_result(material_id, source, url, "Could not extract product name")
        
        return {
            'main': {
                'materialId': material_id,
                'source': source,
                'product_url': url,
                'product_name': product_name,
                'price': price,
                'brand': brand,
                'sku': sku,
                'status': 'Success',
                'error_reason': '',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'specifications': specifications
        }
    
    def _parse_generic(self, material_id, source, url, soup):
        """Generic parser for unknown sites"""
        product_name = None
        for selector in ['h1', '.product-name', '.title', '[itemprop="name"]']:
            elem = soup.select_one(selector)
            if elem:
                product_name = elem.get_text().strip()
                break
        
        if not product_name:
            return self._create_error_result(material_id, source, url, f"Scraper not implemented for {source}")
        
        return {
            'main': {
                'materialId': material_id,
                'source': source,
                'product_url': url,
                'product_name': product_name,
                'price': 'N/A',
                'brand': 'N/A',
                'sku': 'N/A',
                'status': 'Partial',
                'error_reason': 'Generic parser used',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'specifications': []
        }
    
    def _clean_price(self, price_text):
        """Extract numeric price"""
        if not price_text:
            return 'N/A'
        # Remove extra spaces and newlines
        price_text = ' '.join(price_text.split())
        # Extract price with currency
        match = re.search(r'₹\s*[\d,]+\.?\d*|Rs\.?\s*[\d,]+\.?\d*', price_text)
        if match:
            return match.group().replace('Rs', '₹').replace(' ', '')
        # Try just numbers
        match = re.search(r'[\d,]+\.?\d*', price_text)
        if match:
            return f"₹{match.group()}"
        return 'N/A'
    
    def _create_error_result(self, material_id, source, url, error_reason):
        """Create error result"""
        return {
            'main': {
                'materialId': material_id,
                'source': source,
                'product_url': url,
                'product_name': 'N/A',
                'price': 'N/A',
                'brand': 'N/A',
                'sku': 'N/A',
                'status': 'Failed',
                'error_reason': error_reason,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'specifications': []
        }

# ============================================================================
# SESSION STATE
# ============================================================================

if 'total_scraped' not in st.session_state:
    st.session_state.total_scraped = 0

# ============================================================================
# UI
# ============================================================================

st.markdown('<h1 class="main-header">⚡ SKU HARVESTER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Hybrid Data Extraction Platform</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ System")
    
    st.markdown("#### 🌐 Scraping Method")
    st.markdown("**Requests (Fast):**")
    st.markdown("✅ Indiamart")
    st.markdown("✅ Industry Buying")
    
    st.markdown("**Selenium (Full):**")
    if SELENIUM_AVAILABLE:
        st.markdown("✅ Amazon")
        st.markdown("✅ Flipkart")
    else:
        st.markdown("⚠️ Amazon (Limited)")
        st.markdown("⚠️ Flipkart (Limited)")
    
    st.markdown("---")
    st.metric("Total Processed", st.session_state.total_scraped)

# Main
st.markdown("### 📁 Bulk Upload Scraping")

st.markdown("""
<div class="info-box">
    <b>📋 File Format:</b> materialId | Source | Product URL
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Excel/CSV", type=['csv', 'xlsx', 'xls'])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        required_cols = ['materialId', 'Source', 'Product URL']
        missing = [c for c in required_cols if c not in df.columns]
        
        if missing:
            st.error(f"❌ Missing: {', '.join(missing)}")
        else:
            st.success("✅ File validated!")
            st.dataframe(df.head(10))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", len(df))
            with col2:
                simple = len(df[df['Source'].str.lower().str.contains('indiamart|industry', na=False)])
                st.metric("Fast Mode", simple)
            with col3:
                complex_sites = len(df[df['Source'].str.lower().str.contains('amazon|flipkart', na=False)])
                st.metric("Full Mode", complex_sites)
            
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                scrape_btn = st.button("🚀 START SCRAPING", type="primary")
            
            if scrape_btn:
                st.markdown("---")
                st.markdown("### 🔄 Scraping...")
                
                scraper = HybridScraper()
                main_results = []
                all_specs = []
                
                progress = st.progress(0)
                status = st.empty()
                current = st.empty()
                
                for idx, row in df.iterrows():
                    material_id = row['materialId']
                    source = row['Source']
                    url = row['Product URL']
                    
                    current.info(f"📦 {material_id} - {source}")
                    status.text(f"{idx + 1}/{len(df)}")
                    
                    result = scraper.scrape_product(material_id, source, url)
                    main_results.append(result['main'])
                    all_specs.extend(result['specifications'])
                    
                    progress.progress((idx + 1) / len(df))
                    
                    if idx < len(df) - 1:
                        time.sleep(1.5)
                
                scraper.close_selenium()
                
                current.empty()
                status.text("✅ Complete!")
                
                st.session_state.total_scraped += len(df)
                
                # Results
                st.markdown("---")
                st.markdown("### 📊 Summary")
                
                success_count = len([r for r in main_results if r['status'] == 'Success'])
                success_rate = (success_count / len(main_results) * 100) if main_results else 0
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total", len(main_results))
                with col2:
                    st.metric("✅ Success", success_count)
                with col3:
                    st.metric("❌ Failed", len(main_results) - success_count)
                with col4:
                    st.metric("Rate", f"{success_rate:.1f}%")
                
                st.markdown("---")
                st.markdown("### 📋 Results")
                
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
                            f"specifications_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            "text/csv",
                            use_container_width=True
                        )
                        
                        st.info(f"📊 {len(all_specs)} specification rows extracted")
                    else:
                        st.info("No specifications found")
                
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 2rem;'>
    <p><b>⚡ SKU Harvester v2.0</b> | Hybrid Extraction Platform</p>
    <p style='font-size: 0.9rem;'>Requests: Indiamart, Industry Buying | Selenium: Amazon, Flipkart</p>
</div>
""", unsafe_allow_html=True)
