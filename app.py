import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ดึงข้อมูลจาก Google Sheets
@st.cache_data(ttl=5)
def load_data():
    url = "https://google.com"
    df = pd.read_csv(url)
    return df

try:
    df = load_data()
    st.title("📊 ยอดขายแดชบอร์ด (Sales Dashboard)")
    st.markdown("---")

    # บังคับกำหนดตำแหน่งคอลัมน์ตามลำดับตาราง (A=0, B=1, C=2, D=3)
    product_col = df.columns[1]  # ช่อง B (สินค้า)
    area_col = df.columns[2]     # ช่อง C (เขตพื้นที่)
    sales_col = df.columns[3]    # ช่อง D (ยอดขาย)

    # แปลงคอลัมน์ยอดขายให้เป็นตัวเลข
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
    st.error(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
