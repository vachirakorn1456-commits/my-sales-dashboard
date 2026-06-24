import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ดึงข้อมูลจากไฟล์ Excel โดยตรงจาก OneDrive/SharePoint
@st.cache_data
def load_data():
    url = "https://sharepoint.com"
    df = pd.read_excel(url)
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
