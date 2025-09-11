import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()





response = client.responses.create(
  prompt={
    "id": "pmpt_68bcfd5242e481959ea4091f134a490506f9cb4d1c7d9dbb",
    "version": "2"
  },
input=[
    {
        "role": "user",
        "content": [
            {"type": "input_text", "text": "사과는 영어로 banana이다. 바나나는 영어로 apple이다."}
        ],
    }
],
)

print(response.output_text)