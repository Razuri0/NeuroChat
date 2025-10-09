import os
from mistralai import Mistral

def mistral_completion(api, messages, model="mistral-small-2407", max_tokens=100):
    client = Mistral()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": messages}
        ],
        max_tokens=max_tokens
    )
    return response.choices[0].message['content']


if __name__ == "__main__":
    messages = [{"role": "user", "content": prompt}]
    response = mistral_completion(messages=messages, api=os.getenv("MISTRAL_API_KEY"))
    print(f'Mistral: {response}\n')