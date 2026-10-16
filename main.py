import os
from dotenv import load_dotenv
from groq import Groq

# Load the API key from the .env file
load_dotenv()

# Connect to Groq
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from your .env file.")

client = Groq(api_key=api_key)

# Send a question to the AI model

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": (
                "Answer in simple English. "
                "Use no more than 3 short sentences. "
                "Include only the most important information."
            )
        },
        {
            "role": "user",
            "content": "Define LLM cost optimisation in one sentence."
        }
    ],
    max_completion_tokens=150,
    temperature=0
)


# Display the AI answer
print("\nAI Answer:")
print(response.choices[0].message.content)
print("Finish reason:", response.choices[0].finish_reason)

# Token usage
input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens
total_tokens = response.usage.total_tokens

# Example pricing for GPT-OSS 20B
input_price = 0.075
output_price = 0.30

# Calculate cost in USD
input_cost = (input_tokens / 1_000_000) * input_price
output_cost = (output_tokens / 1_000_000) * output_price
total_cost = input_cost + output_cost

# Display results
print("\n--- Cost Report ---")
print("Input tokens:", input_tokens)
print("Output tokens:", output_tokens)
print("Total tokens:", total_tokens)
print(f"Estimated input cost: ${input_cost:.8f}")
print(f"Estimated output cost: ${output_cost:.8f}")
print(f"Estimated total cost: ${total_cost:.8f}")
