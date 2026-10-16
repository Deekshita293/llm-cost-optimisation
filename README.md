# LLM Cost Optimisation Study

## 1. Project Overview

The LLM Cost Optimisation Study explores techniques for reducing the cost and resource usage of Large Language Model (LLM) applications while maintaining useful and accurate responses.

The project uses the Groq API and Python to measure token usage and response latency, test optimisation techniques, and compare experimental results.

Three techniques were investigated: prompt optimisation, output-token limit control, and response caching.

## 2. Objectives

- Measure input and output token usage.
- Record response latency for LLM requests.
- Compare baseline and optimised token usage.
- Test prompt optimisation and output-token limits.
- Implement response caching to avoid repeated API calls.
- Evaluate answer quality before and after optimisation.
- Analyse cost, performance, and quality trade-offs.
- Develop evidence-based recommendations for LLM cost optimisation.

## 3. Technologies Used

- Python
- Groq API
- Groq Python SDK
- python-dotenv
- CSV for experimental data
- JSON for local response caching
- Visual Studio Code

## 4. Project Structure

llm-cost-optimisation/
├── .venv/
├── main.py
├── cache_test.py
├── check_models.py
├── run_evaluation.py
├── baseline_1000.py
├── resume_baseline.py
├── evaluation_cases.csv
├── baseline_original_results.csv
├── baseline_5_test_results.csv
├── baseline_1000_results.csv
├── prompt_optimisation_results.csv
├── output_optimisation_results.csv
├── token_limit_results.csv
├── response_cache.json
├── requirements.txt
├── .gitignore
├── .env
└── README.md

The `.venv/` directory contains the local Python virtual environment.

The `.env` file stores the Groq API key and must not be committed to a public repository. The `.venv/` directory should also be excluded from version control.

The CSV files contain baseline and optimisation experiment results. `baseline_1000.py` runs the 1,000-request baseline experiment, while `resume_baseline.py` resumes an interrupted run using previously recorded successful requests.

## 5. Methodology

A fixed set of five questions was used to evaluate the model:

1. What is an API?
2. What is caching?
3. What is an LLM?
4. Why reduce prompt length?
5. What is a trade-off in cost optimisation?

The original baseline was recorded first. The same five questions were then used to test the optimisation configurations.

The evaluation script recorded input tokens, output tokens, total tokens, response latency, and the request completion status.

The baseline and optimisation results were saved in separate CSV files for comparison.

## 6. Optimisation Techniques

### A. Prompt Optimisation

The system instruction was shortened to encourage concise answers using simple English.

The purpose was to reduce unnecessary prompt tokens while preserving the essential information.

**Result:** Total token usage increased slightly from 940 to 947 tokens across the five test questions.

This demonstrates that shortening a prompt does not necessarily reduce total token usage. Output length and the model's response also affect the result.

### B. Output-Token Limit Control

The `max_completion_tokens` parameter was reduced from 300 to 200 to test whether a smaller completion-token budget would reduce token usage.

The model's answers and token counts did not change in the recorded experiment.

**Result:** Total token usage remained at 902 tokens, showing no measurable reduction in this run.

A restrictive output limit can also affect response completeness. Therefore, output limits should be selected carefully and evaluated alongside answer quality.

### C. Response Caching

A local JSON-based cache was implemented to reuse answers to repeated, identical questions.

The process works as follows:

1. The application checks whether the question exists in the cache.
2. If the question is not cached, the application calls the Groq API.
3. The generated answer is stored in the local JSON cache.
4. If the same question is submitted again, the cached answer is returned without another model call.

**Result:** Testing confirmed that a cache miss made one API call and a subsequent cache hit reused the saved answer with zero additional model calls.

Caching can reduce repeated API calls and may reduce response latency by returning saved answers locally. Its benefits depend on how often requests can reuse cached answers.

## 7. Experimental Results

The following results were collected from five-question evaluation runs.

| Experiment | Input Tokens | Output Tokens | Total Tokens |
|---|---:|---:|---:|
| Original baseline | 499 | 441 | 940 |
| Prompt optimisation | 474 | 473 | 947 |
| Output optimisation | 489 | 413 | 902 |
| Token-limit experiment | 489 | 413 | 902 |

### 7.1 Token-Usage Comparison

**Prompt optimisation**

- Baseline total: 940 tokens
- Optimised total: 947 tokens
- Change: Increase of 7 tokens, approximately 0.74%

Prompt optimisation did not reduce total token usage in this test.

**Output optimisation**

- Baseline total: 940 tokens
- Optimised total: 902 tokens
- Reduction: 38 tokens, approximately 4.04%

Output optimisation produced a modest reduction in total token usage.

**Token-limit experiment**

- Output-optimisation total: 902 tokens
- Token-limit total: 902 tokens
- Reduction: 0 tokens

The lower completion-token limit did not change the recorded results.

### 7.2 Response Latency

| Experiment | Average Latency |
|---|---:|
| Original baseline | 0.750 seconds |
| Output optimisation | 0.627 seconds |

The average latency decreased by approximately 16.4% in these recorded runs.

Latency can vary with network conditions, service load, and other factors. Because the experiments used only five questions, this difference should be treated as an observation rather than proof of a consistent speed improvement.

### 7.3 Response Caching Results

| Scenario | API Calls | Behaviour |
|---|---:|---|
| Cache miss | 1 | Calls the Groq API and saves the answer |
| Cache hit | 0 | Reuses the saved answer |

A cache hit avoids a new model-generation request for that repeated question. The saved answer is reused locally.

### 7.4 Extended Baseline Experiment: 1,000 Requests

After the initial five-question experiments, an extended baseline experiment was completed using 1,000 successful Groq API requests. The same five predefined questions were repeated in sequence, and usage data was recorded in `baseline_1000_results.csv`.

| Measurement | Result |
|---|---:|
| Successful requests | 1,000 |
| Failed requests | 0 |
| Input tokens | 92,800 |
| Output tokens | 142,149 |
| Total tokens | 234,949 |
| Estimated cost | $0.049605 |

The estimated cost was calculated using the published input and output token pricing for the selected model. It represents a token-based cost estimate rather than a verified billed charge.

This extended experiment measures the baseline only. The optimisation results in Sections 7.1–7.3 were collected separately using five-question tests. Therefore, direct cost-savings claims at the 1,000-request scale cannot be made until the optimised configurations are tested on a comparable workload.

## 8. Answer-Quality Evaluation


Answer quality was evaluated manually using the expected answers in `evaluation_cases.csv`.

The following scoring rubric was used:

- **2 points:** Correct answer containing the essential information.
- **1 point:** Partially correct answer that misses an important detail.
- **0 points:** Incorrect or irrelevant answer.

| Question | Baseline | Prompt Optimisation | Output Optimisation | Token-Limit Experiment |
|---|---:|---:|---:|---:|
| What is an API? | 2/2 | 2/2 | 2/2 | 2/2 |
| What is caching? | 2/2 | 2/2 | 2/2 | 2/2 |
| What is an LLM? | 2/2 | 2/2 | 2/2 | 2/2 |
| Why reduce prompt length? | 2/2 | 1/2 | 2/2 | 2/2 |
| What is a trade-off in cost optimisation? | 2/2 | 2/2 | 2/2 | 2/2 |
| **Total** | **10/10** | **9/10** | **10/10** | **10/10** |
| **Quality Score** | **100%** | **90%** | **100%** | **100%** |

The baseline, output-optimisation, and token-limit configurations received 10/10 in this manual evaluation. Prompt optimisation received 9/10 because its answer to the prompt-length question did not directly mention reducing input tokens and potentially lowering cost.

These results are based on five questions and a subjective manual scoring rubric. They provide an initial comparison of answer quality but do not establish that quality will remain consistent across a wider range of tasks.

## 9. Cost Analysis

The project records input tokens, output tokens, total tokens, and response latency from API responses. These measurements provide a basis for analysing usage and comparing optimisation techniques.

The Groq dashboard also provides usage and cost information. However, the displayed account-wide cost may include requests from other projects using the same account or API keys. Therefore, this amount cannot be attributed entirely to this experiment.

### Cost per 1,000 Requests

The baseline experiment completed 1,000 successful API requests using the `openai/gpt-oss-20b` model through the Groq API. The same five predefined questions were repeated in sequence. Token usage was recorded from each API response and saved in `baseline_1000_results.csv`.

The published pricing used for this calculation is:

- Input tokens: $0.075 per 1 million tokens
- Output tokens: $0.30 per 1 million tokens

Source: [Official Groq GPT OSS 20B documentation](https://console.groq.com/docs/model/openai/gpt-oss-20b).

| Measurement | 1,000-request baseline |
|---|---:|
| Successful requests | 1,000 |
| Failed requests | 0 |
| Input tokens | 92,800 |
| Output tokens | 142,149 |
| Total tokens | 234,949 |
| Estimated input cost | $0.006960 |
| Estimated output cost | $0.042645 |
| **Estimated total cost** | **$0.049605** |

**Cost calculation:**

Input cost = (92,800 / 1,000,000) × $0.075 = $0.006960

Output cost = (142,149 / 1,000,000) × $0.30 = $0.042645

**Estimated baseline cost per 1,000 requests = $0.049605 (approximately $0.050).**

This cost is calculated from the measured token usage and the pricing rates listed above. It is not a verified billed charge from Groq.

### Cost Measurement Limitation

The baseline CSV records token usage for all 1,000 successful API requests. However, the calculated cost is based on published token rates, not an isolated invoice for this experiment. Account-wide billing may include API usage from other projects.

The experiment repeats five predefined questions to reach 1,000 requests. Therefore, it measures 1,000 API calls but does not represent 1,000 unique questions. The results should be interpreted within this limitation.

## 10. Key Findings
- The 1,000-request baseline recorded 92,800 input tokens and 142,149 output tokens, for a total of 234,949 tokens.
- The estimated baseline cost for 1,000 API requests was $0.049605, calculated using the published token pricing rates.
- Prompt optimisation increased total token usage by approximately 0.74% in the five-question experiment.
- Output optimisation reduced total token usage by approximately 4.04% in the five-question experiment while retaining the same manual quality score.
- Reducing `max_completion_tokens` from 300 to 200 produced no measurable change in token usage in the recorded experiment.
- Response caching successfully reused an existing answer without making another model-generation API call.
- The baseline and output-optimisation configurations both scored 10/10 in the five-question manual quality evaluation.
- The optimisation results are preliminary; further testing using a larger, consistent workload is needed to establish reliable cost savings at scale.

## 11. Limitations

- The experiments used only five predefined questions.
- The results may not generalise to all LLM applications.
- Latency can vary across runs.
- Answer quality was evaluated manually rather than using an automated or independent evaluation system.
- The lower token limit showed no measurable reduction in the recorded experiment.
- Actual baseline cost per 1,000 requests has not been isolated from billing records.
- The local cache uses exact question matching and may not reuse answers for differently worded questions.
- Cache effectiveness depends on the frequency of repeated requests.

## 12. Final Recommendation

Based on the experiments, response caching is the clearest demonstrated optimisation for repeated, identical questions because it avoids additional model calls when a cached answer is available.

Output optimisation also showed a modest reduction in total token usage while retaining the same manual quality score across the five test questions.

Prompt optimisation should be evaluated using measured results rather than assuming that shorter instructions will always reduce total usage.

The output-token limit should be chosen based on actual response requirements. Lowering the limit did not improve token usage in this experiment.

For practical applications, a combination of caching and carefully tested prompt/output optimisation is recommended. The effectiveness of each technique should be validated using a larger dataset, repeated trials, and verified cost records.

## 13. How to Run the Project

1. Install Python.

2. Open a terminal in the project directory and create a virtual environment:
  
   python -m venv .venv

3. Activate the virtual environment on Windows:

   .venv\Scripts\activate

4. Install the required dependencies:

   pip install -r requirements.txt

5. Create a `.env` file in the project directory and add your Groq API key:

   GROQ_API_KEY=your_api_key

6. Run the main application:

   python main.py

7. Run the evaluation script:

   python run_evaluation.py

8. Test response caching:

   python cache_test.py

   Run the cache test again with the same question to observe a cache hit.

## 14. Security

- Never upload `.env` or API keys to a public repository.
- Keep `.env` listed in `.gitignore`.
- Do not publish credentials in screenshots, logs, or documentation.
- Review generated CSV and JSON files before sharing them publicly.

## 15. Conclusion

This project investigated practical techniques for optimising Large Language Model (LLM) usage using Python and the Groq API.

The baseline experiment completed 1,000 successful API requests, recording 92,800 input tokens and 142,149 output tokens. Based on published token pricing rates, the estimated baseline cost was $0.049605 per 1,000 requests. This is a calculated estimate, not a verified billed charge.

Three optimisation techniques were evaluated: prompt optimisation, output-token limit control, and response caching. In the preliminary five-question experiments, output optimisation reduced total token usage by approximately 4.04% while maintaining the same manual quality score. Prompt optimisation slightly increased total token usage, while reducing the output-token limit produced no measurable change in token usage in the recorded experiment. Response caching successfully reused a saved answer without making another model-generation API call for an identical question.

The results demonstrate that optimisation techniques should be evaluated using measured token usage, response quality, latency, and application requirements. Since the optimisation experiments used only five predefined questions, further testing on a larger, consistent workload is needed to establish reliable cost savings at scale.