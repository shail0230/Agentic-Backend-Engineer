"""
tests.py — Determinism + Edge Case Tests
Run with: python tests.py
"""
import json
from pipeline import run_pipeline


def assert_equal(label, a, b):
    status = "✅ PASS" if a == b else f"❌ FAIL  expected={b!r}  got={a!r}"
    print(f"  {status}  [{label}]")


def assert_in(label, val, collection):
    status = "✅ PASS" if val in collection else f"❌ FAIL  {val!r} not in {collection!r}"
    print(f"  {status}  [{label}]")


def assert_range(label, val, lo, hi):
    status = "✅ PASS" if lo <= val <= hi else f"❌ FAIL  {val} not in [{lo}, {hi}]"
    print(f"  {status}  [{label}]")


# ── Test 1: Determinism ────────────────────────────────────────────────────────
print("\n=== TEST 1: DETERMINISM (same input → same output) ===")
text = "Build a FastAPI endpoint to extract keywords from a JSON dataset using NLP pipeline."
r1 = run_pipeline(text)
r2 = run_pipeline(text)
r3 = run_pipeline(text)
assert_equal("word_count consistent", r1["word_count"], r2["word_count"])
assert_equal("technical_terms consistent", r1["technical_terms"], r3["technical_terms"])
assert_equal("complexity consistent", r1["complexity"], r2["complexity"])
assert_equal("clarity_score consistent", r1["clarity_score"], r3["clarity_score"])


# ── Test 2: Normal Input ───────────────────────────────────────────────────────
print("\n=== TEST 2: NORMAL INPUT ===")
text = """
Objective: Build a deterministic data ingestion pipeline.
Requirements:
- Accept text input and optional file upload (PDF or JSON)
- Extract technical terms and action verbs
- Detect sections and step patterns
- Return structured JSON output with complexity and clarity scores.
"""
r = run_pipeline(text)
print(f"  word_count={r['word_count']}, complexity={r['complexity']}, clarity={r['clarity_score']}")
assert_in("pipeline in technical_terms", "pipeline", r["technical_terms"])
assert_in("json in technical_terms", "json", r["technical_terms"])
assert_in("build in action_verbs", "build", r["action_verbs"])
assert_in("output section detected", "output", r["sections_detected"])
assert_in("input section detected", "input", r["sections_detected"])
assert_range("clarity_score in range", r["clarity_score"], 0.0, 10.0)


# ── Test 3: Short Input ────────────────────────────────────────────────────────
print("\n=== TEST 3: SHORT / MINIMAL INPUT ===")
r = run_pipeline("hello world")
assert_equal("short complexity=low", r["complexity"], "low")
assert_equal("short category=short", r["signals"]["input_length_category"], "short")
print(f"  word_count={r['word_count']}, complexity={r['complexity']}")


# ── Test 4: High Technical Input ───────────────────────────────────────────────
print("\n=== TEST 4: HIGH TECHNICAL DENSITY ===")
text = (
    "Implement a transformer-based neural network with LSTM layers for NLP classification. "
    "Use FastAPI endpoint for inference with Redis cache and Celery queue. "
    "Deploy with Docker on Kubernetes. Configure JWT authentication and OAuth. "
    "Optimize gradient descent with batch training and hyperparameter tuning. "
    "Monitor with custom metrics, logging, and benchmark latency throughput scalability."
)
r = run_pipeline(text)
assert_equal("high complexity", r["complexity"], "high")
assert_equal("technical content signal", r["signals"]["has_technical_content"], True)
print(f"  tech_terms={r['technical_terms'][:5]}, density={r['technical_density']}")


# ── Test 5: JSON File Input ────────────────────────────────────────────────────
print("\n=== TEST 5: JSON FILE PROCESSING ===")
sample_json = json.dumps({
    "task": "Build a classification pipeline",
    "requirements": ["extract features", "train model", "deploy endpoint"],
    "tech_stack": ["fastapi", "sklearn", "docker"]
}).encode("utf-8")
r = run_pipeline("Process this configuration", file_content=sample_json, file_type="json")
assert_equal("file_processed=json", r["file_processed"], "json")
assert_in("fastapi in technical_terms", "fastapi", r["technical_terms"])
print(f"  file_processed={r['file_processed']}, technical_terms={r['technical_terms']}")


# ── Test 6: Empty-like edge cases ──────────────────────────────────────────────
print("\n=== TEST 6: EDGE CASES ===")
# Only spaces — pipeline should still run (main.py guards empty)
r = run_pipeline("   data pipeline   ")
assert_equal("whitespace-trimmed word_count", r["word_count"], 2)
print(f"  whitespace input: word_count={r['word_count']}")

# Very long input
long_text = "Build and implement a scalable data ingestion pipeline. " * 30
r = run_pipeline(long_text)
assert_equal("long category", r["signals"]["input_length_category"], "long")
print(f"  long input: word_count={r['word_count']}, complexity={r['complexity']}")

print("\n=== ALL TESTS COMPLETE ===\n")
