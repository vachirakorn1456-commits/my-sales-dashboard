import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ฟังก์ชันดึงข้อมูลอัตโนมัติจาก Google Sheets
@st.cache_data(ttl=60)
def load_data():
    sheet_url = "https://google.com"
    csv_url = sheet_url.replace("/edit?gid=0#gid=0", "/export?format=csv")
    df = pd.read_csv(csv_url)
    
    # แปลงคอลัมน์ยอดขายให้เป็นตัวเลข เผื่อมีช่องว่างหรือพิมพ์ผิด
    df['ยอดขาย'] = pd.to_numeric(df['ยอดขาย'], errors='coerce').fillna(0)
    return df

# ส่วนของการแสดงผลบนหน้าแดชบอร์ด
try:
    df = load_data()
    
    st.title("📊 ยอดขายแดชบอร์ด (Sales Dashboard)")
    st.markdown("---")
    
    # สรุปตัวเลขสำคัญด้านบน (KPIs)
    total_sales = df['ยอดขาย'].sum()
    st.metric(label="💰 ยอดขายรวมทั้งหมด", value=f"{total_sales:,.2f} บาท")
    st.markdown("---")
    
    # แบ่งหน้าจอเป็น 2 คอลัมน์ซ้าย-ขวาเพื่อวางกราฟ
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛒 ยอดขายแยกตามประเภทสินค้า")
        # รวมยอดขายตามสินค้า
        df_product = df.groupby('สินค้า', as_index=False)['ยอดขาย'].sum()
        # สร้างกราฟแท่ง
        fig_bar = px.bar(df_product, x='สินค้า', y='ยอดขาย', 
                         text_auto='.2s', color='สินค้า',
                         labels={'ยอดขาย': 'ยอดขาย (บาท)', 'สินค้า': 'ประเภทสินค้า'})
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col2:
        st.subheader("📍 สัดส่วนยอดขายแยกตามเขตพื้นที่")
        # รวมยอดขายตามเขตพื้นที่
        df_region = df.groupby('เขตพื้นที่', as_index=False)['ยอดขาย'].sum()
        # สร้างกราฟวงกลม
        fig_pie = px.pie(df_region, values='ยอดขาย', names='เขตพื้นที่', 
                         hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    st.markdown("---")
    st.subheader("📋 ตารางข้อมูลยอดขายทั้งหมด")
    # แสดงตารางข้อมูลด้านล่างสุด
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการประมวลผลข้อมูล: {e}")
