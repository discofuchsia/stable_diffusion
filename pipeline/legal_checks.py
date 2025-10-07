##############################################################################
# pipeline/legal_checks.py — Simple wildcard-based prohibited-term flags
# Example patterns: 'free*', 'guarantee*', 'best price'
##############################################################################
import re
from typing import List

def run_legal_checks(message: str, prohibited_patterns: List[str]) -> List[str]:
    flags = []
    for pat in prohibited_patterns:
        # Convert '*' into a regex wildcard; anchor with ^...$ for token match
        rx = re.compile("^" + pat.replace("*", ".*") + "$", re.IGNORECASE)

        # Tokenize words to avoid false positives inside longer words
        tokens = re.findall(r"[A-Za-z0-9']+", message)
        for t in tokens:
            if rx.match(t):
                flags.append(f"prohibited:{pat}")
                break
    return flags
