import streamlit as st
import base64
from groq import Groq
import os

# Initialize Groq client with your API key from environment variables
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Function to encode the image into base64 format
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# Streamlit App Title
st.title("Multi-Modal AI System: Vision and Audio Query Interaction")

# Let the user choose whether to upload an image or use the camera
image_choice = st.radio("Would you like to upload an image or capture with your webcam?", ('Upload Image', 'Use Camera'))

# Image input based on user choice
image_file = None
if image_choice == 'Upload Image':
    image_file = st.file_uploader("Upload an Image File (e.g., .png, .jpg)", type=["png", "jpg", "jpeg"])
elif image_choice == 'Use Camera':
    image_file = st.camera_input("Capture an Image using your Webcam")

if image_file:
    st.image(image_file, caption="Selected Image", use_column_width=True)
    with st.spinner('Processing image...'):
        # Encode the image as base64
        base64_image = encode_image(image_file)

# Let the user choose whether to upload an audio file or enter a text query
input_choice = st.radio("Would you like to upload an audio file or enter a text query?", ('Upload Audio', 'Enter Text Query'))

# Audio or text input based on user choice
transcribed_text = None
if input_choice == 'Upload Audio':
    audio_file = st.file_uploader("Upload an Audio File (e.g., .m4a, .mp3, .wav)", type=["m4a", "mp3", "wav"])
    if audio_file:
        st.audio(audio_file, format="audio/m4a")
        with st.spinner('Transcribing audio...'):
            # Send audio file for transcription
            transcription = client.audio.transcriptions.create(
                file=(audio_file.name, audio_file.read()),
                model="whisper-large-v3",  # Use Whisper model for audio transcription
                response_format="verbose_json",
            )
            transcribed_text = transcription.text
            st.write(f"**Transcribed Text:** {transcribed_text}")

elif input_choice == 'Enter Text Query':
    transcribed_text = st.text_input("Enter your text query here")

# Only proceed if both image and audio/text input are provided
if (image_file and transcribed_text):
    # Button to trigger the interaction with the AI model
    if st.button("Get AI Response"):
        with st.spinner('Generating response...'):
            # Send both the transcribed text and the encoded image to Groq's model
            completion = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",  # Vision model to understand image and text
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": transcribed_text  # Audio transcription or text input as query
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",  # Encoded image
                                }
                            }
                        ]
                    }
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )

            # Output the response generated from the model
            ai_response = completion.choices[0].message.content
            st.write("### AI Response:")
            st.write(ai_response)
