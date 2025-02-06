import streamlit as st
from PIL import Image
import io
import os
from Image_embedding import image_files , folder , get_images , get_images_by_text
from information import generate_information
import re
import sys
from gtts import gTTS
from io import BytesIO


# Ensure UTF-8 output in Windows terminal
sys.stdout.reconfigure(encoding="utf-8")
# Set the app title

languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Russian": "ru",
    "Arabic": "ar",
    "Hindi": "hi",
    "Portuguese": "pt",
    "Japanese": "ja",
    "Korean": "ko",
    "Swahili": "sw",
    "Tamil": "ta",
    "Bengali": "bn",
    "Thai": "th",
    "Hebrew": "he",
    "Persian": "fa",
    "Dutch": "nl",
    "Greek": "el",
    "Turkish": "tr",
    "Vietnamese": "vi",
    "Basque": "eu",
    "Welsh": "cy",
    "Maori": "mi",
    "Zulu": "zu",
    "Icelandic": "is",
    "Pashto": "ps",
    "Serbian": "sr",
    "Yoruba": "yo"
}

st.title("AnimalVision : See Hear Learn About Any Creature Instantly")

# Create a sidebar for input selection
input_type = st.sidebar.radio("Select Input Type:", ["Text", "Image"])

if input_type == "Text":
    # Text input section
    st.header("Find Your Creature")
    num_images = st.number_input(
                "Enter the number of images to display (1-7):",
                  min_value=1,
                  max_value=7,
                  value=1,  # Default value
                  step=1
                    )
    user_text = st.text_area("Want to discover more about a creature? Upload the name, and let's explore! :")
    st.title("Select a Language")
    selected_language = st.selectbox("Select the language:", list(languages.keys()))
    if st.button("Submit Text"):
        if user_text:
            # Finding name of animal
            user_text = user_text.capitalize()
            ids , name_of_animal= get_images_by_text(user_text ,num_images)
           

            # Finding the information of living thing.
            
            info_of_thing = generate_information(user_text , selected_language)
            digits = re.findall(r"\d", info_of_thing)
            info_list = re.split(r'[-\d]+', info_of_thing)
            # info_list = [part.split('\\') for part in info_list]

            # Clean up the points to remove leading/trailing whitespace
            info_list = [point.strip() for point in info_list if point.strip()]

            # Create the HTML for the bulleted list
            markdown_text = "<ul style='list-style-type: disc; padding-left: 20px;'>"
            for point in info_list:
                markdown_text += f"<li>{point}</li>"
            markdown_text += "</ul>"


            desired_size = (250, 200)
            cols = st.columns(2)
            for i, img_id in enumerate(ids):
               col = cols[i % 2]
               image_path = os.path.join(folder, image_files[img_id])
               try:
                 img = Image.open(image_path)
                 img_resized = img.resize(desired_size)
                 col.image(img_resized , use_container_width=True)

                 
               except FileNotFoundError:
                 col.text(f"Image {img_id} not found")

            st.markdown(
                          f"""
                          <div style="
                              border: 1px solid green;
                              padding: 5px;
                              border-radius: 5px;
                              background-color: Lightgreen;
                              color : black ;
                              font-weight: bold;  
                              font-size: 30px; 
                              width: 100%;  
                              height: 50px;  
                              margin: auto;
                              text-align: center;  
                              display: flex;  
                              justify-content: center; 
                              align-items: center; 
                          ">
                              So , you are looking for  : {user_text}
                          </div>
                          """,
                          unsafe_allow_html=True,
                      )    
            st.markdown(
                          f"""
                          <div style="
                              border: 5px solid green;
                              padding: 5px;
                              border-radius: 5px;
                              background-color: #0e9553;
                              color : black ;
                              font-weight: bold;  
                              font-size: 30px; 
                              text-align: center;  
                              display: flex;  
                              justify-content: center; 
                              align-items: center; 
                          ">
                              Enjoy with the knowledge  : 
                          </div>
                          """,
                          unsafe_allow_html=True,
                      )     
            st.markdown(
                          f"""
                          <div style="
                              border: 1px solid green;
                              padding: 5px;
                              border-radius: 5px;
                              background-color: Lightgreen;
                              color : black ;
                              font-size: 20px; 
                              display: flex;  
                              justify-content: center; 
                              align-items: center; 
                          ">
                              {markdown_text}
                          </div>
                          """,
                          unsafe_allow_html=True,
                      )
   
            # Join the list of strings into a single string
            st.divider()        
            info_text = " ".join(info_list)


            # Get the language code
            lang_code = languages[selected_language]

            with st.spinner("🎙️ Audio is generating... Please wait."):
              # Convert text to speech
                tts = gTTS(text=info_text, lang=lang_code, slow=False)

                 # Save the audio to a BytesIO object
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)

               # Show success message and display audio player
                st.success("✅ Audio generated successfully!")
                st.audio(audio_bytes, format="audio/mp3")
               
    
elif input_type == "Image":
    
    # Image input section
    st.header("Image Input")
    num_images = st.number_input(
    "Enter the number of images to display (1-7):",
      min_value=1,
      max_value=7,
      value=1,  # Default value
      step=1
        )
    uploaded_image = st.file_uploader("Curious about a creature? Upload its image, and we'll reveal its secrets!", type=["jpg", "jpeg", "png"])
    st.title("Select a Language")
    selected_language = st.selectbox("Select the language:", list(languages.keys()))
    
    # Finding name of animal
    ids , name_of_animal= get_images(uploaded_image ,num_images)
    base_name = re.sub(r'\.[a-zA-Z0-9]+$', '', name_of_animal)
    # Remove all non-alphabetic characters
    base_name = re.sub(r'[^a-zA-Z]', '', base_name)
    name_of_animal = base_name.capitalize()

    # Finding the information of living thing.
    
    info_of_thing = generate_information(name_of_animal , selected_language )
    info_list = info_of_thing.split('-')

    # Clean up the points to remove leading/trailing whitespace
    info_list = [point.strip() for point in info_list if point.strip()]

    # Create the HTML for the bulleted list
    markdown_text = "<ul style='list-style-type: disc; padding-left: 20px;'>"
    for point in info_list:
        markdown_text += f"<li>{point}</li>"
    markdown_text += "</ul>"
    if uploaded_image is not None:
        try:
            # # Open and display the uploaded image
            # image = Image.open(uploaded_image)
            # st.image(image, caption="Uploaded Image", use_column_width=True)
            st.success("Image uploaded successfully!")
           
            desired_size = (250, 200)
            cols = st.columns(2)
            for i, img_id in enumerate(ids):
               col = cols[i % 2]
               image_path = os.path.join(folder, image_files[img_id])
               try:
                 img = Image.open(image_path)
                 img_resized = img.resize(desired_size)
                 col.image(img_resized , use_container_width=True)

                 
               except FileNotFoundError:
                 col.text(f"Image {img_id} not found")

            st.markdown(
                          f"""
                          <div style="
                              border: 1px solid green;
                              padding: 5px;
                              border-radius: 5px;
                              background-color: Lightgreen;
                              color : black ;
                              font-weight: bold;  
                              font-size: 30px; 
                              width: 100%;  
                              height: 50px;  
                              margin: auto;
                              text-align: center;  
                              display: flex;  
                              justify-content: center; 
                              align-items: center; 
                          ">
                              So , you are looking for  : {name_of_animal}
                          </div>
                          """,
                          unsafe_allow_html=True,
                      )    
            st.markdown(
                          f"""
                          <div style="
                              border: 5px solid green;
                              padding: 5px;
                              border-radius: 5px;
                              background-color: #0e9553;
                              color : black ;
                              font-weight: bold;  
                              font-size: 30px; 
                              text-align: center;  
                              display: flex;  
                              justify-content: center; 
                              align-items: center; 
                          ">
                              Enjoy with the knowledge  : 
                          </div>
                          """,
                          unsafe_allow_html=True,
                      )     
            st.markdown(
                          f"""
                          <div style="
                              border: 1px solid green;
                              padding: 5px;
                              border-radius: 5px;
                              background-color: Lightgreen;
                              color : black ;
                              font-size: 20px; 
                              display: flex;  
                              justify-content: center; 
                              align-items: center; 
                          ">
                              {markdown_text}
                          </div>
                          """,
                          unsafe_allow_html=True,
                      )
             # Join the list of strings into a single string
            st.divider()        
            info_text = " ".join(info_list)


            # Get the language code
            lang_code = languages[selected_language]

            with st.spinner("🎙️ Audio is generating... Please wait."):
              # Convert text to speech
                tts = gTTS(text=info_text, lang=lang_code, slow=False)

                 # Save the audio to a BytesIO object
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)

               # Show success message and display audio player
                st.success("✅ Audio generated successfully!")
                st.audio(audio_bytes, format="audio/mp3")
               
               
        except Exception as e:
            st.error(f"Error loading image: {e}")
    else:
        st.info("Please upload an image file.")
