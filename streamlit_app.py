# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write("The name on your smoothie will be:", name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Read fruit options
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
)

fruit_list = my_dataframe.to_pandas()["FRUIT_NAME"].tolist()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

if ingredients_list and name_on_order:
    ingredients_string = ", ".join(ingredients_list)

    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (INGREDIENTS, NAME_ON_ORDER)
        VALUES
        ('{ingredients_string}', '{name_on_order}')
    """

    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")

elif ingredients_list and not name_on_order:
    st.warning("Please enter a name before submitting your smoothie order.")
