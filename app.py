import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Billionaires Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("billionaires.csv")

df = load_data()
st.write(df.columns)
st.stop()


# --------------------------------------------------
# Title and Description
# --------------------------------------------------
st.title("Billionaires Dashboard")
st.markdown(
    "This interactive dashboard analyzes global billionaire data by country, "
    "industry, gender, and net worth."
)

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("Filter Options")

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=sorted(df["country"].dropna().unique()),
    default=sorted(df["country"].dropna().unique())
)

industry_filter = st.sidebar.multiselect(
    "Select Industry",
    options=sorted(df["industry"].dropna().unique()),
    default=sorted(df["industry"].dropna().unique())
)

# Apply filters
filtered_df = df[
    (df["country"].isin(country_filter)) &
    (df["industry"].isin(industry_filter))
]

# --------------------------------------------------
# Overview Metrics
# --------------------------------------------------
st.subheader("Overview Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Billionaires", len(filtered_df))
col2.metric(
    "Total Net Worth ($B)",
    round(filtered_df["netWorth"].sum(), 2)
)
col3.metric(
    "Average Net Worth ($B)",
    round(filtered_df["netWorth"].mean(), 2)
)

# --------------------------------------------------
# Visualization 1: Top Countries
# --------------------------------------------------
st.subheader("Top Countries by Number of Billionaires")

top_n = st.slider("Select number of countries", 5, 20, 10)

country_counts = (
    filtered_df["country"]
    .value_counts()
    .head(top_n)
    .reset_index()
)

country_counts.columns = ["Country", "Number of Billionaires"]

fig1 = px.bar(
    country_counts,
    x="Country",
    y="Number of Billionaires",
    title="Number of Billionaires by Country"
)

st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------
# Visualization 2: Industry Distribution
# --------------------------------------------------
st.subheader("Billionaires by Industry")

industry_counts = (
    filtered_df["industry"]
    .value_counts()
    .reset_index()
)

industry_counts.columns = ["Industry", "Count"]

fig2 = px.pie(
    industry_counts,
    names="Industry",
    values="Count",
    title="Industry Distribution of Billionaires"
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# Visualization 3: Net Worth Distribution
# --------------------------------------------------
st.subheader("Net Worth Distribution")

fig3 = px.histogram(
    filtered_df,
    x="netWorth",
    nbins=30,
    title="Distribution of Net Worth ($ Billions)"
)

st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------------------
# Visualization 4: Gender Comparison
# --------------------------------------------------
st.subheader("Billionaires by Gender")

gender_counts = (
    filtered_df["gender"]
    .value_counts()
    .reset_index()
)

gender_counts.columns = ["Gender", "Count"]

fig4 = px.bar(
    gender_counts,
    x="Gender",
    y="Count",
    title="Gender Distribution of Billionaires"
)

st.plotly_chart(fig4, use_container_width=True)

# --------------------------------------------------
# Key Insights
# --------------------------------------------------
st.subheader("Key Insights")

st.markdown("""
- The United States has the highest number of billionaires.
- Technology and finance are the most common industries.
- Billionaire wealth is highly concentrated among a small number of individuals.
- Male billionaires significantly outnumber female billionaires.
""")
