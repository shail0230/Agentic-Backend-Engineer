"""
pipeline.py — Deterministic Data Ingestion & Processing Pipeline
All logic is rule-based. Same input always produces same output.
"""

import re
import json
import string
from collections import Counter
from typing import Optional

# ── Constants (deterministic, no ML) ─────────────────────────────────────────

TECHNICAL_TERMS = {
    # Data / ML
    "pipeline", "model", "dataset", "ingestion", "preprocessing", "tokenization",
    "classification", "regression", "clustering", "nlp", "api", "endpoint",
    "schema", "json", "csv", "dataframe", "feature", "signal", "vector",
    "embedding", "inference", "training", "validation", "accuracy", "precision",
    "recall", "f1", "loss", "gradient", "batch", "epoch", "hyperparameter",
    "transformer", "lstm", "neural", "network", "layer", "activation",
    # Backend / Infra
    "fastapi", "flask", "sqlalchemy", "database", "orm", "migration",
    "docker", "kubernetes", "microservice", "rest", "graphql", "websocket",
    "middleware", "async", "coroutine", "thread", "process", "queue",
    "cache", "redis", "celery", "kafka", "rabbitmq", "postgres", "sqlite",
    "authentication", "authorization", "jwt", "oauth",
    # General tech
    "algorithm", "complexity", "deterministic", "heuristic", "parser",
    "extractor", "serializer", "deserializer", "payload", "request",
    "response", "latency", "throughput", "scalability", "performance",
    "benchmark", "optimization", "refactor", "deploy", "ci", "cd",
    "git", "repository", "commit", "branch", "merge", "pull", "push",
    "function", "class", "method", "module", "package", "library",
    "framework", "interface", "abstract", "inheritance", "polymorphism",
    "struct", "array", "list", "dict", "set", "tuple", "stack", "heap",
    "recursion", "iteration", "loop", "condition", "exception", "error",
    "logging", "monitoring", "metric", "dashboard", "visualization",
}

ACTION_VERBS = {
    "build", "create", "implement", "develop", "design", "define",
    "extract", "process", "analyze", "parse", "detect", "identify",
    "generate", "return", "accept", "handle", "validate", "test",
    "deploy", "run", "execute", "compute", "calculate", "evaluate",
    "compare", "rank", "score", "classify", "cluster", "transform",
    "load", "save", "read", "write", "fetch", "store", "update",
    "delete", "merge", "split", "filter", "map", "reduce", "sort",
    "send", "receive", "connect", "configure", "initialize", "setup",
    "check", "verify", "ensure", "enforce", "log", "monitor", "track",
    "expose", "wrap", "extend", "refactor", "optimize", "benchmark",
}

SECTION_PATTERNS = {
    "objective":    r"\b(objective|goal|purpose|aim|target)\b",
    "requirement":  r"\b(requirement[s]?|must|shall|should|need[s]?)\b",
    "constraint":   r"\b(constraint[s]?|limitation[s]?|restriction[s]?|boundary|boundaries)\b",
    "input":        r"\b(input[s]?|accept[s]?|receive[s]?|ingest[s]?|upload[s]?)\b",
    "output":       r"\b(output[s]?|return[s]?|produce[s]?|generate[s]?|result[s]?)\b",
    "timeline":     r"\b(timeline|deadline|duration|days|hours|week[s]?|sprint)\b",
    "evaluation":   r"\b(evaluat[ei]|score|grade|assess|criteria|parameter[s]?|pass|fail)\b",
    "deliverable":  r"\b(deliverable[s]?|submit|submission|provide|repo|readme|demo)\b",
    "phase":        r"\b(phase|step|stage|part|section|module)\b",
    "error":        r"\b(error|exception|handle|invalid|empty|malformed|edge case)\b",
}

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "this", "that", "these", "those",
    "it", "its", "as", "up", "so", "if", "no", "not", "than", "then",
    "into", "over", "after", "before", "i", "you", "we", "they", "he",
    "she", "me", "him", "her", "us", "them", "my", "your", "our", "their",
    "what", "which", "who", "whom", "how", "when", "where", "why",
    "also", "just", "more", "very", "can", "all", "any", "each",
    "about", "between", "through", "during", "same", "both", "such",
}


# ── File Extractors ────────────────────────────────────────────────────────────

def extract_text_from_pdf(content: bytes) -> str:
    """Extract raw text from PDF bytes without ML."""
    try:
        import pdfplumber
        import io
        lines = []
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    lines.append(t.strip())
        return "\n".join(lines)
    except Exception as e:
        return f"[PDF extraction error: {e}]"


def extract_text_from_json(content: bytes) -> str:
    """Flatten JSON content into readable text."""
    try:
        data = json.loads(content.decode("utf-8"))
        return _flatten_json(data)
    except Exception as e:
        return f"[JSON extraction error: {e}]"


def _flatten_json(obj, depth=0) -> str:
    """Recursively flatten JSON to plain text."""
    parts = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            parts.append(f"{k}: {_flatten_json(v, depth+1)}")
    elif isinstance(obj, list):
        for item in obj:
            parts.append(_flatten_json(item, depth+1))
    else:
        parts.append(str(obj))
    return " ".join(parts)


# ── Text Analysis ──────────────────────────────────────────────────────────────

def tokenize(text: str) -> list[str]:
    """Simple deterministic tokenizer."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return [t for t in text.split() if t]


def count_words(text: str) -> int:
    return len(tokenize(text))


def count_sentences(text: str) -> int:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return len([s for s in sentences if s.strip()])


def get_keyword_frequency(tokens: list[str]) -> dict:
    """Top keywords excluding stop words."""
    filtered = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]
    counts = Counter(filtered)
    return dict(counts.most_common(15))


def get_technical_terms(tokens: list[str]) -> list[str]:
    """Deterministic lookup against known technical vocabulary."""
    found = sorted(set(t for t in tokens if t in TECHNICAL_TERMS))
    return found


def get_action_verbs(tokens: list[str]) -> list[str]:
    """Deterministic lookup against known action verbs."""
    found = sorted(set(t for t in tokens if t in ACTION_VERBS))
    return found


# ── Structure Detection ────────────────────────────────────────────────────────

def detect_sections(text: str) -> list[str]:
    """Detect which conceptual sections are present in the text."""
    text_lower = text.lower()
    found = []
    for section, pattern in SECTION_PATTERNS.items():
        if re.search(pattern, text_lower):
            found.append(section)
    return sorted(found)


def detect_step_patterns(text: str) -> dict:
    """Detect numbered/bulleted steps and list-like patterns."""
    numbered = re.findall(r"(?m)^\s*\d+[\.\)]\s+\S", text)
    bulleted = re.findall(r"(?m)^\s*[•\-\*]\s+\S", text)
    arrows   = re.findall(r"→|->|=>", text)
    return {
        "numbered_steps": len(numbered),
        "bulleted_items": len(bulleted),
        "arrow_flows":    len(arrows),
        "has_steps":      (len(numbered) + len(bulleted)) > 0
    }


# ── Signal Extraction ──────────────────────────────────────────────────────────

def compute_technical_density(tokens: list[str], tech_terms: list[str]) -> float:
    """Ratio of technical tokens to total tokens (0–1)."""
    if not tokens:
        return 0.0
    density = round(len(tech_terms) / len(tokens), 4)
    return min(density, 1.0)


def compute_complexity(
    word_count: int,
    sentence_count: int,
    tech_count: int,
    tech_density: float
) -> str:
    """
    Deterministic rule-based complexity scoring.
    Rules are transparent and repeatable.
    """
    score = 0

    # Word count rules
    if word_count > 300:   score += 3
    elif word_count > 150: score += 2
    elif word_count > 50:  score += 1

    # Avg sentence length
    if sentence_count > 0:
        avg_len = word_count / sentence_count
        if avg_len > 25:   score += 2
        elif avg_len > 15: score += 1

    # Technical term density
    if tech_density > 0.08:  score += 3
    elif tech_density > 0.04: score += 2
    elif tech_density > 0.01: score += 1

    # Raw tech term count
    if tech_count > 15:  score += 2
    elif tech_count > 7: score += 1

    if score >= 8:   return "high"
    elif score >= 4: return "medium"
    else:            return "low"


def compute_clarity_score(
    text: str,
    sentence_count: int,
    word_count: int,
    has_steps: bool
) -> float:
    """
    Clarity score 0–10 based on deterministic rules.
    Higher = clearer / better structured text.
    """
    score = 10.0

    # Penalize very long sentences
    if sentence_count > 0:
        avg_len = word_count / sentence_count
        if avg_len > 30: score -= 2.0
        elif avg_len > 20: score -= 1.0

    # Penalize too short (not enough info)
    if word_count < 20:  score -= 3.0
    elif word_count < 50: score -= 1.0

    # Reward structured patterns
    if has_steps: score += 1.0

    # Reward presence of key structural keywords
    structural_words = ["objective", "requirement", "input", "output", "example"]
    text_lower = text.lower()
    found = sum(1 for w in structural_words if w in text_lower)
    score += found * 0.4

    # Penalize excessive punctuation / noise
    noise = len(re.findall(r"[!?]{2,}", text))
    score -= noise * 0.5

    return round(max(0.0, min(10.0, score)), 2)


# ── Master Pipeline ────────────────────────────────────────────────────────────

def run_pipeline(
    text: str,
    file_content: Optional[bytes] = None,
    file_type: Optional[str] = None
) -> dict:
    """
    Deterministic pipeline entry point.
    Same inputs ALWAYS produce same outputs.
    """

    # Phase 1a — Combine text sources
    combined_text = text.strip()
    file_extracted_text = None

    if file_content and file_type:
        if file_type == "pdf":
            file_extracted_text = extract_text_from_pdf(file_content)
        elif file_type == "json":
            file_extracted_text = extract_text_from_json(file_content)

        if file_extracted_text and not file_extracted_text.startswith("["):
            combined_text = combined_text + "\n\n" + file_extracted_text

    # Phase 1b — Text processing
    tokens = tokenize(combined_text)
    word_count = count_words(combined_text)
    sentence_count = count_sentences(combined_text)
    keyword_freq = get_keyword_frequency(tokens)
    technical_terms = get_technical_terms(tokens)
    action_verbs = get_action_verbs(tokens)

    # Phase 1c — Structure detection
    sections_detected = detect_sections(combined_text)
    step_info = detect_step_patterns(combined_text)

    # Phase 2a — Signal extraction
    tech_density = compute_technical_density(tokens, technical_terms)
    complexity = compute_complexity(word_count, sentence_count, len(technical_terms), tech_density)
    clarity_score = compute_clarity_score(combined_text, sentence_count, word_count, step_info["has_steps"])

    # Phase 2b — Build output
    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "keyword_frequency": keyword_freq,
        "technical_terms": technical_terms,
        "action_verbs": action_verbs,
        "sections_detected": sections_detected,
        "step_patterns": step_info,
        "complexity": complexity,
        "technical_density": tech_density,
        "clarity_score": clarity_score,
        "file_processed": file_type if file_type else None,
        "file_extracted_text_preview": (
            file_extracted_text[:300] + "..." if file_extracted_text and len(file_extracted_text) > 300
            else file_extracted_text
        ),
        "signals": {
            "has_technical_content": len(technical_terms) > 0,
            "has_action_items":      len(action_verbs) > 3,
            "is_structured":         len(sections_detected) >= 2,
            "has_step_patterns":     step_info["has_steps"],
            "input_length_category": (
                "long" if word_count > 300
                else "medium" if word_count > 80
                else "short"
            ),
        }
    }
