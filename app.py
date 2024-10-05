import streamlit as st
import os
import base64
from groq import Groq

# Set up the page title and icon
st.set_page_config(page_title="Medicine Analysis & LLM Assistant", page_icon="💊")

# Define a function to encode an image in base64 format
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        st.error(f"Error encoding image: {e}")
        return None

# Initialize Groq client with API key from environment variable
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.warning("Please set the 'GROQ_API_KEY' environment variable.")
else:
    client = Groq(api_key=api_key)

# Streamlit UI Design
st.title("💊 Medicine Analysis & LLM Assistant")

# Initialize session state variables
if "image_analysis_result" not in st.session_state:
    st.session_state.image_analysis_result = ""
if "image_uploaded" not in st.session_state:
    st.session_state.image_uploaded = False

# Image Analysis Section
st.header("🔍 Medicine Strip Analysis")
uploaded_file = st.file_uploader("Upload a medicine strip image (backside)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Save the uploaded file temporarily
    image_path = f"temp_{uploaded_file.name}"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Display uploaded image
    st.image(image_path, caption="Uploaded Image", use_column_width=True)

    # Encode the image
    base64_image = encode_image(image_path)
    
    # Analyze the image if not already analyzed
    if base64_image and not st.session_state.image_uploaded:
        with st.spinner("Analyzing the image..."):
            try:
                # Call LLaVA model for image analysis
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Find the medicine name, manufacture date, and expiry date."},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}",
                                    },
                                },
                            ],
                        }
                    ],
                    model="llava-v1.5-7b-4096-preview",
                )
                
                # Capture and store the image analysis result in session state
                st.session_state.image_analysis_result = chat_completion.choices[0].message.content
                st.session_state.image_uploaded = True  # Mark image as analyzed
                
            except Exception as e:
                st.error(f"Error during image analysis: {e}")
        # Remove the temporary file after analysis
        os.remove(image_path)
    else:
        st.info("Image analysis already completed.")

    # Display the stored image analysis result
    # st.subheader("Image Analysis Result:")
    # st.write(st.session_state.image_analysis_result)

# Text Analysis Section
st.header("📝 Language Model Assistant")

# User Input for Age
age = st.text_input("Enter your age", "")

# User Input for Gender
gender = st.selectbox("Select your gender", ["Select", "Male", "Female", "Other"])

# Multi-select for Medical Conditions
medical_conditions = st.multiselect(
    "Select your medical conditions (you can choose multiple)", 
    ["None", "Diabetes", "Hypertension", "Asthma", "Allergies", "Heart Disease", "Kidney Disease"]
)

# User Input Query
user_query = st.text_area("Enter your query (e.g., Can I take this medicine with my current condition?):")

# Combine structured data into a single query
if st.button("Submit Query"):
    if user_query.strip() and age.isdigit() and gender != "Select" and st.session_state.image_analysis_result:
        # Construct the structured input including the image analysis result
        structured_input = f"User Info:\n- Age: {age}\n- Gender: {gender}\n- Medical Conditions: {', '.join(medical_conditions) if medical_conditions else 'None'}\n\nMedicine Analysis:\n{st.session_state.image_analysis_result}\n\nUser Query: {user_query}"
        
        with st.spinner("Processing your query..."):
            try:
                # Call LLaMA model for text analysis
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a medical assistant. The user will provide their medicine name, expiry date, user age, gender, and medical conditions. You should suggest whether they can consume this medicine or not. You should not ask any other questions.use very simple words so user can understand easily"},
                        {
                            "role": "user",
                            "content": structured_input,
                        }
                    ],
                    model="llama3-8b-8192",
                )
                
                # Display the text analysis result
                st.subheader("LLM Response:")
                st.write(chat_completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Error during text analysis: {e}")
    else:
        if not st.session_state.image_analysis_result:
            st.warning("Please complete the image analysis first.")
        else:
            st.warning("Please fill in all fields (age, gender, and query) to submit.")

# Footer
st.markdown("---")

