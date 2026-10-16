import csv
import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is missing from your .env file.")

client = Groq(api_key=api_key)
MODEL = "openai/gpt-oss-20b"

# Load the fixed evaluation questions
with open("evaluation_cases.csv", "r", newline="", encoding="utf-8") as file:
    test_cases = list(csv.DictReader(file))

results = []
EXPERIMENT_NAME = "token_limit"


for case in test_cases:
    print(f"\nRunning test {case['id']}: {case['question']}")

    start_time = time.perf_counter()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
    {
        "role": "system",
        "content": (
            "Answer each question in one concise sentence. "
            "Keep the answer accurate and include essential information only."
        )
    },
    {"role": "user", "content": case["question"]}
],
max_completion_tokens=200,
temperature=0
    )

    latency = time.perf_counter() - start_time
    answer = response.choices[0].message.content or ""
    usage = response.usage

    result = {
        "experiment": EXPERIMENT_NAME,
        "id": case["id"],
        "question": case["question"],
        "expected_answer": case["expected_answer"],
        "answer": answer,
        "input_tokens": usage.prompt_tokens,
        "output_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
        "latency_seconds": round(latency, 3),
        "finish_reason": response.choices[0].finish_reason
    }

    results.append(result)

    print("Answer:", answer)
    print("Input tokens:", usage.prompt_tokens)
    print("Output tokens:", usage.completion_tokens)
    print("Time:", round(latency, 3), "seconds")

# Save the baseline results
with open("token_limit_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\nToken limit experiment completed.")
print("Results saved to token_limit_results.csv")
print("Questions tested:", len(results))
print(
    "Total input tokens:",
    sum(row["input_tokens"] for row in results)
)
print(
    "Total output tokens:",
    sum(row["output_tokens"] for row in results)
)