import os
import openai
api = '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'


import openai

openai.api_key = api


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a cat"},
            {"role": "user", "content": "скажи щось розумне одним реченням"},
        ]
)

result = ''
for choice in response.choices:
    result += choice.message.content

print(result)