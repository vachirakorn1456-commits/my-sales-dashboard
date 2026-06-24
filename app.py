import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# # 1. ตั้งค่าหน้าเว็บให้เป็นแบบเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# # 2. ฟังก์ชันดึงข้อมูลอัตโนมัติจาก Google Sheets
@st.cache_data(ttl=5) # ดึงข้อมูลใหม่ทุกๆ 5 วินาทีเมื่อรีเฟรชหน้าจอ
def load_data():
    # ลิงก์ดึงข้อมูลผ่านรหัสความปลอดภัยพิเศษ
    b = b'aHR0cHM6Ly9kb2NzLmdvb2dsZS5jb20vc3ByZWFkc2hlZXRzL2QvMU5QS2V2Q0NwTlFBcmtqckw3d3FJR2cyM3M1dl8wV0JMcnYyRjJuYVFDenJzL2d2aXovdHE/dHF4PW91dDpjc3Y='
    csv_url = base64.b64decode(b).decode('utf-8')
    
    # อ่านข้อมูลโดยบังคับให้แถวแรกเป็นชื่อคอลัมน์ (Header)
    df = pd.read_csv(csv_url, header=0)
    
    # ลบช่องว่างที่ชื่อคอลัมน์ทั้งหมดป้องกัน Error เช่น " ยอดขาย " -> "ยอดขาย"
    df.columns = df.columns.str.strip()
    
    # แปลงคอลัมน์ยอดขายให้เป็นตัวเลข
    df['ยอดขาย'] = pd.to_numeric(df['ยอดขาย'], errors='coerce').fillna(0)
    return df

# เรียกใช้งานฟังก์ชันโหลดข้อมูล
df = load_data()

# # 3. ส่วนแสดงผลบนหน้าแดชบอร์ด (Dashboard Layout)
st.title("📊 Sales Dashboard - รายงานยอดขาย")
st.markdown("---")

# แสดงตารางข้อมูลดิบ
st.subheader("📋 ตารางข้อมูลยอดขายล่าสุด")
st.dataframe(df, use_container_width=True)

# สร้างกราฟแสดงผลยอดขายแยกตามพื้นที่ (ตัวอย่าง)
if 'เขตพื้นที่' in df.columns and 'ยอดขาย' in df.columns:
    st.subheader("📈 กราฟสรุปยอดขายแยกตามเขตพื้นที่")
    fig = px.bar(df, x='เขตพื้นที่', y='ยอดขาย', color='สินค้า', barmode='group', title="ยอดขายรวมแยกตามพื้นที่")
    st.plotly_chart(fig, use_container_width=True)
