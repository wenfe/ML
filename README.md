# AI Agent Project

A modular Python starter project for an AI agent, following the structure in the
provided reference.

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Add your model API key to `.env`:

   ```env
   OPENAI_API_KEY=your-api-key
   OPENAI_MODEL=gpt-4o-mini
   ```

   Keep `.env` private; it is excluded from Git.

## Run

Start the command-line agent:

```powershell
python main.py
```

Or start the HTTP API:

```powershell
uvicorn src.api.routes:app --reload
```

Send a request to `POST /chat` with JSON such as:

```json
{"message": "Explain what an AI agent is."}
```

The project includes starter tool modules for local document search,
calculations, and weather lookups. Add new tools under `src/tools/` and register
them with `src/agent/executor.py`.

## MNIST notebook

`src/agent/MNIST.ipynb` uses `src/agent/helper_utils.py` to display images,
predictions, and training metrics. Run the notebook with `src/agent` as its
working directory so that `import helper_utils` finds the module. In the
notebook's Python environment, install PyTorch and torchvision as well as the
packages in `requirements.txt`:

```powershell
pip install -r requirements.txt
pip install torch torchvision
```

The notebook also downloads the MNIST dataset. Prediction plots sample from
the first test batch; test accuracy values are percentages.

## Tests

```powershell
python -m unittest discover -s tests
```

## Project layout

```text
.
├── data/
│   ├── examples.json
│   └── knowledge_base/
├── logs/
├── src/
│   ├── agent/
│   ├── api/
│   ├── models/
│   ├── prompts/
│   ├── tools/
│   └── utils/
├── tests/
├── main.py
├── requirements.txt
└── docker-compose.yml
```
