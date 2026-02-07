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

# Ensure numeric wealth (prevents errors if loaded as text)
df["wealth"] = pd.to_numeric(df["wealth"], errors="coerce")

# Column names in your dataset
COUNTRY_COL = "country_of_residence"
INDUSTRY_COL = "industry"
WEALTH_COL = "wealth"
GENDER_COL = "gender"

# --------------------------------------------------
# Title and Description
# --------------------------------------------------
st.title("Billionaires Dashboard")
st.markdown(
    "This interactive dashboard analyzes global billionaire data by country, "
    "industry, gender, and wealth."
)

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("Filter Options")

country_options = sorted(df[COUNTRY_COL].dropna().unique())
industry_options = sorted(df[INDUSTRY_COL].dropna().unique())

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=country_options,
    default=country_options
)

industry_filter = st.sidebar.multiselect(
    "Select Industry",
    options=industry_options,
    default=industry_options
)

# Apply filters
filtered_df = df[
    (df[COUNTRY_COL].isin(country_filter)) &
    (df[INDUSTRY_COL].isin(industry_filter))
]

if filtered_df.empty:
    st.warning("No data matches your filters. Please select more options.")
    st.stop()

# --------------------------------------------------
# Overview Metrics
# --------------------------------------------------
st.subheader("Overview Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Billionaires", len(filtered_df))
col2.metric("Total Wealth ($B)", round(filtered_df[WEALTH_COL].sum(skipna=True), 2))
col3.metric("Average Wealth ($B)", round(filtered_df[WEALTH_COL].mean(skipna=True), 2))

# --------------------------------------------------
# Visualization 1: Top Countries
# --------------------------------------------------
st.subheader("Top Countries by Number of Billionaires")

top_n = st.slider("Select number of countries", 5, 20, 10)

country_counts = (
    filtered_df[COUNTRY_COL]
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
    filtered_df[INDUSTRY_COL]
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
# Visualization 3: Wealth Distribution
# --------------------------------------------------
st.subheader("Wealth Distribution")

fig3 = px.histogram(
    filtered_df,
    x=WEALTH_COL,
    nbins=30,
    title="Distribution of Wealth ($ Billions)"
)
st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------------------
# Visualization 4: Gender Comparison
# --------------------------------------------------
st.subheader("Billionaires by Gender")

gender_counts = (
    filtered_df[GENDER_COL]
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
- The United States has the highest number of billionaires (check in your top countries chart).
- Technology and finance are among the most common industries.
- Billionaire wealth is concentrated among a small number of individuals.
- Male billionaires outnumber female billionaires in most countries.
""")



