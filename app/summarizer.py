import os
import json
import datetime
import re
import unicodedata

from app.utils import extract_text_per_page
from app.pattern_engine import detect_patterns, rank_section
from app.config import SUMMARY_CHAR_LIMIT

INPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../input"))
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../output"))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "round1b_output.json")


def clean_text(text):
    text = re.sub(r'(?i)ieee transactions.*?\n', '', text)
    text = re.sub(r'(?i)preprint.*?\n', '', text)
    text = re.sub(r'\n+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def summarize_text(text):
    normalized = unicodedata.normalize("NFKD", text)
    cleaned = clean_text(normalized)
    informative = [s for s in cleaned.split('. ') if len(s.split()) > 5]
    text = '. '.join(informative)
    return text[:SUMMARY_CHAR_LIMIT] + "..." if len(text) > SUMMARY_CHAR_LIMIT else text


def extract_summary_insight(summary):
    sentences = summary.split('. ')
    for s in sentences:
        if len(s.split()) >= 6:
            return s.strip() + ('.' if not s.endswith('.') else '')
    return summary.strip()


def calculate_relevance_score(title, keywords):
    matches = sum(1 for kw in keywords if kw.lower() in title.lower())
    return round(matches / len(keywords), 2) if keywords else 0.0


def process_documents():
    output = {
        "metadata": {
            "input_documents": os.listdir(INPUT_DIR),
            "persona": "Research Assistant",
            "job_to_be_done": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks",
            "processing_timestamp": datetime.datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    job = output["metadata"]["job_to_be_done"].lower()

    if "literature review" in job:
        category_keywords = {
            "methodologies": ["method", "approach", "architecture", "technique"],
            "datasets": ["data", "dataset", "corpus", "benchmark", "evaluation"],
            "performance_benchmarks": ["result", "performance", "accuracy", "comparison", "metrics"]
        }
    elif "revenue" in job or "financial" in job:
        category_keywords = {
            "revenue_trends": ["revenue", "income", "sales"],
            "rnd_investments": ["research", "r&d", "development", "innovation"],
            "market_positioning": ["market", "strategy", "position", "competition"]
        }
    elif "exam preparation" in job or "study" in job:
        category_keywords = {
            "key_concepts": ["concept", "definition", "principle"],
            "mechanisms": ["mechanism", "reaction", "process", "pathway"],
            "examples": ["example", "illustration", "case study"]
        }
    else:
        category_keywords = {
            "general_insights": ["introduction", "summary", "overview", "conclusion"]
        }

    print("📂 Starting document processing...")
    print(f"📝 Found {len(output['metadata']['input_documents'])} document(s): {output['metadata']['input_documents']}")

    seen = set()
    skipped_sections = []

    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith(".pdf"):
            continue
        print(f"\n📄 Processing: {filename}")
        path = os.path.join(INPUT_DIR, filename)
        pages = extract_text_per_page(path)

        for page_num, text in pages:
            if (filename, page_num) in seen:
                continue
            seen.add((filename, page_num))

            lines = text.splitlines()
            for i, line in enumerate(lines):
                clean_title = unicodedata.normalize("NFKD", line.strip())

                if len(clean_title.split()) > 10 or len(clean_title) < 3:
                    continue
                if not re.match(r"^\d{1,2}(\.\d{1,2})?\.?\s+[A-Z]", clean_title) and clean_title.upper() != clean_title:
                    continue

                rank = rank_section(clean_title)
                if rank <= 2:
                    context = " ".join(lines[i:i+10])
                    summary = summarize_text(context)
                    summary_insight = extract_summary_insight(summary)
                    added = False

                    for category, keywords in category_keywords.items():
                        matched_keywords = [kw for kw in keywords if kw.lower() in clean_title.lower()]
                        if matched_keywords:
                            reason = f"Matched keyword(s): {', '.join(matched_keywords)} — relevant to {category.replace('_', ' ')}."
                            relevance_score = calculate_relevance_score(clean_title, keywords)
                            output["subsection_analysis"].append({
                                "document": filename,
                                "section_title": clean_title,
                                "refined_text": summary,
                                "page_number": page_num,
                                "reason": reason,
                                "summary_insight": summary_insight,
                                "relevance_score": relevance_score
                            })
                            output["extracted_sections"].append({
                                "document": filename,
                                "page_number": page_num,
                                "section_title": clean_title,
                                "importance_rank": rank
                            })
                            added = True
                            break

                    # SKIP adding if no keywords matched (clean output)
                    if not added:
                        skipped_sections.append(f"{filename} → {clean_title}")
                        continue

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)
        print(f"\n🎯 Summary JSON saved to: {OUTPUT_FILE}")

    # Print skipped/irrelevant sections
    if skipped_sections:
        print("\n\033[92m🟢 Skipped Sections (No matched keywords or low relevance):\033[0m")
        for s in skipped_sections:
            print(f"  - {s}")
    else:
        print("\n\033[92m🟢 All extracted sections were matched and scored.\033[0m")


if __name__ == "__main__":
    process_documents()
