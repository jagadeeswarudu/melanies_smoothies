# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)
name_on_order=st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be:',name_on_order)
cnx = st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('search_on'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()
ingredients_list=st.multiselect('choose upto 5 ingreadiants:',my_dataframe,max_selections=5)
if ingredients_list:
    ingredients_string=''
    for i in ingredients_list:
        ingredients_string+=i+' '
    my_insert_stmt = """ insert into smoothies.public.orders (ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    time_to_sumbit=st.button('Submit Order')
    st.write(my_insert_stmt)
    if time_to_sumbit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!'+name_on_order, icon="✅")
import requests
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width = True)
