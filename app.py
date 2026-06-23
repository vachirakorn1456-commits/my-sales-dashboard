import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบเต็มจอ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ดึงข้อมูลจาก Google Sheets (รองรับชื่อแท็บทุกแบบ)
@st.cache_data(ttl=30)
def load_data():
    sheet_id = "1BwpaZk_jtfquue-7F_LZKZbGWFfaTJoBmpe2tZK2B2A"
    # ดึงหน้าแรกสุดของ Sheets เสมอ ไม่ว่าด้านล่างจะชื่อว่าอะไร
    url = f"https://google.com{sheet_id}/export?format=csv&gid=0"
    df = pd.read_csv(url)
    # ล้างช่องว่างที่อาจติดมาในชื่อคอลัมน์
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
    st.title("📊 ยอดขายแดชบอร์ด (Sales Dashboard)")
    st.markdown("---")

    # ตรวจสอบชื่อคอลัมน์ให้ตรงเป๊ะกับในรูป Excel
    sales_col = 'ยอดขาย' if 'ยอดขาย' in df.columns else (df.columns[3] if len(df.columns) > 3 else None)
    area_col = 'เขตพื้นที่' if 'เขตพื้นที่' in df.columns else (df.columns[2] if len(df.columns) > 2 else None)
    product_col = 'สินค้า' if 'สินค้า' in df.columns else (df.columns[1] if len(df.columns) > 1 else None)

    # แปลงคอลัมน์ยอดขายให้เป็นตัวเลข
    if sales_col:
        df[sales_col] = pd.to_numeric(df[sales_col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)

    total_sales = df[sales_col].sum() if sales_col else 0
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
        if area_col and sales_col:
            df_area = df.groupby(area_col, as_index=False)[sales_col].sum()
            fig_bar = px.bar(df_area, x=area_col, y=sales_col, color=area_col, template='plotly_white')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("ไม่พบคอลัมน์เกี่ยวกับ 'พื้นที่' ในตารางข้อมูล")

    with col2:
        st.subheader("🍕 สัดส่วนยอดขายตามประเภทสินค้า")
        if product_col and sales_col:
            df_product = df.groupby(product_col, as_index=False)[sales_col].sum()
            fig_pie = px.pie(df_product, values=sales_col, names=product_col, hole=0.3, color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("ไม่พบคอลัมน์เกี่ยวกับ 'สินค้า' ในตารางข้อมูล")

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการประมวลผล: {e}")
