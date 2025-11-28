
import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Financial Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- Custom CSS for Styling ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# local_css("web/style.css") # You can create this file for advanced styling

st.markdown("""
<style>
    .main {
        background-color: #F5F5F5;
    }
    .card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .metric {
        text-align: center;
    }
    .metric-value {
        font-size: 2.5em;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1.2em;
        color: #555555;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #76b852, #8DC26F);
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_transactions():
    try:
        df = pd.read_csv("database/transactions.txt")
        df['amount'] = df['amount'] / 100  # Convert from paisa/cents
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['date', 'type', 'category', 'amount', 'description'])

@st.cache_data
def load_budgets():
    try:
        df = pd.read_csv("database/budgets.txt", header=None, names=['category', 'budget'])
        df['budget'] = df['budget'] / 100  # Convert from paisa/cents
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=['category', 'budget'])


transactions_df = load_transactions()
budgets_df = load_budgets()

# --- Main Dashboard ---
st.title("📊 Personal Finance Dashboard")

# --- Balance Section ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.header("Financial Overview")

total_income = transactions_df[transactions_df['type'] == 'Income']['amount'].sum()
total_expenses = transactions_df[transactions_df['type'] == 'Expense']['amount'].sum()
current_balance = total_income - total_expenses

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric">', unsafe_allow_html=True)
    st.markdown(f'<p class="metric-label">Current Balance</p><p class="metric-value" style="color: {"#2E8B57" if current_balance >= 0 else "#DC143C"};">₹{current_balance:,.2f}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric">', unsafe_allow_html=True)
    st.markdown(f'<p class="metric-label">Total Income</p><p class="metric-value" style="color: #2E8B57;">₹{total_income:,.2f}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric">', unsafe_allow_html=True)
    st.markdown(f'<p class="metric-label">Total Expenses</p><p class="metric-value" style="color: #DC143C;">₹{total_expenses:,.2f}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# --- Budget Status Section ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.header("Budget Status")

if not budgets_df.empty:
    expense_summary = transactions_df[transactions_df['type'] == 'Expense'].groupby('category')['amount'].sum().reset_index()
    budget_summary = pd.merge(budgets_df, expense_summary, on='category', how='left').fillna(0)
    budget_summary.rename(columns={'amount': 'spent'}, inplace=True)
    budget_summary['remaining'] = budget_summary['budget'] - budget_summary['spent']
    budget_summary['utilization'] = (budget_summary['spent'] / budget_summary['budget']) * 100

    for index, row in budget_summary.iterrows():
        st.subheader(row['category'])
        col1, col2 = st.columns([3,1])
        with col1:
            progress = min(row['utilization'] / 100, 1.0)
            st.progress(progress)
        with col2:
            utilization_color = "green"
            if row['utilization'] > 100:
                utilization_color = "red"
            elif row['utilization'] >= 70:
                utilization_color = "orange"
            st.markdown(f'<p style="color:{utilization_color}; text-align:right;">{row["utilization"]:.2f}%</p>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Budget", f"₹{row['budget']:,.2f}")
        col2.metric("Spent", f"₹{row['spent']:,.2f}")
        col3.metric("Remaining", f"₹{row['remaining']:,.2f}")
        st.markdown("---")
else:
    st.info("No budgets set. You can set budgets in the CLI application.")

st.markdown('</div>', unsafe_allow_html=True)


# --- Recent Transactions Table ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.header("Recent Transactions")

recent_transactions = transactions_df.sort_values(by='date', ascending=False).head(10)

def style_df(df):
    def highlight_type(row):
        color = 'green' if row['type'] == 'Income' else 'red'
        return [f'color: {color}'] * len(row)
    return df.style.apply(highlight_type, axis=1)

if not recent_transactions.empty:
    st.dataframe(style_df(recent_transactions[['date', 'type', 'category', 'description', 'amount']]), use_container_width=True)
else:
    st.info("No transactions found.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='text-align: center; margin-top: 20px;'><p>Generated by Gemini</p></div>", unsafe_allow_html=True)

# To run this app:
# 1. Make sure you have streamlit installed: pip install streamlit
# 2. Run in your terminal: streamlit run web/dashboard.py
