import os
from mistralai import Mistral

def mistral_completion(api, messages, model="mistral-small-2407", max_tokens=100):
    client = Mistral(api_key=api)
    response = client.chat.complete(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content