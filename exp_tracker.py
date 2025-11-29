import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI
import matplotlib.pyplot as plt
load_dotenv()


gpt_key = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=gpt_key)
# response = client.responses.create(
#   model="gpt-5-nano",
#   input="write a haiku about ai",
#   store=True,
# )
# print(response.output_text)

file_path = 'expense_data_1.csv'

if os.path.exists(file_path):
    try:
        df = pd.read_csv(file_path)
        data = df[["Date", "Category", "Note", "Amount", "Income/Expense"]]
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
        data = pd.DataFrame(columns=["Date", "Category", "Note", "Amount", "Income/Expense"])
else:
    print("File does not exist. Creating a new DataFrame.")
    data = pd.DataFrame(columns=["Date", "Category", "Note", "Amount", "Income/Expense"])

expense_summary = data[data['Category'] != 'Income'].groupby("Category")["Amount"].sum()

# Pie Chart
plt.figure(figsize=(6,6))
expense_summary.plot.pie(autopct='%1.1f%%', startangle=90, shadow=True)
plt.title("Expenses Breakdown by Category")
plt.ylabel("")
plt.show()

# Bar Chart
plt.figure(figsize=(8,5))
expense_summary.plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Expenses  by Category")
plt.xlabel("Category")
plt.ylabel("Amount Spend")
plt.show()

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
    
# add_expense("2025-08-22 19:30", "Food", "Shawarma", 2500, "Expense")
# add_expense("2025-08-23 08:00", "Subscriptions", "Netflix Monthly Plan", 4500, "Expense")
# add_expense("2025-08-24 14:00", "Entertainment", "Outdoor Games with friends", 7000, "Expense")

data.to_csv(file_path, index=False)

def view_recent_expense():
    return data.tail()

def summarize_expenses(by="Category"):
    summary=data[data["Income/Expense"]=="Expense"].groupby(by)["Amount"].sum()
    return summary.sort_values(ascending=False)

# def auto_categorize(note):
#     prompt = f"""Categorize this expense note into one of these categories: Food, Transport, Entertainment, Other. Note: {note}"""
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         return "Other"
    
# data['Category'] = data.apply(
#     lambda row: auto_categorize(row['Note']) if pd.isna(row['Category']) else row['Category'], axis=1
# )

# print(data[['Note', 'Category']].head(10))