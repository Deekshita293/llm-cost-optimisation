import os
import json
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CACHE_FILE = "response_cache.json"

# Load saved answers
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as file:
        cache = json.load(file)
else:
    cache = {}

question = "Explain prompt compression in simple English."

if question in cache:
    print("CACHE HIT - Reusing saved answer")
    answer = cache[question]
    print("Cache retrieval completed instantly (no model call).")
    print("AI Answer:", answer)
    print("API calls: 0")
else:
    print("CACHE MISS - Calling Groq API")
    start = time.time()

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "Answer in simple English using 2 short sentences."
            },
            {"role": "user", "content": question}
        ],
        max_completion_tokens=300,
        temperature=0
    )

    answer = response.choices[0].message.content
    elapsed = time.time() - start

    print("AI Answer:", answer)
    print("API calls: 1")
    print("Input tokens:", response.usage.prompt_tokens)
    print("Output tokens:", response.usage.completion_tokens)
    print("Time taken:", round(elapsed, 2), "seconds")

    # Save answer for future reuse
    cache[question] = answer
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file, indent=2)

    print("Answer saved in cache.")
