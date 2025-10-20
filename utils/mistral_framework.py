import os
from mistralai import Mistral

def mistral_completion(api, messages, model, max_tokens, pre_prompt):
    prompt = pre_prompt + messages
    client = Mistral(api_key=api)
    response = client.chat.complete(
        model=model,
        messages=prompt,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content