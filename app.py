import streamlit as st
import pandas as pd

st.set_page_config(page_title="Customer Shopping Behavior Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("customer_shopping_behavior.csv")

df = load_data()

st.title("🛒 Customer Shopping Behavior Dashboard")
st.markdown("Analyze trends in purchases, customer demographics, and spending patterns.")

st.write("### Available columns in dataset:")
st.write(list(df.columns))

st.sidebar.header("Filters")

if "gender" in df.columns:
    genders = st.sidebar.multiselect("Select Gender", df["gender"].unique(), df["gender"].unique())
else:
    genders = df.index

if "category" in df.columns:
    categories = st.sidebar.multiselect("Select Product Category", df["category"].unique(), df["category"].unique())
else:
    categories = df.index

if "payment_method" in df.columns:
    payment_methods = st.sidebar.multiselect("Select Payment Method", df["payment_method"].unique(), df["payment_method"].unique())
else:
    payment_methods = df.index

filtered_df = df.copy()

if "gender" in df.columns:
    filtered_df = filtered_df[filtered_df["gender"].isin(genders)]

if "category" in df.columns:
    filtered_df = filtered_df[filtered_df["category"].isin(categories)]

if "payment_method" in df.columns:
    filtered_df = filtered_df[filtered_df["payment_method"].isin(payment_methods)]

st.write(f"### 📊 Showing {len(filtered_df)} records")
st.dataframe(filtered_df, use_container_width=True)

if "price" in filtered_df.columns:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales ($)", round(filtered_df["price"].sum(), 2))
    with col2:
        st.metric("Average Order Value ($)", round(filtered_df["price"].mean(), 2))
    with col3:
        st.metric("Total Transactions", len(filtered_df))

st.markdown("## 📈 Insights")

if "category" in filtered_df.columns and "price" in filtered_df.columns:
    st.subheader("Sales by Category")
    st.bar_chart(filtered_df.groupby("category")["price"].sum())

if "payment_method" in filtered_df.columns and "price" in filtered_df.columns:
    st.subheader("Sales by Payment Method")
    st.bar_chart(filtered_df.groupby("payment_method")["price"].sum())

if "age" in filtered_df.columns:
    st.subheader("Customer Age Distribution")
    st.histogram(filtered_df["age"])

st.caption("Built with ❤️ using Streamlit")
