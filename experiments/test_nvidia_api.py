import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

completion = client.chat.completions.create(
    model="nvidia/nvidia-nemotron-nano-9b-v2",
    messages=[{"role": "user", "content": "What is 2+2?"}],
    temperature=0.6,
    top_p=0.95,
    max_tokens=2048,
    frequency_penalty=0,
    presence_penalty=0,
    stream=False,
    extra_body={
        "min_thinking_tokens": 1024,
        "max_thinking_tokens": 2048
    }
)

reasoning = getattr(completion.choices[0].message, "reasoning_content", None)
if reasoning:
    print("Reasoning:")
    print(reasoning)
    print("\n" + "="*50 + "\n")

print("Response:")
print(completion.choices[0].message.content)
