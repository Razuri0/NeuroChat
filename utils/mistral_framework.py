import os
from mistralai import Mistral

def mistral_completion(api, messages, model, max_tokens, pre_prompt):
    # Initialize the client
    client = Mistral(api_key=api)

    # In v2.x, messages should be a list of objects/dicts. 
    # If pre_prompt is a string, wrap it as a system message.
    # If it's already a list, concatenate them.
    if isinstance(pre_prompt, str):
        full_messages = [{"role": "system", "content": pre_prompt}] + messages
    else:
        full_messages = pre_prompt + messages

    # The method remains client.chat.complete, but v2.0.0 
    # has stricter validation on parameter types.
    response = client.chat.complete(
        model=model,
        messages=full_messages,
        max_tokens=max_tokens
    )

    # Response parsing remains similar
    return response.choices[0].message.content