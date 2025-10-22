# Mind2Web Evaluation

Evaluate webtask agents on the Mind2Web benchmark.

## Dataset

Mind2Web contains 2,000+ web tasks from 137 websites across 31 domains.

**Data location**: `../../Mind2Web-data/`

The dataset includes:
- **Training**: 1,009 tasks
- **Test splits**:
  - `test_task`: Same websites, different tasks
  - `test_website`: Unseen websites in seen domains
  - `test_domain`: Completely unseen domains

## Task Format

Each task includes:
- `confirmed_task`: Natural language instruction
- `actions`: List of steps with operation types (CLICK, TYPE, SELECT)
- `cleaned_html`: HTML snapshot before each action
- `pos_candidates`: Positive element candidates
- `neg_candidates`: Negative element candidates

## Running Evaluation

```bash
# Load and inspect a single task
python data_loader.py --task-id 0

# Run agent on single task
python run_single.py --task-id 0

# Run on test split
python run_eval.py --split test_task --max-tasks 10
```

## Metrics

- **Element Selection Accuracy**: % of correct element selections
- **Action Accuracy**: % of correct action types
- **Task Success Rate**: % of tasks completed successfully
- **Step Efficiency**: Average steps taken per task

## Results

Results are saved to `../results/mind2web_<timestamp>.json` with:
- Per-task metrics
- Aggregate statistics
- Error logs
