# TODO: Mind2Web Evaluation

## Current Status
- [x] Repository setup
- [x] Mind2Web data types (Task, Action, Operation, Candidate)
- [x] Mind2Web data loader (load_train_split, load_test_split)

## Next Steps

### Phase 1: Evaluation Infrastructure
- [ ] Create `mind2web/evaluator.py`
  - [ ] Initialize webtask agent with LLM
  - [ ] Load task and extract starting URL
  - [ ] Run agent on task instruction
  - [ ] Capture agent actions and compare to ground truth
  - [ ] Handle errors and timeouts gracefully
  - [ ] Return evaluation results for task

- [ ] Create `mind2web/metrics.py`
  - [ ] Element selection accuracy (did we select right element?)
  - [ ] Action type accuracy (CLICK vs TYPE vs SELECT)
  - [ ] Task success rate (did task complete successfully?)
  - [ ] Step efficiency (steps taken vs ground truth)

- [ ] Create `mind2web/run_single.py`
  - [ ] CLI to test on single task by index
  - [ ] Print detailed logs and step-by-step comparison
  - [ ] Save results to JSON file

- [ ] Create `mind2web/run_eval.py`
  - [ ] CLI to run on full test split
  - [ ] Batch processing with progress bar
  - [ ] Save aggregate results and per-task details
  - [ ] Generate summary report

### Phase 2: Testing & Debugging
- [ ] Test data loader on sample tasks
  - [ ] Verify task instructions load correctly
  - [ ] Verify action sequences parse correctly
  - [ ] Verify HTML snapshots are accessible

- [ ] Run evaluator on 1 task manually
  - [ ] Debug any issues with agent initialization
  - [ ] Verify element selection works
  - [ ] Verify action execution works
  - [ ] Fix any errors

- [ ] Run on 10 tasks from test_task split
  - [ ] Analyze failures and common errors
  - [ ] Identify patterns in what works/doesn't work
  - [ ] Iterate and improve

### Phase 3: Full Evaluation
- [ ] Run on test_task split (same websites)
  - [ ] ~100 tasks
  - [ ] Save detailed results

- [ ] Run on test_website split (cross-website)
  - [ ] ~180 tasks
  - [ ] Compare to test_task performance

- [ ] Run on test_domain split (cross-domain)
  - [ ] ~180 tasks
  - [ ] Hardest split - completely new domains

- [ ] Generate comprehensive report
  - [ ] Aggregate metrics across splits
  - [ ] Error analysis
  - [ ] Comparison to Mind2Web baselines

### Phase 4: Analysis & Iteration
- [ ] Document findings in `results/`
- [ ] Identify common failure modes
- [ ] Propose improvements to webtask library
- [ ] Re-run after improvements

## Notes
- Mind2Web data: `../Mind2Web-data/data/`
- Mind2Web repo (reference): `../Mind2Web/`
- webtask library: `../webtask/` (install with `pip install -e ../webtask`)
- Focus on getting 1 task working end-to-end first before scaling
- Use logging to debug agent behavior
