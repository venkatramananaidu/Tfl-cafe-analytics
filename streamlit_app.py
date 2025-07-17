import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set wide layout
st.set_page_config(layout="wide", page_title="TFL Café Analytics")

#background

# Add a background image using custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Load data
@st.cache_data
def load_data():
    footfall_df = pd.read_csv("data/footfall_data.csv", parse_dates=["date"])
    sales_df = pd.read_csv("data/cafe_sales_data.csv", parse_dates=["date"])
    events_df = pd.read_csv("data/external_data.csv", parse_dates=["date"])
    return footfall_df, sales_df, events_df


footfall_df, sales_df, external_df = load_data()

# Merge for analysis
df = footfall_df.merge(sales_df, on="date").merge(external_df, on="date")

# Sidebar filters
st.sidebar.title("📊 Filters")
selected_cafe = st.sidebar.selectbox("Select a Café", options=["All"] + sorted(sales_df["cafe_name"].unique()))
date_range = st.sidebar.date_input("Select Date Range", [df["date"].min(), df["date"].max()])

# Filter data
filtered_df = df.copy()
if selected_cafe != "All":
    filtered_df = filtered_df[filtered_df["cafe_name"] == selected_cafe]
filtered_df = filtered_df[(filtered_df["date"] >= pd.to_datetime(date_range[0])) & 
                          (filtered_df["date"] <= pd.to_datetime(date_range[1]))]

# Title
st.title("☕ Café Performance Analytics")
st.markdown("Exploring how footfall, weather, and events impact café sales.")

# 1. Sales Over Time
st.subheader("📈 Sales Over Time")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtered_df, x="date", y="sales_amount", hue="cafe_name", marker="o", ax=ax1)
ax1.set_ylabel("Sales (£)")
ax1.set_xlabel("Date")
ax1.tick_params(axis='x', rotation=45)
st.pyplot(fig1)


#st.write("Columns available:", filtered_df.columns.tolist())

# Safe merge
df = footfall_df.merge(sales_df, on="date").merge(external_df, on="date")

encoded_df = filtered_df.copy()
# 3. Correlation Heatmap
st.subheader("📊 Correlation Heatmap")

# Prepare dataframe for correlation
encoded_df = filtered_df.copy()

# Encode 'event' as category if it exists
if 'event' in encoded_df.columns:
    encoded_df['event'] = encoded_df['event'].astype('category').cat.codes

# Only include numeric columns for correlation
corr_columns = ['sales_amount', 'entries', 'exits', 'customers', 'temperature_c', 'rain_mm', 'event']
existing_corr_columns = [col for col in corr_columns if col in encoded_df.columns]
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(1, 1, 1)
sns.heatmap(encoded_df[existing_corr_columns].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
ax.set_title("Correlation Between Metrics", fontsize=14)
plt.tight_layout()
st.pyplot(fig)  # Pass the figure object directly to Streamlit

import streamlit as st

# --- Chat with Data Section ---
st.markdown("---")
st.subheader("💬 Chat with your sales Data")

# Search widget
user_query = st.text_input("Ask a question about the data:")

# Placeholder response (you can connect this to real logic later)
if user_query:
    st.info(f"🔍 You asked: **{user_query}**")
    st.warning("⚠️ This is a placeholder response. Real data insights coming soon!")
d
# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Data: Synthetic + TFL"

)

