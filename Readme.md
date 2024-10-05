Description
This project is a multi-modal AI system that integrates vision model and Large language Model (LLM) to provide an interactive experience for users. The system allows users to upload an image or capture one via a webcam and either upload an audio file or enter a text-based query about the image. The AI processes both the image and the query and generates a context-aware response.



Live Demo
🔗 https://vision-with-audio.streamlit.app/

Click the link above to try out the live version of the project.

Features
Image Input Options: Users can either upload an image file or capture one using their webcam.

Audio Query: Users can upload an audio file which will be transcribed into text using Whisper.

Text Query: Users can directly enter text queries about the image.

AI Response: The system generates a response based on both the image and the query using a powerful AI model.

Interactive UI: Built with Streamlit, providing an easy-to-use interface for image and audio processing.


Technologies Used

Streamlit – For creating the interactive user interface.

Groq API – Used for AI-based multi-modal processing (Vision and Audio models).

Whisper Model – For speech-to-text transcription of uploaded audio files.

Llama-3.2 Vision Model – For AI-driven response generation based on visual and textual data.

Python – For backend logic and processing.


How to Use

Image Input:

Choose to upload an image file (.png, .jpg) or use your webcam to capture a photo.

Audio or Text Input:

You can upload an audio file (.m4a, .mp3, .wav) or enter a text query directly.

AI Response:

Click the "Get AI Response" button to see the generated response, which will combine the image and your query for a meaningful reply.



Future Enhancements
Real-Time Audio Capture: Add functionality for recording audio directly from the browser without file uploads.

Support for Video Input: Enable video input for more dynamic query interactions.

Enhanced AI Capabilities: Improve the model's ability to handle more complex image queries.

