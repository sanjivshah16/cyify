import streamlit as st
from openai import OpenAI
import os

# Initialize session state
if 'transformed_text' not in st.session_state:
    st.session_state.transformed_text = ""
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# Page configuration
st.set_page_config(page_title="CYify Text Transformer", layout="wide")
st.title("CYify Text Transformer")

# Secure API key handling - check multiple sources
api_key = None

# 1. Check environment variables (for non-Streamlit hosting)
if os.environ.get('OPENAI_API_KEY'):
    api_key = os.environ.get('OPENAI_API_KEY')
    st.sidebar.success("Using API key from environment variables")

# 2. Check Streamlit secrets (for Streamlit Cloud)
elif 'OPENAI_API_KEY' in st.secrets:
    api_key = st.secrets['OPENAI_API_KEY']
    st.sidebar.success("Using API key from secrets")

# 3. If no API key found, ask the user
else:
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input("Enter your OpenAI API key", type="password")
        st.caption("Your API key is needed to use the OpenAI service")
        st.info("Get your API key from https://platform.openai.com/api-keys")

# Rest of your app remains the same...

# Main content
st.write("Transform your text into flowery, emotionally expressive writing with dramatic single-word lines.")

# Text input area that updates session state
def update_input():
    st.session_state.input_text = st.session_state.text_area_input

user_text = st.text_area(
    "Your text:",
    value=st.session_state.input_text,
    height=200,
    placeholder="Enter your text here...",
    key="text_area_input",
    on_change=update_input
)

# Function to clear inputs
def clear_inputs():
    st.session_state.input_text = ""
    st.session_state.transformed_text = ""
    st.rerun()

if st.button("Clear", on_click=clear_inputs):
    pass

# Function to call OpenAI API
def transform_text(text, api_key):
    if not text:
        return "", "Please enter some text to transform."

    if not api_key:
        return "", "Please enter your OpenAI API key in the sidebar."

    try:
        # Initialize OpenAI client with new API format
        client = OpenAI(api_key=api_key)

        # Create a simple, direct prompt for the API
        system_prompt = f"""You are a creative writing assistant that transforms text into flowery, emotionally expressive messages with dramatic single words on their own lines. Use this text as inspiration:"
        Every emotion you have is justifiable and correct-
        Confusion
        Frustration
        Anger
        Exasperation
        I understand.
        Too many admin folk and too much uncertainty about prolific investigators on the CE tract. The comp plan is antiquated and fails to reward the intangible value that so many bring to the table.
        I've interceded on your behalf. Within days, I am told this will be done. I've been up and down the chain on this.
        The clumsiness is entirely administrative and not anything at all about the assessment of you and your work.
        You are a world class talent and the heir for this Chief job and leading candidate almost by default for any other Chief job. And it doesn't stop there as Chair of Medicine is next if you wish.
        My job is to best enable your success and scrub away the noise that enters your world.
        I will continue to constantly work on your behalf.
        """
        user_prompt = f"""
        Transform this text into a flowery, emotionally expressive style with random single words on their own lines.
        Use over-the-top emotion while preserving the original meaning.
        Follow the style of the example where 5 words appear at the top of the revised text on separate lines, single spaced before the rest of the text.
        Each one word line should end in a period.
        Only 5 one-word lines at the top. The rest of the text should not have any 1 word lines unless they are headings for subsequent text.
        Original text:
        {text}
        """

        # Call the OpenAI API with the new client format
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=1.0,
            max_tokens=1000
        )

        # Extract the transformed text using the new response format
        transformed_text = response.choices[0].message.content.strip()
        return transformed_text, None

    except Exception as e:
        return "", f"Error: {str(e)}"

# Function to handle transformation and update session state
def handle_transform():
    text = st.session_state.input_text
    if text:
        with st.spinner("Transforming your text..."):
            transformed_text, error = transform_text(text, api_key)

            if error:
                st.error(error)
            else:
                st.session_state.transformed_text = transformed_text
    else:
        st.warning("Please enter some text to transform.")

# Button to transform text
if st.button("Transform Text", on_click=handle_transform):
    pass

# Display transformed text if available
if st.session_state.transformed_text:
    st.subheader("Transformed Text:")
    with st.container():
        st.text_area(
            "",
            value=st.session_state.transformed_text,
            height=300,
            key="output_area"
        )

        # Add download button - now using session state
        st.download_button(
            label="Download Transformed Text",
            data=st.session_state.transformed_text,
            file_name="emotional_text.txt",
            mime="text/plain",
            key="download_button"
        )

# Footer
st.markdown("---")
