import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(
    page_title="Business Insights Dashboard",
    layout="centered"
)

# Title
st.title("Business Insights Dashboard")
st.write("Upload your sales data file to view business insights.")

# File upload
uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df)

    # Required columns
    required_columns = ["Date", "Product", "Sales", "Profit"]

    if all(column in df.columns for column in required_columns):

        # Convert Date column
        df["Date"] = pd.to_datetime(df["Date"])

        # Business metrics
        total_sales = df["Sales"].sum()
        total_profit = df["Profit"].sum()

        st.subheader("Key Business Metrics")
        col1, col2 = st.columns(2)
        col1.metric("Total Sales", f"{total_sales}")
        col2.metric("Total Profit", f"{total_profit}")

        # Monthly sales trend
        monthly_sales = (
            df.groupby(df["Date"].dt.to_period("M"))["Sales"]
            .sum()
        )

        st.subheader("Monthly Sales Trend")
        fig1, ax1 = plt.subplots()
        monthly_sales.plot(kind="line", marker="o", ax=ax1)
        ax1.set_xlabel("Month")
        ax1.set_ylabel("Sales")
        st.pyplot(fig1)

        # Top-selling products
        product_sales = (
            df.groupby("Product")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        st.subheader("Top-Selling Products")
        fig2, ax2 = plt.subplots()
        product_sales.plot(kind="bar", ax=ax2)
        ax2.set_xlabel("Product")
        ax2.set_ylabel("Sales")
        st.pyplot(fig2)

    else:
        st.error(
            "The file must contain these columns: "
            "Date, Product, Sales, Profit"
        )
