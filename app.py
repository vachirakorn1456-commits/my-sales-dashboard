import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ดึงข้อมูลจากไฟล์ Excel โดยระบุเอนจินเพื่อความชัวร์
@st.cache_data
def load_data():
    # เปลี่ยนตัวซัฟฟิกซ์ท้ายลิงก์เพื่อบังคับดาวน์โหลดผ่าน SharePoint Web API
    url = "https://sharepoint.com"
    
    # ดึงข้อมูลตรงๆ ด้วย pandas โดยใช้ engine openpyxl
    df = pd.read_excel(url, engine='openpyxl')
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
    st.title("📊 ยอดขายแดชบอร์ด (Sales Dashboard)")
    st.markdown("---")
    st.write(df)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการประมวลผลข้อมูล: {e}")
