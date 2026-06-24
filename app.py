import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ฟังก์ชันดึงข้อมูลจากลิงก์ SharePoint 
@st.cache_data
def load_data():
    # นี่คือลิงก์ของคุณที่ผมแปลงเป็นตัวดาวน์โหลดตรงให้แล้วครับ
    url = "https://sharepoint.com" 
    
    # ดึงข้อมูลเข้า pandas ด้วยเอนจิน openpyxl
    df = pd.read_excel(url, engine='openpyxl')
    return df

# ส่วนของการแสดงผลบนหน้าเว็บแดชบอร์ด
try:
    df = load_data()
    
    st.title("📊 ยอดขายแดชบอร์ด (Sales Dashboard)")
    st.markdown("---")
    
    # แสดงตารางข้อมูลเต็มความกว้างหน้าจอ
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการประมวลผลข้อมูล: {e}")
