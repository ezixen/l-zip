#!/usr/bin/env python3
from lzip import LZIPTranslator

translator = LZIPTranslator()

prompt = (
    "Act as a senior Python developer. Your objective is to write a robust "
    "error handling script that processes user input. Limit the output to "
    "under 100 lines of code. The output should be formatted as a complete, "
    "production-ready Python script."
)

# Run the actual translation
lzip, meta = translator.translate_to_lzip(prompt)

print("L-ZIP Output:")
print(lzip)
print(f"\nCompression: {meta['compression_ratio']}%")
print(f"\nOperators:")
print(f"  ACT: {'ACT:' in lzip}")
print(f"  OBJ: {'OBJ:' in lzip}")
print(f"  LIM: {'LIM:' in lzip}")
print(f"  OUT: {'OUT:' in lzip}")

# Now let's add some debugging to _extract_operators
import re

def debug_extract_operators(text):
    """Debug version of _extract_operators"""
    operators = []
    remaining = text
    
    print("\n\n=== DEBUG EXTRACT OPERATORS ===")
    print(f"Starting text: {remaining[:100]}...")
    
    # ACT extraction
    act_patterns = [
        (r'(?:act as|role|persona|assume|be a?)\s+([a-z\s]{2,30}?)(?:[.,;]|and|then|who|that)', 1),
        (r'\b(senior|expert|professional|experienced)\s+([a-z]+)(?:\s+(developer|engineer|architect|analyst))?', 2),
    ]
    
    for pattern, group in act_patterns:
        try:
            match = re.search(pattern, remaining, re.IGNORECASE)
            if match:
                role = match.group(group).strip()[:40]
                print(f"\nACT matched: {match.group(0)}")
                if len(role) > 1:
                    operators.append(f'ACT:{role}')
                    old_remaining = remaining
                    remaining = remaining[:match.start()] + ' ' + remaining[match.end():]
                    print(f"Remaining after ACT: {remaining[:100]}...")
                    break
        except:
            pass
    
    # OBJ extraction - let's check if it matches
    obj_patterns = [
        (r'(?:your\s+)?(?:objective|goal)\s+(?:is\s+)?(?:to\s+)?([a-z0-9_\s]{2,50}?)(?:\.|,|;|and|$)', 1),
        (r'(?<!to\s)(?:write|create|generate|produce|develop|design)\s+([a-z0-9_\s]{2,50}?)(?:\.|,|;|and)', 1),
    ]
    
    print(f"\nChecking OBJ patterns on remaining text:")
    for i, (pattern, group) in enumerate(obj_patterns):
        match = re.search(pattern, remaining, re.IGNORECASE)
        if match:
            print(f"  Pattern {i}: MATCHED - '{match.group(0)}'")
            print(f"    Group {group}: '{match.group(group)}'")
        else:
            print(f"  Pattern {i}: no match")

debug_extract_operators(prompt.lower())
