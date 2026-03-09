import streamlit as st
import speech_recognition as sr
import ollama
import pyttsx3

def listen():
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            st.write("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
        text = recognizer.recognize_google(audio)
        return text
    except sr.WaitTimeoutError:
        st.warning("No speech detected (timeout).")
        return None
    except sr.UnknownValueError:
        st.warning("Sorry, I didn't catch that.")
        return None
    except sr.RequestError:
        st.error("Speech recognition service unavailable.")
        return None
    except Exception as e:
        st.error(f"An error occured in listen() : {e}")
        return None
    
def think(text: str):
    if not text:
        return None
    
    print("Thinking...")
    
    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        
        response_text = response["messages"]["content"]
        return response_text
    except Exception as e:
        return "Sorry, something went wrong while thinking."
    
def speak(text: str):
    if not text:
        return
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)
            
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        print(f"An error occurred in speak(): {e}")
        
st.title("AI voice Assistant")
st.write("Click the button and speak")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if st.button("Speak"):
    user_input = listen()
    
    if user_input:
        st.write(f"YOU: {user_input}")
        ai_response = think(user_input)
        st.write(f"AI: {ai_response}")
        speak(ai_response)
        st.session_state.chat_history.append("YOU", user_input)
        st.session_state.chat_history.append("AI", ai_response)
        
st.subheader("Conversation History")
for role, message in st.session_state.chat_history:
    st.write(f"{role}: {message}")