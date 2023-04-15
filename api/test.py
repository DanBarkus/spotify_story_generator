import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [{"role": "user", "content": "give me 5 random words, but only return one word per message. Only return the random word, no other words"}]

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
output = completion.choices[0].message.content

print("first word " + output)

for i in range(2,6):
    messages.append({"role": "assistant", "content": output})

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    output = completion.choices[0].message.content

    print(f"{i} word " + output)
