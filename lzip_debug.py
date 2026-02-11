#!/usr/bin/env python3
"""
L-ZIP Debug/Verbose Mode
Shows step-by-step transformation logic with detailed logging
"""

import re
import sys
from datetime import datetime
from typing import Dict, List, Tuple
from lzip import LZIPTranslator, LZIPConfig


class LZIPDebugger:
    """Debug wrapper for L-ZIP translator with verbose logging"""
    
    def __init__(self, log_to_file: bool = True, verbose: bool = True):
        self.translator = LZIPTranslator()
        self.verbose = verbose
        self.log_to_file = log_to_file
        self.log_entries = []
        
        if log_to_file:
            self.log_filename = f"lzip_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message to terminal and/or file"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.log_entries.append(log_entry)
        
        if self.verbose:
            print(log_entry)
    
    def save_log(self):
        """Save all log entries to file"""
        if self.log_to_file and self.log_entries:
            with open(self.log_filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.log_entries))
            self.log(f"Log saved to: {self.log_filename}", "SAVE")
    
    def debug_translate(self, prompt: str) -> Tuple[str, Dict]:
        """Translate with full debug output"""
        
        self.log("=" * 80, "START")
        self.log("L-ZIP DEBUG MODE ACTIVATED", "START")
        self.log("=" * 80, "START")
        self.log("")
        
        # Step 1: Show original
        self.log("STEP 1: ORIGINAL PROMPT", "STEP")
        self.log("-" * 80)
        self.log(f"Text: {prompt}", "INPUT")
        self.log(f"Length: {len(prompt.split())} words", "STAT")
        self.log(f"Estimated tokens: ~{len(prompt) // 4}", "STAT")
        self.log("")
        
        # Step 2: Lowercase conversion
        self.log("STEP 2: PREPROCESSING", "STEP")
        self.log("-" * 80)
        original = prompt
        processed = prompt.lower()
        self.log(f"Action: Convert to lowercase", "TRANSFORM")
        self.log(f"Before: {original[:100]}...", "BEFORE")
        self.log(f"After:  {processed[:100]}...", "AFTER")
        self.log("")
        
        # Step 3: Clean text
        self.log("STEP 3: CLEANING TEXT", "STEP")
        self.log("-" * 80)
        before_clean = processed
        processed = self._debug_clean_text(processed)
        if before_clean != processed:
            self.log(f"Action: Remove extra whitespace and punctuation", "TRANSFORM")
            self.log(f"Before: {before_clean[:100]}...", "BEFORE")
            self.log(f"After:  {processed[:100]}...", "AFTER")
        else:
            self.log("No cleaning needed", "INFO")
        self.log("")
        
        # Step 4: Compress phrases
        self.log("STEP 4: PHRASE COMPRESSION", "STEP")
        self.log("-" * 80)
        before_compress = processed
        processed = self._debug_compress_phrases(processed)
        if before_compress != processed:
            self.log(f"Before: {before_compress[:100]}...", "BEFORE")
            self.log(f"After:  {processed[:100]}...", "AFTER")
        else:
            self.log("No phrases compressed", "INFO")
        self.log("")
        
        # Step 5: Extract operators
        self.log("STEP 5: OPERATOR EXTRACTION", "STEP")
        self.log("-" * 80)
        lzip_parts = self._debug_extract_operators(processed)
        self.log(f"Extracted {len(lzip_parts)} operator(s)", "STAT")
        for i, part in enumerate(lzip_parts, 1):
            self.log(f"  {i}. {part}", "OPERATOR")
        self.log("")
        
        # Step 6: Build final L-ZIP
        self.log("STEP 6: BUILDING FINAL L-ZIP", "STEP")
        self.log("-" * 80)
        if lzip_parts:
            final_lzip = ' '.join(lzip_parts)
            self.log(f"Action: Join {len(lzip_parts)} parts with spaces", "TRANSFORM")
        else:
            final_lzip = processed[:100] if processed else "UNCLASSIFIED"
            self.log("Action: No operators found, using truncated text", "TRANSFORM")
        
        self.log(f"Final L-ZIP: {final_lzip}", "OUTPUT")
        self.log("")
        
        # Step 7: Calculate stats
        self.log("STEP 7: COMPRESSION STATISTICS", "STEP")
        self.log("-" * 80)
        
        original_words = len(prompt.split())
        final_words = len(final_lzip.split())
        original_tokens = len(prompt) // 4
        final_tokens = len(final_lzip) // 4
        compression_ratio = round((1 - final_tokens / max(original_tokens, 1)) * 100, 1)
        tokens_saved = original_tokens - final_tokens
        
        self.log(f"Original: {original_words} words ({original_tokens} tokens)", "STAT")
        self.log(f"Compressed: {final_words} words ({final_tokens} tokens)", "STAT")
        self.log(f"Tokens saved: {tokens_saved}", "STAT")
        self.log(f"Compression: {compression_ratio}%", "STAT")
        
        # Calculate efficiency
        if compression_ratio >= 70:
            efficiency = "EXCELLENT"
        elif compression_ratio >= 50:
            efficiency = "GOOD"
        elif compression_ratio >= 30:
            efficiency = "FAIR"
        else:
            efficiency = "LOW"
        
        self.log(f"Efficiency: {efficiency}", "STAT")
        self.log("")
        
        # Step 8: Summary
        self.log("STEP 8: TRANSFORMATION SUMMARY", "STEP")
        self.log("-" * 80)
        self.log("Transformations applied:", "SUMMARY")
        self.log("  ✓ Lowercase conversion", "SUMMARY")
        self.log("  ✓ Text cleaning", "SUMMARY")
        self.log("  ✓ Phrase compression", "SUMMARY")
        self.log(f"  ✓ Operator extraction ({len(lzip_parts)} found)", "SUMMARY")
        self.log("")
        
        self.log("=" * 80, "END")
        self.log("DEBUG SESSION COMPLETE", "END")
        self.log("=" * 80, "END")
        
        metadata = {
            'original_length': original_words,
            'original_tokens': original_tokens,
            'final_length': final_words,
            'final_tokens': final_tokens,
            'compression_ratio': compression_ratio,
            'tokens_saved': tokens_saved,
            'efficiency': efficiency
        }
        
        if self.log_to_file:
            self.save_log()
        
        return final_lzip, metadata
    
    def _debug_clean_text(self, text: str) -> str:
        """Clean text with logging"""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', text)
        cleaned = cleaned.strip()
        
        # Remove some punctuation
        cleaned = re.sub(r'[.,;!?]+\s*', ' ', cleaned)
        
        return cleaned
    
    def _debug_compress_phrases(self, text: str) -> str:
        """Compress common phrases with logging"""
        compressed = text
        changes = []
        
        # Remove filler words
        fillers = [
            (r'\bplease\b', '', 'Removed "please"'),
            (r'\bi need you to\b', '', 'Removed "I need you to"'),
            (r'\bcan you\b', '', 'Removed "can you"'),
            (r'\bcould you\b', '', 'Removed "could you"'),
            (r'\byou should\b', '', 'Removed "you should"'),
            (r'\bmake sure\b', '', 'Removed "make sure"'),
        ]
        
        for pattern, replacement, description in fillers:
            if re.search(pattern, compressed, re.IGNORECASE):
                compressed = re.sub(pattern, replacement, compressed, flags=re.IGNORECASE)
                changes.append(description)
                self.log(f"  → {description}", "COMPRESS")
        
        # Clean up extra spaces
        compressed = re.sub(r'\s+', ' ', compressed).strip()
        
        if not changes:
            self.log("  → No filler words found", "INFO")
        
        return compressed
    
    def _debug_extract_operators(self, text: str) -> List[str]:
        """Extract operators with detailed logging"""
        operators = []
        
        # Look for OBJ (objective)
        self.log("Searching for OBJ (Objective)...", "SEARCH")
        obj_patterns = [
            (r'(?:write|create|generate|develop)\s+a?\s+([a-z][a-z\s]{2,50}?)(?:\s+that|\s+to|\s+for|$)', 1, 'write/create pattern'),
            (r'function\s+(?:that\s+)?([a-z][a-z\s]{2,50}?)(?:\s+with|\s+to|$)', 1, 'function pattern'),
        ]
        
        for pattern, group, desc in obj_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                objective = match.group(group).strip()
                objective = re.sub(r'\s+', '_', objective)
                objective = objective[:50]  # Limit length
                operators.append(f'OBJ:{objective}')
                self.log(f"  ✓ Found OBJ via {desc}: '{objective}'", "FOUND")
                break
        else:
            self.log("  ✗ No OBJ pattern matched", "NOTFOUND")
        
        # Look for OUT (output format)
        self.log("Searching for OUT (Output)...", "SEARCH")
        out_keywords = ['docstring', 'type hints', 'test suite', 'implementation', 'complete']
        found_outputs = []
        
        for keyword in out_keywords:
            if keyword in text:
                found_outputs.append(keyword.replace(' ', '+'))
                self.log(f"  ✓ Found output requirement: '{keyword}'", "FOUND")
        
        if found_outputs:
            operators.append(f'OUT:{"+".join(found_outputs)}')
        else:
            self.log("  ✗ No output keywords found", "NOTFOUND")
        
        # Look for GEN (generation type)
        self.log("Searching for GEN (Generate)...", "SEARCH")
        if re.search(r'\bfunction\b', text, re.IGNORECASE):
            operators.append('GEN:Function')
            self.log("  ✓ Found generation type: Function", "FOUND")
        elif re.search(r'\bclass\b', text, re.IGNORECASE):
            operators.append('GEN:Class')
            self.log("  ✓ Found generation type: Class", "FOUND")
        elif re.search(r'\bscript\b', text, re.IGNORECASE):
            operators.append('GEN:Script')
            self.log("  ✓ Found generation type: Script", "FOUND")
        else:
            self.log("  ✗ No generation type found", "NOTFOUND")
        
        # Look for ACT (actor/role)
        self.log("Searching for ACT (Actor)...", "SEARCH")
        act_patterns = [
            (r'(?:act as|role|be)\s+(?:a\s+)?([a-z\s]{2,30}?)(?:\s+and|\s+who|$)', 1, 'direct role'),
            (r'(senior|expert|professional)\s+([a-z]+)', 2, 'expertise level'),
        ]
        
        for pattern, group, desc in act_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                role = match.group(group).strip()
                role = re.sub(r'\s+', '_', role)
                operators.insert(0, f'ACT:{role}')  # ACT goes first
                self.log(f"  ✓ Found ACT via {desc}: '{role}'", "FOUND")
                break
        else:
            self.log("  ✗ No ACT pattern matched", "NOTFOUND")
        
        return operators


def main():
    """Run debug session"""
    import sys
    
    # Check args
    if len(sys.argv) > 1:
        prompt = ' '.join(sys.argv[1:])
    else:
        # Default test prompts
        prompt = input("Enter prompt to debug (or press Enter for default): ").strip()
        
        if not prompt:
            prompt = "I need you to write a Python function that validates email addresses. The function should check for proper format, handle edge cases, and include comprehensive error handling. Please provide the complete implementation with docstring, type hints, and a full test suite covering all edge cases."
    
    debugger = LZIPDebugger(log_to_file=True, verbose=True)
    lzip_result, metadata = debugger.debug_translate(prompt)
    
    print("\n" + "=" * 80)
    print("FINAL RESULT")
    print("=" * 80)
    print(f"L-ZIP: {lzip_result}")
    print(f"Log file: {debugger.log_filename if debugger.log_to_file else 'N/A'}")
    print("=" * 80)


if __name__ == "__main__":
    main()
