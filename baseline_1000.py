
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
TEST_REQUESTS = TOTAL_REQUESTS

QUESTIONS_FILE = "evaluation_cases.csv"
OUTPUT_FILE = "baseline_1000_results.csv"

# Load the evaluation questions
with open(QUESTIONS_FILE, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    questions = list(reader)

if not questions or "question" not in questions[0]:
    raise ValueError("No questions found. Check evaluation_cases.csv.")

input_tokens_total = 0
output_tokens_total = 0
successful_requests = 0
failed_requests = 0

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "request_number", "timestamp", "question", "status",
        "input_tokens", "output_tokens", "total_tokens",
        "latency_seconds", "error"
    ])

    for request_number in range(1, TEST_REQUESTS + 1):
        question = questions[(request_number - 1) % len(questions)]["question"]
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
            usage = response.usage
            input_tokens = usage.prompt_tokens
            output_tokens = usage.completion_tokens
            total_tokens = input_tokens + output_tokens

            input_tokens_total += input_tokens
            output_tokens_total += output_tokens
            successful_requests += 1

            writer.writerow([
                request_number, timestamp, question, "success",
                input_tokens, output_tokens, total_tokens, latency, ""
            ])
            file.flush()

            print(
                f"Request {request_number}/{TEST_REQUESTS}: "
                f"question={question!r}, input={input_tokens}, "
                f"output={output_tokens}, total={total_tokens}, "
                f"latency={latency}s"
            )

        except Exception as error:
            latency = round(time.perf_counter() - start, 3)
            failed_requests += 1

            writer.writerow([
                request_number, timestamp, question, "failed",
                0, 0, 0, latency, str(error)
            ])
            file.flush()

            print(f"Request {request_number} failed: {error}")
            break

        time.sleep(2.1)

print("\nTEST SUMMARY")
print(f"Successful requests: {successful_requests}")
print(f"Failed requests: {failed_requests}")
print(f"Input tokens: {input_tokens_total}")
print(f"Output tokens: {output_tokens_total}")
print(f"Total tokens: {input_tokens_total + output_tokens_total}")
print(f"Results saved to: {OUTPUT_FILE}")

if successful_requests == TEST_REQUESTS and failed_requests == 0:
    print("Test passed. Verify the CSV before running 1,000 requests.")
else:
    print("Test incomplete. Resolve the error before continuing.")
