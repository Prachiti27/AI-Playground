import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="Text-to-SQL App")
st.title("Talk to your DB")
st.write("Ask questions about the student grades database.")

db = SQLDatabase.from_uri("sqlite:///student_grades.db")

llm = ChatOllama(
    model="llama3",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
 You are a senior data analyst and SQL Expert.
 Given the database schema below, write a correct SQL 
 that answers the user's question.
 Rules:
 - Use only the tables and columns in the schema
 - Do NOT explain anything
 - Return ONLY the SQL query
 
 Schema:
 {schema}
 
 Question:
 {question}                                         
    """)

sql_chain = (
    prompt 
    | llm
    | StrOutputParser()
)

schema = db.get_table_info()

question = st.text_input(
    "Enter your question:",
    placeholder="e.g., Who scored highest marks in Math"
)

if question:
    try:
        sql_query = sql_chain.invoke(
            {"schema": schema, "question": question}
        ).strip()
        
        st.subheader("Generated SQL")
        st.code(sql_query, language="sql")
        
        st.subheader("Result")
        result = db.run(sql_query)
        st.write(result)
    except Exception as e:
        st.error(f"Error: {e}")
        