import os
from mistralai import Mistral

def mistral_completion(api, messages, model="mistral-small-2407", max_tokens=100):
    client = Mistral(api_key=api)
    response = client.chat.completions.create(
        model=model,
        messages=
        messages,
        max_tokens=max_tokens
    )
    return response.choices[0].message['content']


def main():
    with open("../mistral_key", "r") as file:
        mistral_key = file.read().strip()
    prompt = "test"
    messages = [{"role": "user", "content": prompt}]
    response = mistral_completion(messages=messages, api=mistral_key)
    print(f'Mistral: {response}\n')

main()