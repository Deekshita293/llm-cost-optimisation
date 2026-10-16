
import os
import csv
import time
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is missing from your .env file.")

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-20b"
TOTAL_REQUESTS = 1000
QUESTIONS_FILE = "evaluation_cases.csv"
OUTPUT_FILE = "baseline_1000_results.csv"

fields = [
    "request_number", "timestamp", "question", "status",
    "input_tokens", "output_tokens", "total_tokens",
    "latency_seconds", "error"
]

# Keep successful results and remove failed attempts from the CSV.
with open(OUTPUT_FILE, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    saved_rows = [
        row for row in reader if row["status"] == "success"
    ]

successful_numbers = {
    int(row["request_number"]) for row in saved_rows
}

with open(QUESTIONS_FILE, "r", newline="", encoding="utf-8-sig") as file:
    questions = list(csv.DictReader(file))

if not questions or "question" not in questions[0]:
    raise ValueError("Check evaluation_cases.csv.")

# Rewrite the CSV with successful results only.
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(saved_rows)

input_total = sum(int(row["input_tokens"]) for row in saved_rows)
output_total = sum(int(row["output_tokens"]) for row in saved_rows)

print(f"Already completed: {len(successful_numbers)} requests")

with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)

    for number in range(1, TOTAL_REQUESTS + 1):
        if number in successful_numbers:
            continue

        question = questions[(number - 1) % len(questions)]["question"]
        start = time.perf_counter()
        timestamp = datetime.now().isoformat(timespec="seconds")

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Answer clearly and accurately in simple English. "
                            "Keep the answer concise."
                        )
                    },
                    {"role": "user", "content": question}
                ],
                max_completion_tokens=300,
                temperature=0,
            )

            latency = round(time.perf_counter() - start, 3)
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            row = {
                "request_number": number,
                "timestamp": timestamp,
                "question": question,
                "status": "success",
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "latency_seconds": latency,
                "error": ""
            }

            writer.writerow(row)
            file.flush()

            input_total += input_tokens
            output_total += output_tokens
            successful_numbers.add(number)

            print(
                f"Request {number}/{TOTAL_REQUESTS}: success, "
                f"input={input_tokens}, output={output_tokens}, "
                f"latency={latency}s"
            )

        except Exception as error:
            print(f"Request {number} failed: {error}")
            print("Stopped. Your successful results are saved.")
            break

        time.sleep(2.1)

print("\nCURRENT SUMMARY")
print(f"Successful requests: {len(successful_numbers)}")
print(f"Remaining requests: {TOTAL_REQUESTS - len(successful_numbers)}")
print(f"Input tokens: {input_total}")
print(f"Output tokens: {output_total}")
print(f"Results saved to: {OUTPUT_FILE}")
