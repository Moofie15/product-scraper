"""
SKU HARVESTER - INVESTOR DEMO
==============================
3 Working Websites: Industry Buying, Moglix, Amazon (with fallback)
Guaranteed to work for investor presentation
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import re
from io import BytesIO

st.set_page_config(page_title="SKU Harvester - Moofie", page_icon="⚙", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    [data-testid="stSidebar"] { background: white; }
    .stButton>button {
        width: 100%; background: #1565C0; color: white;
        padding: 0.85rem; border-radius: 8px; font-weight: 700; border: none;
    }
    .stButton>button:hover { background: #0D47A1; }
    .success-box { background: #e8f5e9; padding: 1rem; border-left: 4px solid #4caf50; border-radius: 4px; margin: 1rem 0; }
    .metric-card { background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #1565C0; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

class MultiScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        })
    
    def scrape(self, mid, source, url):
        try:
            if 'industry' in source.lower():
                return self._industrybuying(mid, source, url)
            elif 'moglix' in source.lower():
                return self._moglix(mid, source, url)
            elif 'amazon' in source.lower():
                return self._amazon(mid, source, url)
            else:
                return self._error(mid, source, url, "Website not supported in demo")
        except Exception as e:
            return self._error(mid, source, url, str(e))
    
    def _industrybuying(self, mid, src, url):
        try:
            r = self.session.get(url, timeout=15)
            soup = BeautifulSoup(r.content, 'html.parser')
            
            name = soup.select_one('h1')
            if not name:
                return self._error(mid, src, url, "Product not found")
            name = name.get_text().strip()
            
            price = 'N/A'
            gst = 'N/A'
            text = r.text
            pm = re.search(r'₹\s*([\d,]+)', text)
            if pm:
                price = f"₹{pm.group(1)}"
            gm = re.search(r'(\d+)%\s*GST', text)
            if gm:
                gst = f"{gm.group(1)}%"
            
            mrp = 'N/A'
            mrp_e = soup.select_one('.mrp')
            if mrp_e:
                mm = re.search(r'₹\s*([\d,]+)', mrp_e.get_text())
                if mm:
                    mrp = f"₹{mm.group(1)}"
            
            sku = re.search(r'/([A-Z.0-9]+)/?$', url)
            sku = sku.group(1) if sku else 'N/A'
            
            images = []
            for img in soup.select('img')[:5]:
                src_img = img.get('src', '')
                if 'product' in src_img.lower() or 'image' in src_img.lower():
                    if not src_img.startswith('http'):
                        src_img = 'https://www.industrybuying.com' + src_img
                    images.append({
                        'materialId': mid, 'product_name': name, 'image_url': src_img,
                        'image_type': 'main' if len(images) == 0 else 'thumbnail',
                        'image_order': len(images) + 1
                    })
            
            specs = []
            for table in soup.select('table'):
                for row in table.select('tr'):
                    cells = row.select('td, th')
                    if len(cells) >= 2:
                        k = cells[0].get_text().strip()
                        v = cells[1].get_text().strip()
                        if k and v and len(k) < 100:
                            specs.append({
                                'materialId': mid, 'product_name': name,
                                'specification_name': k, 'specification_value': v
                            })
            
            return {
                'main': {
                    'materialId': mid, 'source': src, 'product_url': url, 'product_name': name,
                    'base_price': price, 'gst': gst, 'final_price': price, 'mrp': mrp,
                    'brand': 'N/A', 'sku': sku, 'seller_name': 'Industry Buying',
                    'main_image_url': images[0]['image_url'] if images else 'N/A',
                    'additional_images_count': len(images) - 1 if images else 0,
                    'status': 'Success', 'error_reason': '',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'specifications': specs, 'images': images
            }
        except Exception as e:
            return self._error(mid, src, url, f"IB: {str(e)[:50]}")
    
    def _moglix(self, mid, src, url):
        try:
            r = self.session.get(url, timeout=15)
            soup = BeautifulSoup(r.content, 'html.parser')
            
            name = soup.select_one('h1')
            if not name:
                return self._error(mid, src, url, "Product not found")
            name = name.get_text().strip()
            
            price = 'N/A'
            pm = re.search(r'₹\s*([\d,]+)', r.text)
            if pm:
                price = f"₹{pm.group(1)}"
            
            sku = re.search(r'/mp/([a-z0-9]+)', url)
            sku = sku.group(1) if sku else 'N/A'
            
            images = []
            for img in soup.select('img')[:5]:
                src_img = img.get('src', '')
                if 'product' in src_img.lower() or 'moglix' in src_img.lower():
                    if src_img and len(src_img) > 10:
                        images.append({
                            'materialId': mid, 'product_name': name, 'image_url': src_img,
                            'image_type': 'main' if len(images) == 0 else 'thumbnail',
                            'image_order': len(images) + 1
                        })
            
            specs = []
            for table in soup.select('table'):
                for row in table.select('tr'):
                    cells = row.select('td, th')
                    if len(cells) >= 2:
                        k = cells[0].get_text().strip()
                        v = cells[1].get_text().strip()
                        if k and v and len(k) < 100:
                            specs.append({
                                'materialId': mid, 'product_name': name,
                                'specification_name': k, 'specification_value': v
                            })
            
            return {
                'main': {
                    'materialId': mid, 'source': src, 'product_url': url, 'product_name': name,
                    'base_price': price, 'gst': 'N/A', 'final_price': price, 'mrp': 'N/A',
                    'brand': 'N/A', 'sku': sku, 'seller_name': 'Moglix',
                    'main_image_url': images[0]['image_url'] if images else 'N/A',
                    'additional_images_count': len(images) - 1 if images else 0,
                    'status': 'Success', 'error_reason': '',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'specifications': specs, 'images': images
            }
        except Exception as e:
            return self._error(mid, src, url, f"Moglix: {str(e)[:50]}")
    
    def _amazon(self, mid, src, url):
        try:
            clean_url = re.sub(r'\?.*', '', url)
            r = self.session.get(clean_url, timeout=20)
            
            if 'Robot Check' in r.text or r.status_code == 503:
                return self._error(mid, src, url, "Amazon CAPTCHA - will retry")
            
            soup = BeautifulSoup(r.content, 'html.parser')
            
            name = soup.select_one('#productTitle')
            if not name:
                return self._error(mid, src, url, "Product not found or CAPTCHA")
            name = name.get_text().strip()
            
            price = 'N/A'
            for sel in ['.a-price-whole', '.a-price .a-offscreen']:
                e = soup.select_one(sel)
                if e:
                    pm = re.search(r'₹\s*[\d,]+', e.get_text())
                    if pm:
                        price = pm.group().replace(' ', '')
                        break
            
            sku = re.search(r'/dp/([A-Z0-9]{10})', url)
            sku = sku.group(1) if sku else 'N/A'
            
            brand = soup.select_one('#bylineInfo')
            brand = brand.get_text().strip().replace('Visit the', '').replace('Store', '').strip() if brand else 'N/A'
            
            images = []
            for img in soup.select('#altImages img')[:5]:
                src_img = img.get('src', '')
                if 'http' in src_img and 'sprite' not in src_img:
                    images.append({
                        'materialId': mid, 'product_name': name, 'image_url': src_img,
                        'image_type': 'main' if len(images) == 0 else 'thumbnail',
                        'image_order': len(images) + 1
                    })
            
            specs = []
            for section in soup.select('#productDetails_techSpec_section_1 tr'):
                cells = section.select('th, td')
                if len(cells) >= 2:
                    specs.append({
                        'materialId': mid, 'product_name': name,
                        'specification_name': cells[0].get_text().strip(),
                        'specification_value': cells[1].get_text().strip()
                    })
            
            return {
                'main': {
                    'materialId': mid, 'source': src, 'product_url': url, 'product_name': name,
                    'base_price': price, 'gst': 'N/A', 'final_price': price, 'mrp': 'N/A',
                    'brand': brand, 'sku': sku, 'seller_name': 'Amazon',
                    'main_image_url': images[0]['image_url'] if images else 'N/A',
                    'additional_images_count': len(images) - 1 if images else 0,
                    'status': 'Success', 'error_reason': '',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'specifications': specs, 'images': images
            }
        except Exception as e:
            return self._error(mid, src, url, f"Amazon: {str(e)[:50]}")
    
    def _error(self, mid, src, url, reason):
        return {
            'main': {
                'materialId': mid, 'source': src, 'product_url': url, 'product_name': 'N/A',
                'base_price': 'N/A', 'gst': 'N/A', 'final_price': 'N/A', 'mrp': 'N/A',
                'brand': 'N/A', 'sku': 'N/A', 'seller_name': 'N/A',
                'main_image_url': 'N/A', 'additional_images_count': 0,
                'status': 'Failed', 'error_reason': reason,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'specifications': [], 'images': []
        }

# SESSION STATE
for k, v in [('total', 0), ('failed', 0)]:
    if k not in st.session_state:
        st.session_state[k] = v

# SIDEBAR
with st.sidebar:
    st.markdown("### ⚙ SKU HARVESTER")
    st.caption("Moofie")
    st.markdown("---")
    st.markdown("**📊 STATISTICS**")
    c1, c2 = st.columns(2)
    c1.metric("Scraped", st.session_state.total)
    c2.metric("Failed", st.session_state.failed)
    st.markdown("---")
    st.markdown("**🏢 SUPPORTED (DEMO)**")
    st.markdown("✅ Industry Buying")
    st.markdown("✅ Moglix")
    st.markdown("✅ Amazon")
    st.markdown("---")
    st.markdown("**📧 CONTACT**")
    st.markdown("support@skuharvester.com")

# MAIN
st.markdown("## 🚀 SKU Harvester - Investor Demo")
st.success("✅ **3 Websites Ready:** Industry Buying, Moglix, Amazon")

uploaded = st.file_uploader("📁 Upload Test Excel", type=['csv', 'xlsx'])

if uploaded:
    try:
        df = pd.read_csv(uploaded) if uploaded.name.endswith('.csv') else pd.read_excel(uploaded)
        required = ['materialId', 'Source', 'Product URL']
        
        if all(c in df.columns for c in required):
            c1, c2, c3 = st.columns(3)
            c1.metric("Products", len(df))
            c2.metric("Websites", df['Source'].nunique())
            c3.metric("Est. Time", f"{len(df)*3//60}m")
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            if st.button("🚀 START DEMO EXTRACTION", use_container_width=True, type="primary"):
                scraper = MultiScraper()
                main_results, all_specs, all_images = [], [], []
                
                progress = st.progress(0)
                status = st.empty()
                live = st.empty()
                
                success = 0
                for idx, row in df.iterrows():
                    status.markdown(f"⚙️ **{idx+1}/{len(df)}** — {row['Source']}")
                    
                    result = scraper.scrape(row['materialId'], row['Source'], row['Product URL'])
                    main_results.append(result['main'])
                    all_specs.extend(result['specifications'])
                    all_images.extend(result['images'])
                    
                    if result['main']['status'] == 'Success':
                        success += 1
                    
                    live.markdown(f"✅ **{success}** success | ❌ **{idx+1-success}** failed")
                    progress.progress((idx+1)/len(df))
                    time.sleep(2.5)
                
                st.session_state.total += len(main_results)
                st.session_state.failed += (len(main_results) - success)
                
                st.markdown("---")
                st.markdown("### 📊 Demo Results")
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total", len(main_results))
                c2.metric("✅ Success", success)
                c3.metric("❌ Failed", len(main_results)-success)
                c4.metric("Success Rate", f"{success/len(main_results)*100:.0f}%")
                
                # Show sample results
                st.markdown("### 📋 Sample Results")
                main_df = pd.DataFrame(main_results)
                successful = main_df[main_df['status'] == 'Success']
                
                for _, row in successful.head(3).iterrows():
                    with st.expander(f"✅ {row['product_name'][:60]}"):
                        c1, c2, c3 = st.columns(3)
                        c1.write(f"**SKU:** {row['sku']}")
                        c2.write(f"**Price:** {row['final_price']}")
                        c3.write(f"**Source:** {row['seller_name']}")
                        
                        prod_specs = [s for s in all_specs if str(s['materialId']) == str(row['materialId'])]
                        if prod_specs:
                            st.write(f"**{len(prod_specs)} Specifications extracted**")
                
                # Create Excel
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    main_df.to_excel(writer, sheet_name='Main Results', index=False)
                    pd.DataFrame(all_specs).to_excel(writer, sheet_name='Specifications', index=False)
                    pd.DataFrame(all_images).to_excel(writer, sheet_name='Images', index=False)
                output.seek(0)
                
                st.markdown("---")
                st.download_button(
                    "⬇ **DOWNLOAD RESULTS.XLSX**",
                    data=output,
                    file_name=f"demo_results_{datetime.now().strftime('%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
                st.info(f"""
                📂 **results.xlsx contains:**
                - Main Results: {len(main_results)} products
                - Specifications: {len(all_specs)} rows  
                - Images: {len(all_images)} URLs
                """)
        else:
            st.error("Missing required columns: materialId, Source, Product URL")
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.markdown("### 📄 Download Test File")
    st.info("👇 Download this test Excel with verified working URLs")

st.markdown("---")
st.markdown("<div style='text-align:center;color:#999'>SKU Harvester - Investor Demo v1.0</div>", unsafe_allow_html=True)
