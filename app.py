# Natural Language Text to SQL LLM Application
#Prompt --> LLM -->Gemini Pro --->Query -->SQL Database -->Response.
from dotenv import load_dotenv
load_dotenv() #load all the environement variables.

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

## Configure our API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Function to Load Google Gemini Model and Provide sql Query as Response.

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text
    
    # Clean the response to extract only the SQL query
    query = response.text.strip()  # Remove unnecessary whitespace
    query = query.replace('\n', ' ')  # Replace newline characters with spaces
    print(f"Generated SQL Query: {query}")
    
    return query

#Function to retrieve query from the sql database.
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


#Define Your Prompt
prompt=[
'''
You are an expert in converting English questions to SQL query!you are also expert in predicting crop yield ie. Hectogram_per_Hectare !The SQL database has the name Crop with the following columns - Country,Item,Year,Hectogram_per_Hectare,Rainfall,Pesticides,Temprature. Here Item represents Crop name. So based on user inputs you need to predict Hectogram_per_Hectare in tonnes.Inputs can be Country,Crop,Year,Rainfall,Pesticides,Temprature.You need to give response as "Expected Crop yield is:" also you need to predict crop name having highest Hectogram_per_Hectare as per user inputs.
Example 1 - Which crop has highest yield in 2025 for country India; Example 2 - Tell me all the crops ?
the SQL command will be something like this SELECT * From Crop;
also the sql code should not have ``` in beginning or end and sql word in output.
'''
]

#Streamlit APP
import streamlit as st

# Page configuration
st.set_page_config(page_title="I can Predict your Crop Yield :)")

# Add custom CSS for styling
page_bg_color = """
<style>
body {
    background-color: #f5f5dc; /* Beige background */
    color: #2c3e50; /* Text color (dark blue-grey) */
    font-family: 'Arial', sans-serif; /* Optional: set a font */
}
header {
    display: flex;
    justify-content: center;
    align-items: center;
}
header img {
    width: 100%;
    height: 25vh;
    object-fit: cover; /* Ensure the image scales proportionally */
}
.sidebar-image {
    position: fixed;
    top: 50%;
    left: 200px;
    transform: translate(-50%, -50%);
    width: 200px; /* Adjust width as needed */
}
</style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

# Add images
st.markdown('<header><img src="<a href="https://www.freepik.com/free-vector/radishes-growing-soil-cartoon_26350144.htm#fromView=keyword&page=1&position=5&uuid=d654b6e9-12b4-47ad-a64c-c8ee19702b10&new_detail=true">Image by brgfx on Freepik</a>" alt="Top Image"></header>', unsafe_allow_html=True)
st.markdown('<img class="sidebar-image" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCRcNa0eZn6JVfEk2uqmf3006L5a5TU5zIbQ&s" alt="Left Image">', unsafe_allow_html=True)

# Header and inputs
st.header("Know your Yield with CropAI")
question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# Your logic here...
if submit and question:
    st.write(f"You asked: {question}")


#if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    data=read_sql_query(response,"project.db")
    st.subheader("The Response is ")
    for row in data:
        print(row)
        st.header(row)
