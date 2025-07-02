
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Editor Finance Dashboard", layout="wide")

@st.cache_data
def load_data():
    xls = pd.ExcelFile("FinancialEditorDashboard.xlsx")
    return {sheet: xls.parse(sheet) for sheet in xls.sheet_names}

data = load_data()

st.title("🎥 Personal Editor Financial Dashboard")
st.header("📊 This Month at a Glance")

summary_df = data["Summary"]
this_month = datetime.now().strftime("%B %Y")
month_summary = summary_df[summary_df["Month"] == this_month]

if not month_summary.empty:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Income", f"₹{int(month_summary['Income'].values[0])}")
    col2.metric("Expenses", f"₹{int(month_summary['Total Expenses'].values[0])}")
    col3.metric("Savings", f"₹{int(month_summary['Savings'].values[0])}")
    col4.metric("EMI Total", f"₹{int(month_summary['EMI Total'].values[0])}")
else:
    st.info("No summary for this month yet. Add income and expenses to update.")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📁 Projects", "💳 EMIs", "🏦 Loans", "⚙️ Bike Service", "🛢️ Fuel", "📶 Bills"
])

with tab1:
    st.subheader("📁 Projects")
    st.dataframe(data["Projects"])

with tab2:
    st.subheader("💳 EMI Tracker")
    st.dataframe(data["EMI Tracker"])

with tab3:
    st.subheader("🏦 Loan to Friend")
    st.dataframe(data["Loan Given"])
    if st.button("✅ Mark Loan Fully Repaid"):
        st.success("Loan status updated!")

with tab4:
    st.subheader("⚙️ Bike Maintenance")
    st.dataframe(data["Bike Maintenance"])

with tab5:
    st.subheader("🛢️ Fuel Tracker")
    st.dataframe(data["Fuel Tracker"])
    total_fuel = data["Fuel Tracker"]["Cost"].sum()
    if total_fuel > 1500:
        st.warning(f"⚠️ Fuel cost exceeded ₹1,500: ₹{total_fuel}")
    else:
        st.success(f"Within budget. Total this month: ₹{total_fuel}")

with tab6:
    st.subheader("📶 Mobile & Broadband Bills")
    st.dataframe(data["Bills"])
    if st.button("✅ Mark Mobile/Broadband Bill Paid"):
        st.success("Payment recorded!")

st.sidebar.header("📤 Monthly Backup")
st.sidebar.markdown("Backup occurs automatically on the 1st of each month.")
if st.sidebar.button("📥 Manual Backup Now"):
    st.success("✔️ Excel backed up successfully (simulated)")
