import streamlit as st
import pandas as pd

st.set_page_config(page_title="Customer Shopping Behavior Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("customer_shopping_behavior.csv")

df = load_data()

st.title("🛒 Customer Shopping Behavior Dashboard")
st.markdown("Analyze trends in purchases, customer demographics, and spending patterns.")

st.sidebar.header("Filters")

genders = st.sidebar.multiselect(
    "Select Gender",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

categories = st.sidebar.multiselect(
    "Select Product Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

payment_methods = st.sidebar.multiselect(
    "Select Payment Method",
    options=df["payment_method"].unique(),
    default=df["payment_method"].unique()
)

filtered_df = df[
    (df["gender"].isin(genders)) &
    (df["category"].isin(categories)) &
    (df["payment_method"].isin(payment_methods))
]

st.write(f"### 📊 Showing {len(filtered_df)} records after filtering")

st.dataframe(filtered_df, use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sales ($)", round(filtered_df["price"].sum(), 2))

with col2:
    st.metric("Average Order Value ($)", round(filtered_df["price"].mean(), 2))

with col3:
    st.metric("Total Transactions", len(filtered_df))

st.markdown("## 📈 Insights")

col4, col5 = st.columns(2)

with col4:
    st.subheader("Sales by Category")
    st.bar_chart(filtered_df.groupby("category")["price"].sum())

with col5:
    st.subheader("Sales by Payment Method")
    st.bar_chart(filtered_df.groupby("payment_method")["price"].sum())

st.subheader("Customer Age Distribution")
st.histogram(filtered_df["age"])

st.success("Dashboard ready! Use filters on the left to explore the data.")

st.caption("Built with ❤️ using Streamlit")
