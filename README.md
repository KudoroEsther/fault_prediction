# PowerBot Fault Analysis

PowerBot is a machine learning and RAG application for transmission line fault analysis. The backend predicts the likely fault class from six electrical measurements, then uses retrieval-augmented generation to explain the fault and suggest mitigation steps.

## Project Structure

```text
Fault_Analysis/
├── powerbot/
│   └── app/
│       ├── main.py
│       ├── api/routes/
│       ├── core/
│       ├── schemas/
│       ├── services/
│       ├── features/
│       ├── rag/
│       ├── models/
│       └── utils/
├── artifacts/
│   ├── detection_pipeline.pkl
│   └── vectorstore/
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
│   ├── train_model.py
│   └── build_vectorstore.py
├── tests/
├── deployment/
├── .env.example
├── requirements.txt
└── README.md
```

## Backend Layout

- `powerbot/app/main.py` creates the FastAPI application and registers the routes.
- `powerbot/app/api/routes/` contains `predict`, `diagnose`, and `health` endpoints.
- `powerbot/app/services/` contains the prediction and diagnosis orchestration logic.
- `powerbot/app/features/transformer.py` contains the scikit-learn feature engineering transformer.
- `powerbot/app/rag/` contains document loading, vector store access, retrieval, and prompt building.
- `powerbot/app/models/model_loader.py` loads the saved ML pipeline from `artifacts/`.

## Artifacts And Data

- The trained pipeline now lives at `artifacts/detection_pipeline.pkl`.
- The Chroma vector store now lives under `artifacts/vectorstore/`.
- The dataset has been moved to `data/raw/merged_dataset.csv`.
- Place RAG source documents in `data/raw/docs/` before running the vector store build script.

## Local Run

1. Create a virtual environment and install dependencies.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` or `PAID_API2`.

3. Start the API.

```bash
uvicorn powerbot.app.main:app --reload
```

4. Open `frontend/index.html` in a browser and point it at the local API on `http://localhost:8000`.

## Utility Scripts

- Train and save a fresh model:

```bash
python scripts/train_model.py
```

- Build or rebuild the RAG vector store:

```bash
python scripts/build_vectorstore.py
```

## Tests

```bash
pytest
```

## Notes

- Root-level `main.py`, `train.py`, `Feature_engineer.py`, `utils_openai.py`, and `fault_rag_using_utils.py` were kept as compatibility shims for the original prototype workflow.
- The `/diagnose` route needs a valid OpenAI API key. `/predict` can run with the local model alone.
