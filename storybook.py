import os
import time

import streamlit as st
from openai import OpenAI

my_secret = st.secrets('OPENAI_API_KEY')
#my_secret = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=my_secret)

#story generator method
def story_gen(prompt):
  system_prompt = """
  You are a girl who loves to fantasize. 
  You will be given a concept to generate a story
  and you will generate a story suitable for teenage dreams.
  """

  response = client.chat.completions.create(
      model = 'gpt-4o-mini', 
      messages = [
          {"role" : "system",
           "content" : system_prompt},
           {"role" : "user",
            "content" : prompt
           }
      ],
      temperature = 1.3,
      max_tokens = 200
)

  return response.choices[0].message.content

#image generator method 
def image_gen(prompt):
  response = client.images.generate(
      model = 'dall-e-2',
      prompt = prompt,
      size = '1024x1024',
      quality = 'standard',
      n = 1
  )

  return response.data[0].url

  return response.choices[0].message.content

#cover prompt generator method
def cover_gen(prompt):
  system_prompt = """
  Generate a prompt for a cover art 
  that is suitable and shows off the story themes. The prompt will be sent to dall-e-2. 
  """
  response = client.chat.completions.create(
        model = 'gpt-4o-mini', 
        messages = [
            {"role" : "system",
            "content" : system_prompt},
            {"role" : "user",
              "content" : prompt
            }
        ],
        temperature = 1.3,
        max_tokens = 100
  )
  return response.choices[0].message.content

#storybook method
def storybook_gen(prompt):
  story = story_gen(prompt)
  cover = cover_gen(story)
  image = image_gen(cover)
  st.write(image)
  st.write(story)

 
st.title("Storybook Generator for kids for fun")
st.divider()

prompt = st.text_area("Enter your story concept:")

if st.button("Genarate Storybook"):
  with st.spinner("Please wait.."):
    story = story_gen(prompt)
    cover = cover_gen(story)
    image = image_gen(cover)
    time.sleep(5) 
    st.balloons()
    st.snow()
    st.image(image)
    st.write(story)