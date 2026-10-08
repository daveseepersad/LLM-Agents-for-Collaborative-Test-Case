
## HOW TO RUN

### Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> [!NOTE]
> Run experiments from the activated environment. Mutation testing launches `pytest` from `PATH`, and when it is not found the mutation metrics are silently recorded as `null`.

### LLM Providers

Experiments run on Groq (the provider of the original experiments) or on Azure AI Foundry. Set `llm.provider` in the experiment config to `groq` (default) or `azure_foundry`, then copy `.env.example` to `.env` and fill in the settings of the provider you use.

#### Groq

Go to https://console.groq.com/keys and generate an API_KEY, then put it in the .env file:

```bash
GROQ_API_KEY=my_key
```

Groq no longer serves the paper's two Llama models (`llama-3.3-70b-versatile` and `meta-llama/llama-4-scout-17b-16e-instruct` were retired in 2026, see https://console.groq.com/docs/deprecations); `openai/gpt-oss-120b` and `openai/gpt-oss-20b` are still available, including on the free tier.

The Groq client is set up for reasoning models and for the free tier:

* It requests the model's maximum output (`max_tokens`, 65,536 for the gpt-oss models). Without it Groq caps `openai/gpt-oss-20b` at 2,048 completion tokens, which can end the model's reasoning before it writes an answer. Set `llm.max_tokens` to use another limit.
* It waits out rate limits (HTTP 429) for as long as Groq asks, up to 12 hours per call, including the daily limits. The groq SDK alone gives up on waits longer than a minute.
* It retries, with a growing pause for up to 30 minutes, requests that Groq refuses as too large for the tokens-per-minute limit (HTTP 413). Groq adds an estimate of the completion to the prompt when it admits a request; the estimate follows the model's recent completions, up to `max_tokens`, so after a long reasoning answer it can refuse every request for a few minutes.

The free tier allows, per model, 30 requests and 8,000 tokens per minute and 1,000 requests and 200,000 tokens per day. The daily limit refills continuously, about 8,300 tokens an hour once it is used up, so an experiment runs at its pace: in the archived results a collaborative or competitive module used about 11,000 tokens at the median and up to 114,000, so a single configuration can take more than a day. A request must also fit within the 8,000 tokens per minute together with the completion estimate, so prompts of about 7,500 tokens or more are refused even when no other request is running. See [replication/README.md](replication/README.md#groq-free-tier) for a pilot on the free tier.

#### Azure AI Foundry

Model names in the config are deployment names of your Foundry resource (for example `gpt-5-mini`). Put the resource endpoint in the .env file:

```bash
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
```

Authentication uses Microsoft Entra ID through `DefaultAzureCredential`, so an `az login` session is enough. Your account needs a data-plane role on the resource, such as *Cognitive Services OpenAI User* or *Azure AI User*. If the resource allows key authentication you can set `AZURE_OPENAI_API_KEY` instead. `AZURE_OPENAI_API_VERSION` overrides the default API version (`2025-04-01-preview`).

```yaml
llm:
  provider: "azure_foundry"
  model: "gpt-5-mini"          # deployment name
  temperature: 1.0
  reasoning_effort: "medium"   # optional, sent to every role: minimal | low | medium | high
  # max_retries: 6             # optional, retries on transient errors (Azure default: 6)
  # timeout: 600               # optional, request timeout in seconds (default: 600)
  # max_tokens: 16384          # optional, completion token limit per call (Groq default: the model's maximum)
```

Ready-made configs: `single_gpt5mini.yaml`, `collaborative_gpt5mini_gpt5mini.yaml` and `competitive_gpt5mini_gpt5mini_gpt5mini.yaml`.

> [!IMPORTANT]
> Reasoning models such as gpt-5-mini (o-series and gpt-5 models, except chat variants) only accept their default temperature of 1. Any other configured temperature is ignored with a warning, and a deployment that rejects a temperature at runtime is retried without it. Each results file records, in `llm.models`, the temperature actually sent for each role (`null` means the provider default).

To mix providers or models, prefix a role's model with a provider name:

```yaml
llm:
  provider: "groq"
  planner_model: "azure_foundry:gpt-5-mini"
  generator_model: "llama-3.3-70b-versatile"
  temperature: 0.2
```

### Run Experiments

#### Option 1: Run Experiments via Command Line

```bash
python -m src.experiment_runner --config configs/experiments/{experiment_name}.yaml
```

Example:
```bash
python -m src.experiment_runner --config configs/experiments/single_gptoss120B.yaml
python -m src.experiment_runner --config configs/experiments/single_gpt5mini.yaml
```

The multi-agent loops stop after `agent.max_iterations` rounds (default 5) and re-plan while coverage is below `agent.target_coverage` (default 100). The archived `results/` were produced with different values of both settings over time; [replication/README.md](replication/README.md) documents them and replicates the full grid on Azure AI Foundry.

#### Option 2: Run via Jupyter Notebook

Open and run `experiments.ipynb` to execute experiments interactively.

#### Option 3: Analyze Results

After running experiments:

1. **Export metrics to CSV**:
   ```bash
   python export_metrics_as_csv.py
   ```
   This creates `all_metrics.csv` with aggregated results.

2. **Run mutation testing** (optional):
   Open and run `mutation_injection.ipynb` to inject mutations and measure test quality.

3. **View metrics visualization**:
   Open and run `metrics_aggregation.ipynb` to see aggregated metrics by experiment with charts.

### Tests

The unit tests run offline and never call a model:

```bash
python -m pytest tests
```

`tests/test_foundry_live.py` calls Azure AI Foundry and is skipped unless `RUN_FOUNDRY_LIVE_TESTS=1`. Run it before a long experiment to verify the endpoint, login and deployments. It checks token accounting, concurrent requests (as made by the competitive graph), the planner's JSON plan, and a full single-agent generation with pytest and coverage. `FOUNDRY_LIVE_DEPLOYMENTS` selects the deployments (comma separated, default `gpt-5-mini`) and `FOUNDRY_LIVE_REASONING_EFFORT` the reasoning effort (default: the model's default). Set the reasoning effort to the value in your experiment config, because some models accept only specific values.

```bash
RUN_FOUNDRY_LIVE_TESTS=1 python -m pytest tests/test_foundry_live.py -v
```

Prefix a model with `groq:` to run the same checks against Groq:

```bash
RUN_FOUNDRY_LIVE_TESTS=1 FOUNDRY_LIVE_DEPLOYMENTS="groq:openai/gpt-oss-120b,groq:openai/gpt-oss-20b" \
    python -m pytest tests/test_foundry_live.py -v
```

## Packages Overview

### LLM and Agent Management
- **langchain** / **langchain-core**: For base interaction with LLMs and prompt templates
- **langgraph**: Framework for agent orchestration with state graphs (replaces manual agent coordination)
- **langchain-groq** / **langchain-openai**: Chat model integrations for Groq and Azure AI Foundry
- **azure-identity**: Microsoft Entra ID authentication (e.g. `az login`) for Azure AI Foundry
- **python-dotenv**: To securely manage API keys

### Testing and Evaluation
- **pytest**: The standard framework for running generated tests
- **pytest-cov**: Plugin to calculate line/branch code coverage
- **mutmut**: For mutation testing (verify if tests "kill" mutants - artificially injected bugs)

### Data Analysis & Visualization
- **pandas**: To organize and aggregate metric results
- **matplotlib**: To create comparison charts and visualizations
- **numpy**: For numerical computations and statistics

### Configuration
- **PyYAML**: For loading experiment configuration files

## Output & Metrics

### Results Directory Structure
Each experiment creates a JSON file in `results/` with:
- `run_id`: Unique identifier (experiment_name + timestamp)
- `experiment_name`: Name of the configuration used
- `timestamp`: When the experiment was run
- `temperature`: LLM temperature parameter
- `llm`: Provider and reasoning effort, plus for each role (`models`) the provider, model and temperature actually sent (`null` means the provider default)
- `agent`: `max_iterations` and `target_coverage` of the multi-agent loop
- `results[]`: Array containing per-file results:
  - `file`: Source file name
  - `status`: success/failure
  - `metrics`:
    - `coverage_percent`: Line coverage percentage
    - `mutation_score_percent`: Mutation test success rate
    - `mutation_killed`: Number of mutations killed by tests
    - `mutation_survived`: Number of undetected mutations
    - `total_tokens`: LLM tokens used

### Analysis Notebooks
- **metrics_aggregation.ipynb**: Aggregates metrics by experiment_name, shows mean/std for coverage, mutation score, and tokens
- **mutation_injection.ipynb**: Runs mutation testing where missing, adds mutation metrics to results

### CSV Export
`export_metrics_as_csv.py` generates `all_metrics.csv` for easy analysis in Excel/Pandas

## Agent Architectures

### Single Agent
- One LLM generates all tests from scratch
- Baseline for comparison

### Multi-Agent Collaborative
- **Planner**: Creates test plan JSON
- **Developer**: Generates test code from plan
- **Executor**: Runs tests and measures coverage
- **Feedback Loop**: Re-plans to fill coverage gaps

### Multi-Agent Competitive
- **Planner**: Creates test plan
- **Developer 1 & 2**: Simultaneously generate different test implementations
- **Executor**: Runs both and selects best based on coverage/quality
- Strategy focuses on diverse test generation approaches

--------------
   
- TO RUN: python -m src.experiment_runner --config configs/experiments/{experiment_name}.yaml
