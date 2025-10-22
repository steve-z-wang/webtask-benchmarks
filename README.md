# webtask-benchmarks

Evaluation framework for testing webtask agents on web automation benchmarks.

## Directory Structure

This repo expects the following structure in your workspace:

```
<your-workspace>/
├── Mind2Web/              # Clone from OSU-NLP-Group/Mind2Web
├── Mind2Web-data/         # Clone from HuggingFace dataset
├── webtask/               # Main webtask library
└── webtask-benchmarks/    # This repo
    ├── mind2web/          # Mind2Web evaluation scripts
    └── results/           # Evaluation results (gitignored)
```

## Setup

**1. Clone required repositories** (if not already done):

```bash
cd <your-workspace>

# Clone Mind2Web benchmark repo
git clone https://github.com/OSU-NLP-Group/Mind2Web.git

# Clone Mind2Web dataset
git clone https://huggingface.co/datasets/osunlp/Mind2Web Mind2Web-data

# Clone webtask library
git clone <your-webtask-repo> webtask

# Clone this benchmarks repo
git clone <this-repo> webtask-benchmarks
```

**2. Install dependencies**:

```bash
# Install webtask library
cd webtask
pip install -e .

# Install benchmark dependencies
cd ../webtask-benchmarks
pip install -r requirements.txt
```

## Running Mind2Web Evaluation

```bash
cd mind2web

# Test single task
python run_single.py --task-id 0

# Run evaluation on test split
python run_eval.py --split test_task --max-tasks 10

# Generate report
python generate_report.py --results ../results/
```

## Benchmarks

### Mind2Web
- **Paper**: [Mind2Web: Towards a Generalist Agent for the Web](https://arxiv.org/abs/2306.06070)
- **Dataset**: 2,000+ tasks, 137 websites, 31 domains
- **Test Splits**: test_task, test_website, test_domain
- **Metrics**: Element accuracy, action accuracy, task success rate

See `mind2web/README.md` for details.

## Results

Results are saved to `results/` with timestamps and stored in JSON format.
