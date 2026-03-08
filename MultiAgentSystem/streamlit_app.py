import streamlit as st
from agent import app

st.set_page_config(page_title="AI Blog Generator")

st.title("AI Research Blog Generator")
st.write("Enter a topic and the AI will research and write a blog.")

topic = st.text_input("Enter a topic")

if st.button("Generate Blog"):
    
    if topic.strip()=="":
        st.warning("Please enter a topic")
    else:
        with st.spinner("Researching and writing..."):
            result = app.invoke({
                "topic": topic,
                "research_data": [],
                "blog_post": ""
            })
            
        st.subheader("Generated Blog Post")
        st.write(result["blog_post"])