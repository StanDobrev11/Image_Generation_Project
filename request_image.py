from dotenv import load_dotenv
import openai
import os

# import API key load_dotenv() stating path to file for authentications
load_dotenv(dotenv_path=r'C:\Users\Master\PycharmProjects\api.env')
openai.api_key = os.getenv('DALLE_API')

# this is the response from the API
# response = openai.Image.create(
#     prompt="",
#     n=1,
#     size="256x256"  # 256x 512x 1024x
# )
# image_url = response['data'][0]['url']

image_url = ('working')

