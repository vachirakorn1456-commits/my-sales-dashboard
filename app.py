import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าแดชบอร์ดเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ฟังก์ชันดึงข้อมูลอัตโนมัติจาก Google Sheets
@st.cache_data(ttl=5)
def load_data():
    # โค้ดถอดรหัสลับเพื่อป้องกันระบบแอบสลับตัวพิมพ์เล็กพิมพ์ใหญ่และโดเมนเว็บ
    r = "104 116 116 112 115 58 47 47 100 111 99 115 46 103 111 111 103 108 101 46 99 111 109 47 115 112 114 101 97 100 115 104 101 101 116 115 47 100 47 49 78 80 75 101 118 67 67 112 78 113 65 114 107 106 114 76 55 119 113 73 71 103 50 51 115 118 95 48 87 66 108 114 118 50 70 50 110 113 67 81 114 115 47 101 120 112 111 114 116 63 102 111 114 109 97 116 61 99 115 118"
    url = "".join([chr(int(x)) for x in r.split()])
    
    # อ่านข้อมูลและลบช่องว่างส่วนเกินที่หัวคอลัมน์
    df = pd.read_csv(url, header=0)
    df.columns = df.columns.str.strip()
    return df

# เรียกใช้งานฟังก์ชันโหลดข้อมูล
df = load_data()

# 3. แสดงผลแดชบอร์ด
st.title("📊 Sales Dashboard - รายงานยอดขายอัตโนมัติ")
st.markdown("---")

# แสดงตารางข้อมูลดิบ
st.subheader("📋 ตารางข้อมูลยอดขาย (อัปเดตตาม Google Sheets ล่าสุด)")
st.dataframe(df, use_container_width=True)

# สร้างกราฟแสดงผลยอดขายแยกตามพื้นที่
if 'เขตพื้นที่' in df.columns and 'ยอดขาย' in df.columns:
    st.subheader("📈 กราฟสรุปยอดขายแยกตามเขตพื้นที่")
    df['ยอดขาย'] = pd.to_numeric(df['ยอดขาย'], errors='coerce').fillna(0)
    fig = px.bar(df, x='เขตพื้นที่', y='ยอดขาย', color='สินค้า', barmode='group')
    st.plotly_chart(fig, use_container_width=True)
