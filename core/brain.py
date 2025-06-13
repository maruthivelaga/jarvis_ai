from openai import OpenAI
client = OpenAI(api_key="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")

def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4"
        messages=[
            {"role": "system", "content": "You are a helpful personal assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content