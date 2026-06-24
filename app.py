import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ฟังก์ชันดึงข้อมูลอัตโนมัติจาก Google Sheets
@st.cache_data(ttl=60)  # ดึงข้อมูลใหม่ทุกๆ 1 นาทีอัตโนมัติเมื่อมีการเปิดดูหน้าเว็บ
def load_data():
    # ลิงก์จาก Google Sheets ของคุณที่เปิดสิทธิ์เรียบร้อยแล้ว
    sheet_url = "https://google.com"
    
    # แปลงลิงก์แชร์ให้เป็นลิงก์ดึงข้อมูลดิบ (CSV) ที่ถูกต้อง
    csv_url = sheet_url.replace("/edit?gid=0#gid=0", "/export?format=csv")
    
    # ดึงข้อมูลเข้าสู่ระบบ
    df = pd.read_csv(csv_url)
    return df

# ส่วนของการแสดงผลบนหน้าแดชบอร์ด
try:
    df = load_data()
    
    st.title("📊 ยอดขายแดชบอร์ด (Sales Dashboard)")
    st.markdown("---")
    
    # แสดงตารางข้อมูลเต็มความกว้างหน้าจอ
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการประมวลผลข้อมูล: {e}")
