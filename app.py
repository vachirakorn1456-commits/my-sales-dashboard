import streamlit as st
import pandas as pd
import plotly.express as px

# อ่านข้อมูลจาก Excel
df = pd.read_excel("sales_data.xlsx")

# Title
st.title("Dashboard ยอดขาย")

# Filter
product = st.selectbox("เลือกสินค้า", df["สินค้า"].unique())

# กรองข้อมูลตามสินค้า
filtered = df[df["สินค้า"] == product]

# กราฟยอดขายตามพื้นที่
fig = px.bar(filtered, x="เขตพื้นที่", y="ยอดขาย", title=f"ยอดขายของ {product}")
st.plotly_chart(fig)

# กราฟยอดขายรวมตามสินค้า
summary = df.groupby("สินค้า")["ยอดขาย"].sum().reset_index()
fig2 = px.pie(summary, names="สินค้า", values="ยอดขาย", title="สัดส่วนยอดขายตามสินค้า")
st.plotly_chart(fig2)