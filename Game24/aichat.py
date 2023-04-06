

api = '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'


import openai

openai.api_key = api

def aichat(key):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": "You are a bot"},
                        {"role": "user", "content": key},])
            result = ""
            for choice in response.choices:
                result += choice.message.content
            return result
if __name__ == "__main__":

    print(aichat("скільки буде три плюс 3"))