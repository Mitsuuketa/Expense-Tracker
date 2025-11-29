import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

api_key = st.secrets.get("OPENAI_KEY")
print(api_key)
if not api_key:
    st.error("OpenAI API key is missing!")
    st.stop()
# open_ai_key = st.secrets["OPENAI_KEY"]["key"]
# gpt_key = os.getenv('OPENAI_KEY')
client=OpenAI(api_key=api_key)

def predict_category(description):
    prompt = f"""
    Categorize this expense into one of the following categories: ['Food', 'Transport', 'Entertainment', 'Utilities', 'Shopping', 'Others'].
    
    Expense: "{description}"
    Just return the category name.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

csv_file = "expense_data_1.csv"
if os.path.exists(csv_file):
    try:
        df = pd.read_csv(csv_file)
        data = df[["Date", "Category", "Note", "Amount", "Income/Expense"]]
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
        data = pd.DataFrame(columns=["Date", "Category", "Note", "Amount", "Income/Expense"])
else:
    print("File does not exist. Creating a new DataFrame.")
    data = pd.DataFrame(columns=["Date", "Category", "Note", "Amount", "Income/Expense"])
    
st.title("Smart Expense Tracker")

with st.form("expense_form"):
    date = st.date_input("Date")
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    
    predicted_category = ""
    if description:
        predicted_category = predict_category(description)
        
    category = st.text_input(
        "Category (predicted but editable)", 
        value=predicted_category
    )
    
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        new_expense = {"Date": date, "Description": description, "Note": description, "Amount": amount, "Category": category}
        data = pd.concat([data, pd.DataFrame([new_expense])], ignore_index=True)
        data.to_csv(csv_file, index=False)
        st.success(f"Added: {description} - {amount} ({category})")
        
st.subheader("All Expenses")
st.dataframe(data)

if not data.empty:
    st.subheader("Expense Breakdown by Category")
    
    category_totals = data.groupby("Category")["Amount"].sum()
    
    # Bar Chart
    fig, ax = plt.subplots()
    category_totals.plot(kind="bar", ax=ax)
    ax.set_ylabel("Amount")
    st.pyplot(fig)
    
    # Pie Chart
    st.subheader ("Category Distribution")
    fig2, ax2 = plt.subplots()
    category_totals.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    st.pyplot(fig2)
    
    
def add_expense(date, category, note, amount, exp_type="Expense"):
    global data
    new_entry = {
        "Date": date,
        "Category": category,
        "Note": note,
        "Amount": amount,
        "Income/Expense": exp_type
    }
    
    new_df=pd.DataFrame([new_entry])
    data =pd.concat([data, new_df], ignore_index=True)
    print(f"Added: {note} - {amount} ({category})")