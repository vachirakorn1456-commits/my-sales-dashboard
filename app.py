import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ฟังก์ชันดึงข้อมูลอัตโนมัติจาก Google Sheets
@st.cache_data(ttl=60)
def load_data():
  # สร้างฟังก์ชันดึงลิงก์จริงของคุณออกมาโดยตรง ไม่ผ่านเครื่องหมายคำพูดปกติ
    codes = [104,116,116,112,115,58,47,47,100,111,99,115,46,103,111,111,103,108,101,46,99,111,109,47,115,112,114,101,97,100,115,104,101,101,116,115,47,100,47,49,78,80,75,101,118,67,67,112,78,81,65,114,107,106,114,76,55,119,113,73,71,103,50,51,115,118,95,48,87,66,108,114,118,50,70,50,110,113,67,81,114,115,47,101,120,112,111,114,116,63,102,111,114,109,97,116,61,99,115,118]
    csv_url = "".join([chr(x) for x in codes])
    # อ่านข้อมูลผ่าน pandas
    df = pd.read_csv(csv_url)
    
    # ลบช่องว่างที่อาจติดมากับชื่อหัวคอลัมน์ เช่น " ยอดขาย " ให้กลายเป็น "ยอดขาย"
    df.columns = df.columns.str.strip()
    
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
        df_product = df.groupby('สินค้า', as_index=False)['ยอดขาย'].sum()
        fig_bar = px.bar(df_product, x='สินค้า', y='ยอดขาย', 
                         text_auto='.2s', color='สินค้า',
                         labels={'ยอดขาย': 'ยอดขาย (บาท)', 'สินค้า': 'ประเภทสินค้า'})
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col2:
        st.subheader("📍 สัดส่วนยอดขายแยกตามเขตพื้นที่")
        df_region = df.groupby('เขตพื้นที่', as_index=False)['ยอดขาย'].sum()
        fig_pie = px.pie(df_region, values='ยอดขาย', names='เขตพื้นที่', 
                         hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    st.markdown("---")
    st.subheader("📋 ตารางข้อมูลยอดขายทั้งหมด")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการประมวลผลข้อมูล: {e}")
