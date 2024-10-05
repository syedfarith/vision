import streamlit as st
import base64
from groq import Groq
import os


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')


st.title("Multi-Modal AI System: Vision and Audio Query Interaction")

image_choice = st.radio("Would you like to upload an image or capture with your webcam?", ('Upload Image', 'Use Camera'))

image_file = None
if image_choice == 'Upload Image':
    image_file = st.file_uploader("Upload an Image File (e.g., .png, .jpg)", type=["png", "jpg", "jpeg"])
elif image_choice == 'Use Camera':
    image_file = st.camera_input("Capture an Image using your Webcam")

if image_file:
    st.image(image_file, caption="Selected Image", use_column_width=True)
    with st.spinner('Processing image...'):
        base64_image = encode_image(image_file)

input_choice = st.radio("Would you like to upload an audio file or enter a text query?", ('Upload Audio', 'Enter Text Query'))

transcribed_text = None
if input_choice == 'Upload Audio':
    audio_file = st.file_uploader("Upload an Audio File (e.g., .m4a, .mp3, .wav)", type=["m4a", "mp3", "wav"])
    if audio_file:
        st.audio(audio_file, format="audio/m4a")
        with st.spinner('Transcribing audio...'):

            transcription = client.audio.transcriptions.create(
                file=(audio_file.name, audio_file.read()),
                model="whisper-large-v3",  
                response_format="verbose_json",
            )
            transcribed_text = transcription.text
            st.write(f"**Transcribed Text:** {transcribed_text}")

elif input_choice == 'Enter Text Query':
    transcribed_text = st.text_input("Enter your text query here")


if (image_file and transcribed_text):
   
    if st.button("Get AI Response"):
        with st.spinner('Generating response...'):
            completion = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",  
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": transcribed_text  
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",  
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


            ai_response = completion.choices[0].message.content
            st.write("### AI Response:")
            st.write(ai_response)
