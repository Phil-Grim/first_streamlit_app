import streamlit
import pandas
import requests

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt") # using a csv hosted by Snowflake in their AWS S£ bucket
my_fruit_list = my_fruit_list.set_index('Fruit') # setting Fruit to the dataframe index so that the multiselect function below picks out the Fruit to be displayed as options in the app

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected] # filter the table based on the fruits that have been selected

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#NewSection to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

# could use below to have a selectbox where you select an option and the fruityvice json for that fruit is returned
# issue is that not all the fruits in my_fruit_list have entries in fruityvice
# fruit_for_advice = streamlit.selectbox("Pick a fruit to see it's information",list(my_fruit_list.index))
# fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_for_advice}")

fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response.json())



