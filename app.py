import pandas as pd
import streamlit as stream  # อย่าลืม import สองตัวนี้ด้านบนสุดของไฟล์ด้วยนะครับ

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ดึงข้อมูลจากไฟล์ Excel โดยระบุเอนจินเพื่อความชัวร์
@st.cache_data
def load_data():
    # เปลี่ยน url ด้านล่างนี้ให้เป็นลิงก์ดาวน์โหลดตรงของไฟล์ Excel จริงๆ บน SharePoint
    url = "https://your-sharepoint-link-here...&download=1" 
    
    # ดึงข้อมูลตรงๆ ด้วย pandas โดยใช้ engine openpyxl
    df = pd.read_excel(url, engine='openpyxl')
    
    # ลบช่องว่างเฉพาะกรณีที่หัวตารางทุกอันเป็นตัวหนังสือ (String) เท่านั้น
    # df.columns = df.columns.str.strip() 
    
    return df

# ส่วนของการแสดงผล
try:
    df = load_data()
    
    st.title("📊 ยอดขายแดชบอร์ด (Sales Dashboard)")
    st.markdown("---")
    
    # ใช้ st.dataframe แทน st.write เพื่อการจัดรูปแบบตารางที่สวยงามกว่า
    st.dataframe(df)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการประมวลผลข้อมูล: {e}")
