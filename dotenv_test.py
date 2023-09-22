from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r'C:\Users\Master\PycharmProjects\api.env')

new_var = os.getenv('DALLE_API')

print(new_var)