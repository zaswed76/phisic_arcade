

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

    print(aichat("скажи щось смішне одним реченням"))