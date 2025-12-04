# reviews/views.py
import os
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .forms import CodeUploadForm
from .models import ReviewReport

# Use google genai SDK but DO NOT create Client() at import time
from google import genai

REVIEW_PROMPT_TEMPLATE = (
    "You are an expert senior software engineer and code reviewer.\n"
    "Analyze the following source code for readability, modularity, maintainability, potential bugs, security issues, and performance pitfalls.\n"
    "Provide: (1) Short summary, (2) Line-by-line important issues (if any), (3) Suggested improvements, (4) Example refactor or code snippet if appropriate.\n\n"
    "Language hint: {language_hint}\n\n"
    "Code:\n\n{code}\n"
)


def _create_genai_client():
    """Create and return genai.Client(api_key=...) if key exists, else None."""
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GENAI_API_KEY")
    if not key:
        return None
    try:
        return genai.Client(api_key=key)
    except Exception:
        # If client creation fails, return None and let caller handle fallback
        return None


import json
import re

def call_llm_for_review(code: str, language_hint: str = "") -> str:
    """
    Call Google Gen AI (Gemini) and return a *cleanly formatted* textual review.
    This version tries to parse a JSON object from the model output (preferred).
    If JSON is present and valid, it converts it to a neat plain-text format.
    Otherwise it strips common markdown (**, `, #, etc.) and returns cleaned text.
    """
    prompt = REVIEW_PROMPT_TEMPLATE.format(
        language_hint=language_hint or "unspecified", code=code
    )

    client = _create_genai_client()
    if client is None:
        return (
            "Gemini API key not configured or client creation failed. Please set GEMINI_API_KEY (or GOOGLE_API_KEY) in your environment.\n\n"
            "Fallback checklist:\n"
            "- Readability: check variable and function names\n"
            "- Comments: ensure important blocks have comments\n            "
            "- Modularization: extract large functions into smaller units\n"
            "- Security: validate and sanitize inputs\n"
            "- Performance: look for repeated work inside loops\n"
        )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        raw = getattr(response, "text", None) or str(response)
    except Exception as e:
        return (
            f"LLM call to Gemini failed: {e}\n\n"
            "Fallback checklist:\n"
            "- Readability: check variable names\n"
            "- Comments: check presence of comments\n"
            "- Modularization: check long functions\n"
            "- Security: check for unsafe input handling\n"
        )

    raw = raw.strip()

    # 1) Try direct JSON parse
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return _format_parsed_review(parsed)
    except Exception:
        pass

    # 2) Try to extract JSON substring and parse
    sub = _extract_json_substring(raw)
    if sub:
        try:
            parsed = json.loads(sub)
            if isinstance(parsed, dict):
                return _format_parsed_review(parsed)
        except Exception:
            pass

    # 3) Fallback: clean markdown-like chars and return readable text
    return _cleanup_markdown(raw)


def _format_parsed_review(parsed: dict) -> str:
    """Convert structured JSON review into a clean plain-text report."""
    lines = []

    summary = parsed.get("summary") or parsed.get("Summary") or ""
    if summary:
        lines.append("SUMMARY:")
        lines.append(summary.strip())
        lines.append("")

    issues = parsed.get("issues") or []
    if issues:
        lines.append("ISSUES:")
        for it in issues:
            if isinstance(it, dict):
                line_no = it.get("line")
                msg = it.get("message", "")
            else:
                line_no = None
                msg = str(it)
            if line_no:
                lines.append(f"  - Line {line_no}: {msg.strip()}")
            else:
                lines.append(f"  - {msg.strip()}")
        lines.append("")

    suggestions = parsed.get("suggestions") or []
    if suggestions:
        lines.append("SUGGESTIONS:")
        for s in suggestions:
            lines.append(f"  - {str(s).strip()}")
        lines.append("")

    refactor = parsed.get("refactor")
    if refactor:
        lines.append("REFACTOR EXAMPLE:")
        code = str(refactor).strip()
        # remove stray code fences/backticks
        code = code.strip("`")
        lines.append(code)
        lines.append("")

    return "\n".join(lines).strip()


def _extract_json_substring(s: str) -> str | None:
    """Find first balanced JSON object substring in s, return it or None."""
    start = s.find("{")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[start:i + 1]
    return None


def _cleanup_markdown(text: str) -> str:
    """Remove common markdown/formatting markers to return readable plain text."""
    # remove bold/italic markers **text** or __text__
    text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text, flags=re.DOTALL)
    # remove single * or _ emphasis
    text = re.sub(r"(?<!\*)\*(?!\*)(.*?)\*(?<!\*)", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"(?<!_)_(?!_)(.*?)_(?<!_)", r"\1", text, flags=re.DOTALL)
    # remove inline code/backticks
    text = text.replace("`", "")
    # remove markdown headings like ### Title
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    # collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

@require_http_methods(["GET", "POST"])
def upload_code(request):
    if request.method == "POST":
        form = CodeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data["file"]
            language_hint = form.cleaned_data.get("language_hint", "")
            content_bytes = f.read()
            try:
                code_text = content_bytes.decode("utf-8")
            except UnicodeDecodeError:
                code_text = content_bytes.decode("latin-1")

            report = ReviewReport.objects.create(
                filename=f.name,
                code_content=code_text,
            )

            # Call Gemini (synchronously) and save result
            review_text = call_llm_for_review(code_text, language_hint)
            report.review_text = review_text
            report.save()

            return redirect("reviews:view_report", pk=report.pk)
    else:
        form = CodeUploadForm()

    return render(request, "reviews/upload.html", {"form": form})


def view_report(request, pk):
    report = get_object_or_404(ReviewReport, pk=pk)
    return render(request, "reviews/report.html", {"report": report})
