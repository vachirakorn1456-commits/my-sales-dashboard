import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ดึงข้อมูลจากไฟล์ Excel โดยระบุเอนจินเพื่อความชัวร์
@st.cache_data
def load_data():
    # ⚠️ สำคัญ: ต้องเปลี่ยนลิงก์ด้านล่างนี้ให้เป็น URL ดาวน์โหลดตรงของไฟล์ Excel จริงบน SharePoint
    url = "https://sharepoint.com" 
    
    # ดึงข้อมูลตรงๆ ด้วย pandas โดยใช้ engine openpyxl
    df = pd.read_excel(url, engine='openpyxl')
    
    # ลบช่องว่างที่หัวตาราง (ใส่เครื่องหมาย # ปิดไว้ก่อนเพื่อป้องกัน Error หากหัวตารางไม่ใช่ตัวหนังสือ)
    # df.columns = df.columns.str.strip()
    
    return df

# ส่วนของการแสดงผลบนหน้าเว็บ
try:
    # เรียกใช้ฟังก์ชันดึงข้อมูล
    df = load_data()
    
    # แสดงหัวข้อแดชบอร์ด
    st.title("📊 ยอดขายแดชบอร์ด (Sales Dashboard)")
    st.markdown("---")
    
    # แสดงตารางข้อมูลบนหน้าเว็บ
    st.dataframe(df, use_container_width=True)

except Exception as e:
    # แสดงข้อความแจ้งเตือนสีแดงหากเกิดข้อผิดพลาดในการดึงหรืออ่านข้อมูล
    st.error(f"เกิดข้อผิดพลาดในการประมวลผลข้อมูล: {e}")
