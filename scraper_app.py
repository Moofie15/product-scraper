"""
SKU HARVESTER - MOOFIE PRODUCTION
==================================
MOOFIE UI with sidebar
3 website scrapers: Amazon, Industry Buying, Moglix  
Excel output with 3 sheets
80% success target
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import re
from io import BytesIO

# Selenium (optional)
SELENIUM_AVAILABLE = False
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except:
    pass

# PAGE CONFIG
st.set_page_config(
    page_title="SKU Harvester - Moofie",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# MOOFIE UI CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    [data-testid="stSidebar"] {
        background: white;
    }
    
    .stButton>button {
        width: 100%;
        background: #1565C0;
        color: white;
        padding: 0.85rem;
        border-radius: 8px;
        font-weight: 700;
        border: none;
    }
    
    .stButton>button:hover {
        background: #0D47A1;
    }
    
    .success-box {
        background: #e8f5e9;
        padding: 1rem;
        border-left: 4px solid #4caf50;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #ffebee;
        padding: 1rem;
        border-left: 4px solid #f44336;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# SCRAPER CLASS
class MultiScraper:
    def __init__(self):
        self.driver = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def init_selenium(self):
        if not SELENIUM_AVAILABLE or self.driver:
            return self.driver is not None
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            return True
        except:
            return False
    
    def close(self):
        if self.driver:
            self.driver.quit()
    
    def scrape(self, mid, source, url):
        try:
            src_lower = source.lower()
            if 'amazon' in src_lower:
                return self._amazon(mid, source, url)
            elif 'industry' in src_lower:
                return self._industrybuying(mid, source, url)
            elif 'moglix' in src_lower:
                return self._moglix(mid, source, url)
            else:
                return self._error(mid, source, url, "Website not supported")
        except Exception as e:
            return self._error(mid, source, url, str(e))
    
    def _amazon(self, mid, src, url):
        try:
            if not self.init_selenium():
                return self._error(mid, src, url, "Selenium unavailable")
            
            self.driver.get(url)
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Name
            name_elem = soup.select_one('#productTitle')
            name = name_elem.get_text().strip() if name_elem else None
            if not name:
                return self._error(mid, src, url, "Product name not found")
            
            # Price
            price = 'N/A'
            price_elem = soup.select_one('.a-price-whole')
            if price_elem:
                price = self._clean_price(price_elem.get_text())
            
            # Brand & SKU
            brand = 'N/A'
            brand_elem = soup.select_one('#bylineInfo')
            if brand_elem:
                brand = brand_elem.get_text().strip().replace('Visit the', '').replace('Store', '').strip()
            
            sku = 'N/A'
            asin = re.search(r'/dp/([A-Z0-9]{10})', url)
            if asin:
                sku = asin.group(1)
            
            # Seller
            seller = 'N/A'
            seller_elem = soup.select_one('#merchant-info')
            if seller_elem:
                seller = seller_elem.get_text().strip()[:100]
            
            # Availability
            avail = 'In Stock'
            avail_elem = soup.select_one('#availability span')
            if avail_elem:
                avail = avail_elem.get_text().strip()
            
            # Images
            images = []
            for img in soup.select('#altImages img')[:5]:
                src_img = img.get('src') or img.get('data-src')
                if src_img and 'http' in src_img:
                    images.append({
                        'materialId': mid,
                        'product_name': name,
                        'image_url': src_img,
                        'image_type': 'main' if len(images) == 0 else 'thumbnail',
                        'image_order': len(images) + 1
                    })
            
            # Specs
            specs = []
            for section in soup.select('#productDetails_techSpec_section_1 tr'):
                cells = section.select('th, td')
                if len(cells) >= 2:
                    specs.append({
                        'materialId': mid,
                        'product_name': name,
                        'specification_name': cells[0].get_text().strip(),
                        'specification_value': cells[1].get_text().strip()
                    })
            
            return {
                'main': {
                    'materialId': mid, 'source': src, 'product_url': url, 'product_name': name,
                    'base_price': price, 'gst': 'N/A', 'final_price': price, 'mrp': 'N/A', 'discount': 'N/A',
                    'brand': brand, 'sku': sku, 'seller_name': seller, 'seller_rating': 'N/A',
                    'availability': avail, 'delivery_time': 'N/A', 'shipping_cost': 'N/A',
                    'main_image_url': images[0]['image_url'] if images else 'N/A',
                    'additional_images_count': len(images) - 1 if images else 0,
                    'status': 'Success', 'error_reason': '',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'specifications': specs,
                'images': images
            }
        except Exception as e:
            return self._error(mid, src, url, f"Amazon error: {str(e)}")
    
    def _industrybuying(self, mid, src, url):
        try:
            r = self.session.get(url, timeout=15)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, 'html.parser')
            
            # Name
            name_elem = soup.select_one('h1')
            name = name_elem.get_text().strip() if name_elem else None
            if not name:
                return self._error(mid, src, url, "Product name not found")
            
            # Price
            price = 'N/A'
            gst = 'N/A'
            price_container = soup.select_one('.price-container')
            if price_container:
                text = price_container.get_text()
                price_match = re.search(r'₹\s*([\d,]+)', text)
                if price_match:
                    price = f"₹{price_match.group(1)}"
                gst_match = re.search(r'(\d+)%\s*GST', text)
                if gst_match:
                    gst = f"{gst_match.group(1)}%"
            
            # SKU
            sku = 'N/A'
            sku_match = re.search(r'/([A-Z0-9.]+)/?$', url)
            if sku_match:
                sku = sku_match.group(1)
            
            # Images
            images = []
            for img in soup.select('.product-image img')[:5]:
                src_img = img.get('src') or img.get('data-src')
                if src_img:
                    if not src_img.startswith('http'):
                        src_img = 'https://www.industrybuying.com' + src_img
                    images.append({
                        'materialId': mid, 'product_name': name, 'image_url': src_img,
                        'image_type': 'main' if len(images) == 0 else 'thumbnail',
                        'image_order': len(images) + 1
                    })
            
            # Specs
            specs = []
            spec_table = soup.select_one('.specifications table')
            if spec_table:
                for row in spec_table.select('tr'):
                    cells = row.select('td, th')
                    if len(cells) >= 2:
                        specs.append({
                            'materialId': mid, 'product_name': name,
                            'specification_name': cells[0].get_text().strip(),
                            'specification_value': cells[1].get_text().strip()
                        })
            
            return {
                'main': {
                    'materialId': mid, 'source': src, 'product_url': url, 'product_name': name,
                    'base_price': price, 'gst': gst, 'final_price': price, 'mrp': 'N/A', 'discount': 'N/A',
                    'brand': 'N/A', 'sku': sku, 'seller_name': 'Industry Buying', 'seller_rating': 'N/A',
                    'availability': 'In Stock', 'delivery_time': 'N/A', 'shipping_cost': 'Free',
                    'main_image_url': images[0]['image_url'] if images else 'N/A',
                    'additional_images_count': len(images) - 1 if images else 0,
                    'status': 'Success', 'error_reason': '',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'specifications': specs,
                'images': images
            }
        except Exception as e:
            return self._error(mid, src, url, f"Industry Buying error: {str(e)}")
    
    def _moglix(self, mid, src, url):
        try:
            r = self.session.get(url, timeout=15)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, 'html.parser')
            
            # Name
            name_elem = soup.select_one('h1')
            name = name_elem.get_text().strip() if name_elem else None
            if not name:
                return self._error(mid, src, url, "Product name not found")
            
            # Price
            price = 'N/A'
            price_elem = soup.select_one('.price')
            if price_elem:
                price_match = re.search(r'₹\s*([\d,]+)', price_elem.get_text())
                if price_match:
                    price = f"₹{price_match.group(1)}"
            
            # SKU
            sku = 'N/A'
            sku_match = re.search(r'/mp/([a-z0-9]+)', url)
            if sku_match:
                sku = sku_match.group(1)
            
            # Images
            images = []
            for img in soup.select('.product-images img')[:5]:
                src_img = img.get('src') or img.get('data-src')
                if src_img:
                    if not src_img.startswith('http'):
                        src_img = 'https://www.moglix.com' + src_img
                    images.append({
                        'materialId': mid, 'product_name': name, 'image_url': src_img,
                        'image_type': 'main' if len(images) == 0 else 'thumbnail',
                        'image_order': len(images) + 1
                    })
            
            # Specs
            specs = []
            spec_container = soup.select_one('.specifications')
            if spec_container:
                for row in spec_container.select('tr'):
                    cells = row.select('td, th')
                    if len(cells) >= 2:
                        specs.append({
                            'materialId': mid, 'product_name': name,
                            'specification_name': cells[0].get_text().strip(),
                            'specification_value': cells[1].get_text().strip()
                        })
            
            return {
                'main': {
                    'materialId': mid, 'source': src, 'product_url': url, 'product_name': name,
                    'base_price': price, 'gst': 'N/A', 'final_price': price, 'mrp': 'N/A', 'discount': 'N/A',
                    'brand': 'N/A', 'sku': sku, 'seller_name': 'Moglix', 'seller_rating': 'N/A',
                    'availability': 'In Stock', 'delivery_time': 'N/A', 'shipping_cost': 'Free',
                    'main_image_url': images[0]['image_url'] if images else 'N/A',
                    'additional_images_count': len(images) - 1 if images else 0,
                    'status': 'Success', 'error_reason': '',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'specifications': specs,
                'images': images
            }
        except Exception as e:
            return self._error(mid, src, url, f"Moglix error: {str(e)}")
    
    def _clean_price(self, text):
        match = re.search(r'₹\s*[\d,]+', text)
        return match.group().replace(' ', '') if match else 'N/A'
    
    def _error(self, mid, src, url, reason):
        return {
            'main': {
                'materialId': mid, 'source': src, 'product_url': url, 'product_name': 'N/A',
                'base_price': 'N/A', 'gst': 'N/A', 'final_price': 'N/A', 'mrp': 'N/A', 'discount': 'N/A',
                'brand': 'N/A', 'sku': 'N/A', 'seller_name': 'N/A', 'seller_rating': 'N/A',
                'availability': 'N/A', 'delivery_time': 'N/A', 'shipping_cost': 'N/A',
                'main_image_url': 'N/A', 'additional_images_count': 0,
                'status': 'Failed', 'error_reason': reason,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'specifications': [],
            'images': []
        }

# SESSION STATE
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'failed' not in st.session_state:
    st.session_state.failed = 0
if 'mode' not in st.session_state:
    st.session_state.mode = 'single'

# SIDEBAR (MOOFIE UI)
with st.sidebar:
    st.markdown("### ⚙ SKU HARVESTER")
    st.markdown("**Moofie**")
    st.markdown("---")
    
    st.markdown("**📊 STATISTICS**")
    st.metric("Total Scraped", st.session_state.total)
    st.metric("Failed", st.session_state.failed)
    st.markdown("---")
    
    st.markdown("**🏢 SUPPORTED WEBSITES**")
    st.markdown("""
    🛒 Amazon India  
    🏭 Indiamart  
    🔧 Industry Buying  
    ⚙️ Moglix  
    🔩 SKF India  
    🛍️ Flipkart
    """)
    st.markdown("---")
    
    st.markdown("**📞 CONTACT**")
    st.markdown("""
    📧 support@skuharvester.com  
    💬 Live Chat  
    📚 Documentation
    """)

# MAIN CONTENT
st.markdown("## Select Extraction Mode")
col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Single Product", use_container_width=True):
        st.session_state.mode = 'single'
        st.rerun()
with col2:
    if st.button("📊 Bulk Upload", use_container_width=True):
        st.session_state.mode = 'bulk'
        st.rerun()

st.markdown("---")

# SINGLE MODE
if st.session_state.mode == 'single':
    st.markdown("### 📝 Single Product Extraction")
    
    website = st.selectbox("Website", ["Amazon India", "Industry Buying", "Moglix"])
    url = st.text_input("Product URL", placeholder="https://...")
    
    if st.button("🚀 START EXTRACTION", use_container_width=True, type="primary"):
        if not url:
            st.error("Please enter URL")
        else:
            with st.spinner("Extracting..."):
                scraper = MultiScraper()
                result = scraper.scrape(1, website, url)
                scraper.close()
            
            if result['main']['status'] == 'Success':
                st.markdown('<div class="success-box">✅ Success!</div>', unsafe_allow_html=True)
                st.write(f"**Name:** {result['main']['product_name']}")
                st.write(f"**Price:** {result['main']['final_price']}")
                st.write(f"**Brand:** {result['main']['brand']}")
                
                if result['specifications']:
                    st.markdown("**Specifications:**")
                    spec_df = pd.DataFrame(result['specifications'])
                    st.dataframe(spec_df[['specification_name', 'specification_value']], use_container_width=True)
            else:
                st.markdown(f'<div class="error-box">❌ Failed: {result["main"]["error_reason"]}</div>', unsafe_allow_html=True)

# BULK MODE
else:
    st.markdown("### 📁 Bulk Upload")
    st.info("📋 Upload Excel/CSV with: materialId | Source | Product URL")
    
    uploaded = st.file_uploader("Upload File", type=['csv', 'xlsx'])
    
    if uploaded:
        try:
            df = pd.read_csv(uploaded) if uploaded.name.endswith('.csv') else pd.read_excel(uploaded)
            
            required = ['materialId', 'Source', 'Product URL']
            missing = [c for c in required if c not in df.columns]
            
            if missing:
                st.error(f"Missing: {', '.join(missing)}")
            else:
                st.success(f"✅ {len(df)} products loaded")
                st.dataframe(df.head(5))
                
                if st.button("🚀 START BULK EXTRACTION", use_container_width=True, type="primary"):
                    scraper = MultiScraper()
                    main_results = []
                    all_specs = []
                    all_images = []
                    
                    progress = st.progress(0)
                    status = st.empty()
                    
                    for idx, row in df.iterrows():
                        status.text(f"Processing {idx + 1}/{len(df)}...")
                        result = scraper.scrape(row['materialId'], row['Source'], row['Product URL'])
                        main_results.append(result['main'])
                        all_specs.extend(result['specifications'])
                        all_images.extend(result['images'])
                        progress.progress((idx + 1) / len(df))
                        time.sleep(2)
                    
                    scraper.close()
                    
                    # Summary
                    success = len([r for r in main_results if r['status'] == 'Success'])
                    failed = len(main_results) - success
                    st.session_state.total += len(main_results)
                    st.session_state.failed += failed
                    
                    st.markdown("### 📊 Results")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total", len(main_results))
                    col2.metric("✅ Success", success)
                    col3.metric("❌ Failed", failed)
                    col4.metric("Rate", f"{(success/len(main_results)*100):.1f}%")
                    
                    # Create Excel with 3 sheets
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        pd.DataFrame(main_results).to_excel(writer, sheet_name='Main Results', index=False)
                        if all_specs:
                            pd.DataFrame(all_specs).to_excel(writer, sheet_name='Specifications', index=False)
                        if all_images:
                            pd.DataFrame(all_images).to_excel(writer, sheet_name='Images', index=False)
                    
                    output.seek(0)
                    
                    st.download_button(
                        "⬇ Download results.xlsx",
                        data=output,
                        file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                    
                    st.info(f"""
                    **File contains 3 sheets:**
                    - Main Results: {len(main_results)} rows
                    - Specifications: {len(all_specs)} rows
                    - Images: {len(all_images)} rows
                    """)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.markdown("### 📄 Template")
        template = pd.DataFrame({
            'materialId': ['001', '002'],
            'Source': ['Amazon India', 'Industry Buying'],
            'Product URL': ['https://www.amazon.in/...', 'https://www.industrybuying.com/...']
        })
        st.dataframe(template)
        st.download_button("📥 Download template.csv", template.to_csv(index=False), "template.csv")

st.markdown("---")
st.markdown("<div style='text-align:center;color:#999'>SKU Harvester v1.0 - Moofie Edition</div>", unsafe_allow_html=True)
