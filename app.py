import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบเต็มจอ (Wide mode) และใส่ชื่อหัวข้อเว็บ
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 2. ดึงข้อมูลจาก Google Sheets (เวอร์ชันแก้ไขภาษาไทยแล้ว)
@st.cache_data(ttl=60)
def load_data():
    sheet_id = "1BwpaZk_jtfquue-7F_LZKZbGWFfaTJoBmpe2tZK2B2A" 
    # ใช้ค่าส่งออก csv และระบุรหัสหน้าแรก (gid=0) แทนการใช้ชื่อแผ่นงานภาษาไทย
    url = f"https://google.com{sheet_id}/export?format=csv&gid=0"
    df = pd.read_csv(url)
    return df

try:
    df = load_data()
    # หัวข้อใหญ่ของแดชบอร์ด
    st.title("📊 ยอดขายแดชบอร์ด (Sales Dashboard)")
    st.markdown("---")

    total_sales = df['ยอดขาย'].sum() if 'ยอดขาย' in df.columns else 0
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
        if 'เขตพื้นที่' in df.columns and 'ยอดขาย' in df.columns:
            df_area = df.groupby('เขตพื้นที่', as_index=False)['ยอดขาย'].sum()
            fig_bar = px.bar(df_area, x='เขตพื้นที่', y='ยอดขาย', color='เขตพื้นที่', template='plotly_white')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("ไม่พบคอลัมน์ 'เขตพื้นที่' ใน Google Sheets")

    with col2:
        st.subheader("🍕 สัดส่วนยอดขายตามประเภทสินค้า")
        if 'สินค้า' in df.columns and 'ยอดขาย' in df.columns:
            df_product = df.groupby('สินค้า', as_index=False)['ยอดขาย'].sum()
            fig_pie = px.pie(df_product, values='ยอดขาย', names='สินค้า', hole=0.3, color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("ไม่พบคอลัมน์ 'สินค้า' ใน Google Sheets")

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
