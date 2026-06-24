import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าแดชบอร์ดเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ฟังก์ชันดึงข้อมูลอัตโนมัติจาก Google Sheets
@st.cache_data(ttl=5)
def load_data():
    # แก้ไขรหัส ID ให้ตรงกับหน้าจอคอมพิวเตอร์ของคุณแบบเป๊ะๆ 100%
    p1 = "https://google.com"
    p2 = "1NPKevCCpNQArkjrL7wqIGg23s5v_0WBlrv2F2nqCQrs"
    p3 = "/export?format=csv"
    
    url = p1 + p2 + p3
    df = pd.read_csv(url, header=0)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# 3. แสดงผลแดชบอร์ด
st.title("📊 Sales Dashboard - รายงานยอดขายอัตโนมัติ")
st.markdown("---")

st.subheader("📋 ตารางข้อมูลยอดขาย (อัปเดตตาม Google Sheets ล่าสุด)")
st.dataframe(df, use_container_width=True)

if 'เขตพื้นที่' in df.columns and 'ยอดขาย' in df.columns:
    st.subheader("📈 กราฟสรุปยอดขายแยกตามเขตพื้นที่")
    df['ยอดขาย'] = pd.to_numeric(df['ยอดขาย'], errors='coerce').fillna(0)
    fig = px.bar(df, x='เขตพื้นที่', y='ยอดขาย', color='สินค้า', barmode='group')
    st.plotly_chart(fig, use_container_width=True)
