import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ฟังก์ชันดึงข้อมูลจาก Google Sheets ด้วยรูปแบบเฉพาะที่ถูกต้อง
@st.cache_data(ttl=5) # เคลียร์แคชทุกๆ 5 วินาทีเพื่อให้เห็นผลทันใจตอนเปลี่ยนเลข
def load_data():
    # ดึงข้อมูลผ่านแชร์รูปแบบกูเกิลสเปรดชีตโดยตรง
    url = "https://google.com"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip() # ลบเว้นวรรคหัวตาราง
    return df

try:
    df = load_data()
    st.title("📊 ยอดขายแดชบอร์ด (Sales Dashboard)")
    st.markdown("---")

    # ตั้งชื่อคอลัมน์ตามตารางจริงของคุณ
    sales_col = 'ยอดขาย'
    area_col = 'เขตพื้นที่'
    product_col = 'สินค้า'

    # ปรับแต่งชนิดข้อมูลให้เป็นตัวเลข
    df[sales_col] = pd.to_numeric(df[sales_col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)

    total_sales = df[sales_col].sum()
    total_items = len(df)

    mx1, mx2 = st.columns(2)
    with mx1:
        st.metric(label="💰 ยอดขายรวมทั้งหมด", value=f"{total_sales:,.2f} บาท")
    with mx2:
        st.metric(label="📦 จำนวนรายการขายทั้งหมด", value=f"{total_items:,} รายการ")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 ยอดขายแยกตามพื้นที่")
        df_area = df.groupby(area_col, as_index=False)[sales_col].sum()
        fig_bar = px.bar(df_area, x=area_col, y=sales_col, color=area_col, template='plotly_white')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("🍕 สัดส่วนยอดขายตามประเภทสินค้า")
        df_product = df.groupby(product_col, as_index=False)[sales_col].sum()
        fig_pie = px.pie(df_product, values=sales_col, names=product_col, hole=0.3, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการประมวลผลข้อมูล: {e}")
