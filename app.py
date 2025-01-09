import streamlit as st
import pandas as pd
from openpyxl import load_workbook, Workbook
import os
import datetime

# Excel Configuration
EXCEL_FILE = "friend_money_tracker.xlsx"

# Initialize Excel File if it doesn't exist
if not os.path.exists(EXCEL_FILE):
    wb = Workbook()
    ws = wb.active
    ws.append(["Date", "Type", "Amount", "Description"])  # Add header row
    wb.save(EXCEL_FILE)

# Load existing data
def load_data():
    try:
        return pd.read_excel(EXCEL_FILE)
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
        return pd.DataFrame(columns=["Date", "Type", "Amount", "Description"])

# Save data to Excel
def save_data(dataframe):
    try:
        dataframe.to_excel(EXCEL_FILE, index=False)
    except Exception as e:
        st.error(f"Error saving to the Excel file: {e}")

# Initialize the app
st.set_page_config(page_title="Friend Money Tracker", layout="centered")
st.title("Money Tracker with Friend")

# Add a new transaction
st.subheader("Add a Transaction")
transaction_type = st.radio("Transaction Type", ["Borrowed", "Repaid"])
amount = st.number_input("Amount", min_value=0.01, step=0.01)
description = st.text_area("Description (optional)", placeholder="e.g., Lunch money")
date = st.date_input("Date", value=datetime.date.today())

if st.button("Add Transaction"):
    # Load data and append new transaction
    data = load_data()
    new_transaction = {"Date": str(date), "Type": transaction_type, "Amount": amount, "Description": description}
    data = pd.concat([data, pd.DataFrame([new_transaction])], ignore_index=True)  # Use pd.concat instead of append
    save_data(data)
    st.success("Transaction added!")

# Fetch and display transaction history
st.subheader("Transaction History")
data = load_data()
if not data.empty:
    st.dataframe(data)

    # Calculate summary
    total_borrowed = data[data["Type"] == "Borrowed"]["Amount"].sum()
    total_repaid = data[data["Type"] == "Repaid"]["Amount"].sum()
    balance = total_borrowed - total_repaid

    # Display totals
    st.subheader("Summary")
    st.metric("Total Borrowed", f"Rs.{total_borrowed:.2f}")
    st.metric("Total Repaid", f"Rs.{total_repaid:.2f}")
    st.metric("Current Balance", f"Rs.{balance:.2f}")
else:
    st.info("No transactions recorded yet.")

