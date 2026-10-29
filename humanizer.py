#!/usr/bin/env python3
"""
HUMANIZER ENGINE (v1.0)
An intelligent, modular tool to detect and humanize AI-generated text.

Features:
- Multi-tier catalogue matching (Pompous, Corporate Slop, Throat-Clearing, Transition Clichés)
- Burstiness & Sentence Length Variance analysis
- Automated dead-phrase pruning and conversational substitution
- Contraction restoration for natural human voice
"""

import re
import math
import json
from typing import Dict, List, Tuple

# ============================================================================
# CATALOGUES: EXPANDABLE RULES FOR AI IDENTIFICATION & REPLACEMENT
# ============================================================================

FILLERS_TO_PRUNE = [
    r"\bit is important to (note|remember|highlight) that\b",
    r"\bit is worth (noting|mentioning) that\b",
    r"\bin order to\b",
    r"\bat the end of the day\b",
    r"\bby leveraging the power of\b",
    r"\bplays a pivotal role in\b",
    r"\bserves as a testament to\b",
    r"\bin today's fast-paced (world|environment|digital age)\b",
    r"\bit should be noted that\b",
    r"\bit goes without saying that\b",
    r"\ball things considered\b",
]

REPLACEMENTS_MAP = {
    # Pompous academic / LLM vocabulary
    r"\bdelve into\b": "look at",
    r"\bdelves into\b": "looks at",
    r"\bdelving into\b": "looking at",
    r"\btestament to\b": "proof of",
    r"\btapestry of\b": "mix of",
    r"\bpivotal\b": "key",
    r"\bparamount\b": "top priority",
    r"\bmultifaceted\b": "complex",
    r"\brealm of\b": "field of",
    r"\bharness\b": "use",
    r"\bharnessing\b": "using",
    r"\butilize\b": "use",
    r"\butilizes\b": "uses",
    r"\butilizing\b": "using",
    r"\butilization\b": "use",
    r"\bfacilitate\b": "help",
    r"\bfacilitates\b": "helps",
    r"\bfoster\b": "build",
    r"\bfostering\b": "building",
    r"\bunderscore\b": "show",
    r"\bunderscores\b": "shows",
    r"\bunderscored\b": "showed",
    r"\belucidate\b": "explain",
    r"\bconcomitant\b": "connected",
    
    # Stiff transitions
    r"\bfurthermore,\b": "also,",
    r"\bmoreover,\b": "plus,",
    r"\bnevertheless,\b": "still,",
    r"\bnonetheless,\b": "even so,",
    r"\bconsequently,\b": "as a result,",
    r"\bsubsequently,\b": "later,",
    r"\bin conclusion,\b": "overall,",
    r"\bin summary,\b": "to wrap up,",
    r"\bultimately,\b": "in the end,",
    
    # Silicon Valley / MBA buzzwords
    r"\bscalable saas margins\b": "lean software costs",
    r"\bdigital aggregation platform\b": "booking website",
    r"\bcommercial friction points\b": "everyday hassles",
    r"\bseamlessly\b": "smoothly",
    r"\bstreamlined\b": "simple",
    r"\bparadigm shift\b": "major change",
    r"\bsynergistic\b": "collaborative",
    r"\bholistic approach\b": "complete plan",
}

CONTRACTIONS_MAP = {
    r"\bdo not\b": "don't",
    r"\bcannot\b": "can't",
    r"\bwill not\b": "won't",
    r"\bdoes not\b": "doesn't",
    r"\bis not\b": "isn't",
    r"\bare not\b": "aren't",
    r"\bwe are\b": "we're",
    r"\bthey are\b": "they're",
    r"\bit is\b": "it's",
    r"\bthat is\b": "that's",
    r"\bthere is\b": "there's",
    r"\bwe have\b": "we've",
    r"\byou have\b": "you've",
}


# ============================================================================
# ANALYSIS & HUMANIZATION LOGIC
# ============================================================================

class TextHumanizer:
    def __init__(self, custom_replacements: Dict[str, str] = None):
        self.replacements = dict(REPLACEMENTS_MAP)
        if custom_replacements:
            self.replacements.update(custom_replacements)

    def split_sentences(self, text: str) -> List[str]:
        """Split text into sentences while preserving structure."""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]

    def calculate_burstiness(self, text: str) -> Tuple[float, float, str]:
        """
        Calculate sentence length variance (Burstiness).
        Low variance (< 4) = Metronomic robotic rhythm.
        High variance (> 8) = Natural, rhythmic human voice.
        """
        sentences = self.split_sentences(text)
        if len(sentences) < 2:
            return 0.0, 0.0, "Insufficient text to measure cadence"
        
        lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
        avg_len = sum(lengths) / len(lengths)
        variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
        std_dev = math.sqrt(variance)

        if std_dev < 4.0:
            cadence = "Monotonous / Robotic (Low Burstiness - all sentences similar length)"
        elif std_dev < 7.5:
            cadence = "Moderate Flow (Acceptable, but could use punchier rhythm)"
        else:
            cadence = "Dynamic / Human-like (High Burstiness - great variety in sentence length)"

        return round(std_dev, 2), round(avg_len, 1), cadence

    def scan_buzzwords(self, text: str) -> List[Dict]:
        """Detect all AI buzzwords and fillers with character positions."""
        flagged = []
        words = re.findall(r'\b\w+\b', text)
        total_words = max(len(words), 1)

        # 1. Scan Fillers
        for pattern in FILLERS_TO_PRUNE:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                flagged.append({
                    "matched": match.group(0),
                    "type": "Throat-Clearing Filler",
                    "suggestion": "Delete entirely (Zero-calorie phrase)",
                    "span": match.span()
                })

        # 2. Scan Replacements
        for pattern, replacement in self.replacements.items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                flagged.append({
                    "matched": match.group(0),
                    "type": "AI Buzzword / Cliché",
                    "suggestion": f"Replace with '{replacement}'",
                    "span": match.span()
                })

        return flagged

    def humanize(self, text: str, apply_contractions: bool = True) -> Dict:
        """
        Humanize input text by pruning dead fillers, substituting buzzwords,
        and restoring natural conversational contractions.
        """
        original_text = text
        working_text = text
        changes_made = []

        # Step 1: Prune Throat-Clearing Fillers
        for pattern in FILLERS_TO_PRUNE:
            matches = list(re.finditer(pattern, working_text, re.IGNORECASE))
            if matches:
                for match in matches:
                    changes_made.append(f"Pruned filler: '{match.group(0)}'")
                # Clean replacement (handle leading capitalization if needed)
                working_text = re.sub(pattern + r"\s*", "", working_text, flags=re.IGNORECASE)

        # Step 2: Replace AI Clichés and Buzzwords
        for pattern, rep in self.replacements.items():
            matches = list(re.finditer(pattern, working_text, re.IGNORECASE))
            if matches:
                for match in matches:
                    # Match casing of original word
                    original_word = match.group(0)
                    replacement_word = rep
                    if original_word.istitle():
                        replacement_word = rep.capitalize()
                    elif original_word.isupper():
                        replacement_word = rep.upper()
                    
                    changes_made.append(f"Replaced: '{original_word}' -> '{replacement_word}'")
                    working_text = re.sub(pattern, replacement_word, working_text, count=1, flags=re.IGNORECASE)

        # Step 3: Inject Natural Contractions (Optional for formal vs casual)
        if apply_contractions:
            for pattern, contraction in CONTRACTIONS_MAP.items():
                if re.search(pattern, working_text, re.IGNORECASE):
                    working_text = re.sub(pattern, contraction, working_text, flags=re.IGNORECASE)
                    changes_made.append(f"Applied contraction: '{contraction}'")

        # Step 4: Cleanup double spaces or weird punctuation
        working_text = re.sub(r'\s+', ' ', working_text)
        working_text = re.sub(r'\s+([,.;!?])', r'\1', working_text)
        # Capitalize sentence starts if a filler removal lowered the case
        working_text = re.sub(r'(^|[.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), working_text)

        # Metrics
        std_dev, avg_len, cadence = self.calculate_burstiness(working_text)
        total_words = len(re.findall(r'\b\w+\b', original_text))
        flagged_count = len(self.scan_buzzwords(original_text))
        ai_density = round((flagged_count / max(total_words, 1)) * 100, 1)

        return {
            "original": original_text,
            "humanized": working_text,
            "ai_density_score": f"{ai_density}%",
            "burstiness_index": std_dev,
            "avg_sentence_length": avg_len,
            "cadence_feedback": cadence,
            "total_edits": len(changes_made),
            "changes": changes_made
        }


# ============================================================================
# CLI INTERFACE
# ============================================================================
if __name__ == "__main__":
    sample_ai_text = (
        "Furthermore, it is important to note that our digital aggregation platform "
        "delves into commercial friction points to seamlessly foster scalable SaaS margins. "
        "Moreover, this serves as a testament to the multifaceted realm of modern technology. "
        "In order to facilitate growth, we utilize a holistic approach that underscores efficiency."
    )

    print("=" * 70)
    print("🔍 AI HUMANIZER ENGINE — RUNNING SAMPLE TEST")
    print("=" * 70)
    print("\n[ORIGINAL AI TEXT]:")
    print(sample_ai_text)

    humanizer = TextHumanizer()
    result = humanizer.humanize(sample_ai_text)

    print("\n" + "-" * 70)
    print("[HUMANIZED RESULT]:")
    print(result["humanized"])
    print("-" * 70)
    print(f"📊 AI Density Score:   {result['ai_density_score']}")
    print(f"📈 Burstiness (Cadence): {result['burstiness_index']} ({result['cadence_feedback']})")
    print(f"✂️ Edits Performed:     {result['total_edits']}")
    print("\n[CHANGES LOG]:")
    for change in result["changes"]:
        print(f" • {change}")
    print("=" * 70)
