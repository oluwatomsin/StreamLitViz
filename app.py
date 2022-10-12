import pandas as pd
import plotly_express as px
import streamlit as st

# Setting web app basic configuration
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":boom:",  # *favicon
    layout="wide"
)


@st.cache
def get_data_fron_excel():
    dtf = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000
    )
    # ADD HOUR COLUMN TO DATAFRAME
    dtf["hour"] = pd.to_datetime(dtf["Time"], format="%H:%M:%S").dt.hour
    return dtf


df = get_data_fron_excel()

# st.dataframe(df)

# ------  SIDE BAR  ------
st.sidebar.header("Please filter here:")
city = st.sidebar.multiselect(
    "Select the city:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

gender = st.sidebar.multiselect(
    "Select the gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer_type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

# --------- SELECTION OF DATAFRAME -------
df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# ------ MAIN PAGE ------
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sales_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sales_by_transaction}")

st.markdown("---")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(sales_by_product_line,
                           x="Total",
                           y=sales_by_product_line.index,
                           title="<b>Sales by Product Line</b>",
                           color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
                           template="plotly_white")
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0, 0, 0, 0)"
)

# SALES BY HOUR
sales_by_hour = (
    df_selection.groupby(by=["hour"]).sum()[["Total"]].sort_values(by="Total")
)
fig_hourly_sales = px.bar(sales_by_hour,
                          y="Total",
                          x=sales_by_hour.index,
                          title="<b>Sales by Hour</b>",
                          color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
                          template="plotly_white")
fig_hourly_sales.update_layout(
    plot_bgcolor="rgba(0, 0, 0, 0)",
    xaxis=dict(tickmode="linear")
)

left_plot, right_plot = st.columns(2)
left_plot.plotly_chart(fig_product_sales, use_container_width=True)
right_plot.plotly_chart(fig_hourly_sales, use_container_width=True)
