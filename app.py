import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ดึงข้อมูลจากไฟล์ Excel โดยผ่าน Request
@st.cache_data
def load_data():
    # ลิงก์ดาวน์โหลดตรงที่แปลงแล้ว
    url = "https://sharepoint.com"
    
    # ดึงข้อมูลผ่าน requests เพื่อจัดการไฟล์ไบนารี
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    # อ่านข้อมูลเข้าสู่ pandas dataframe โดยระบุเอนจิน openpyxl
    df = pd.read_excel(io.BytesIO(response.content), engine='openpyxl')
    df.columns = df.columns.str.strip() # ล้างช่องว่างหัวตาราง
    return df

try:
    df = load_data()
    st.title("📊 ยอดขายแดชบอร์ด (Sales Dashboard)")
    st.markdown("---")
    
    # แสดงตารางข้อมูลตรวจสอบความถูกต้อง
    st.write(df)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการประมวลผลข้อมูล: {e}")
