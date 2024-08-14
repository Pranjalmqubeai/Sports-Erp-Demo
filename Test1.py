import streamlit as st
import openai
from docx import Document
import os
# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the contract template from the .docx file


# Function to call the OpenAI API
def chatgpt_api_call(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4o-2024-08-06",
        messages=messages
    )
    return response['choices'][0]['message']['content']

# Function to format messages
def format_message(role, content):
    return {"role": role, "content": content}

def main():
    st.title("Mqube Football Player Contract Generator")
    st.write("Interact with the MQube AI to create a custom football player contract.")

    # Replace with your logo path or URL
    mqube_logo = "mqube_logo.png"  # Path to the MQube logo

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.session_state.messages == []:
        # Start the conversation with the initial system prompt
        initial_prompt = f"""
        You are a legal advisor for Fenerbahçe Futbol A.Ş., a Turkish football club in the Süper Lig. Your role is to generate legally compliant player contracts in accordance with the latest FIFA and Turkish Football Federation regulations.

        When a user indicates they want to create a player contract, proceed by asking the following questions one by one:

        1. Name of the player: Please enter the full name of the player.
        2. Nationality of the player: What is the player's nationality?
        3. Passport number: Could you provide the player's passport number?
        4. Address and email: Please enter the player's residential address and email address.
        5. Contract start date: When does the contract begin?
        6. Contract end date: When does the contract end?
        7. Contract signature date: On what date will the contract be signed?
        8. Guarantee fee information: Please provide the guarantee fee information season by season.
        9. Attendance fee: What is the attendance fee for the player?
        10. Bonus: Specify any bonuses the player will receive.
        11. Signing-on fee: What is the signing-on fee for the player?
        12. Other benefits: Are there any other benefits included in the contract?

        Once all the details are gathered, generate a Word document with the full contract, ensuring that all provided inputs are integrated into the template. Use the following contract template as the format for generating the final contract document:

        
        """
        st.session_state.messages.append(
            format_message("system", initial_prompt))

    # Display conversation (only user and assistant messages)
    for message in st.session_state.messages[1:]:  # Skip the system message
        if message['role'] == 'assistant':
            st.chat_message("MQube", avatar=mqube_logo).write(
                message['content'],
                unsafe_allow_html=True,
                style="background-color: #E0F7FA; padding: 10px; border-radius: 5px;"
            )
        else:
            st.chat_message("You").write(message['content'])

    # User input
    user_input = st.chat_input("Your input")

    if user_input:
        st.session_state.messages.append(format_message("user", user_input))

        # Get the response from ChatGPT
        assistant_response = chatgpt_api_call(st.session_state.messages)

        # Add the assistant's response to the messages
        st.session_state.messages.append(
            format_message("assistant", assistant_response))

        # Refresh the page to display the new message
        st.experimental_rerun()

if __name__ == "__main__":
    main()