from openai import OpenAI


pre_prompt_default = [{"role": "user", "content": "write the shortest possible answer in every response"}, {"role": "assistant", "content": "k"}]


def GPT_completion(messages, API, model="gpt-5-nano", temperature=0.8, n=1, max_tokens=1000, pre_prompt=pre_prompt_default):
    prompt = pre_prompt + messages
    client = OpenAI(api_key=API)

    completion = client.responses.create(
        model=model,
        input=prompt,
        reasoning={
            "effort": "minimal",
        },
        text={
            "verbosity": "low",
        },
        max_output_tokens=max_tokens,
    )
    
    return completion


if __name__ == "__main__":
    API = "openai_api_key"
    conversation = []
    AI_model = "gpt-5-nano"
    while True:
        message = [{"role": "user", "content": input("Input: ")}]
        completion = GPT_completion(message, API, AI_model).output_text
        answer = [{"role": "assistant", "content": completion}]
        print(f'\n {AI_model}: {answer[0]["content"]} \n')
