import streamlit as st
import google.generativeai as genai

st.title("🏸 Athlete Badminton Coaching Chatbot")
st.subheader("Conversation")

# Capture Gemini API Key
gemini_api_key = st.text_input("Gemini API Key:", placeholder="Type your API Key here...", type="password")

# Initialize the Gemini Model
model = None
if gemini_api_key:
    try:
        # Configure Gemini with the provided API Key
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")

# Initialize session state for storing chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize with an empty list

# Extra Features: Dropdown for predefined topics and radio buttons for coaching level
st.sidebar.title("Chatbot Settings")
selected_topic = st.sidebar.selectbox(
    "Select a badminton topic:",
    ("General Coaching", "Footwork Techniques", "Racket Skills", "Fitness and Conditioning", "Shuttlecock Control")
)

coaching_level = st.sidebar.radio(
    "Select coaching level:",
    ("Beginner", "Intermediate", "Advanced")
)

# Display examples of what users can ask
st.sidebar.markdown("### Example Questions")
st.sidebar.write("- How do I improve my footwork?")
st.sidebar.write("- What are the best racket string tensions?")
st.sidebar.write("- How can I increase my shuttlecock speed?")
st.sidebar.write("- Tips for beginner badminton drills?")
st.sidebar.write("- How to recover after a badminton match?")

# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# Define a function to check if the user's input is related to badminton
def is_badminton_related(user_input):
    badminton_keywords = ["badminton", "shuttlecock", "racket", "footwork", "smash", "net play", "drills", "serve", "clear", "drop shot", "coaching"]
    return any(keyword in user_input.lower() for keyword in badminton_keywords)

# Capture user input and generate bot response
if user_input := st.chat_input("Type your message here..."):
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    # Check if the query is related to badminton
    if not is_badminton_related(user_input):
        bot_response = (
            "I specialize in badminton coaching. Here are some topics I can help with:\n"
            "- Footwork techniques\n"
            "- Racket skills and maintenance\n"
            "- Shuttlecock control and speed\n"
            "- Badminton drills for all levels\n"
            "Please ask me something related to these topics!"
        )
    else:
        # Use Gemini AI to generate a bot response
        if model:
            try:
                response = model.generate_content(f"Badminton {selected_topic} for {coaching_level}")
                bot_response = response.text

                # Store and display the bot response
                st.session_state.chat_history.append(("assistant", bot_response))
                st.chat_message("assistant").markdown(bot_response)
            except Exception as e:
                st.error(f"An error occurred while generating the response: {e}")
        else:
            bot_response = "The chatbot is not yet configured with a valid API key."

    # Store and display the bot response if not already handled
    st.session_state.chat_history.append(("assistant", bot_response))
    st.chat_message("assistant").markdown(bot_response)
