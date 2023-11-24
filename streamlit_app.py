import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

#################
# New Section to display fruityvice api response
################ 

#creating repeatable code block / function
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) # takes the json version of the response and normalizes it
    return fruityvice_normalized
     
streamlit.header("Fruityvice Fruit Advice!")
try:
  # text input so that user can choose which fruit to see information about
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function) # outputs it to the screen as a table
except URLError as e:
  streamlit.error()

################
# Connecting Snowflake to Streamlit
################

streamlit.header("The fruit load list contains:")

# Snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
        
# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

streamlit.stop()

# Allow end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add', 'jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

# This won't work properly
my_cur.execute("insert into fruit_load_list values ('from streamlit')")



