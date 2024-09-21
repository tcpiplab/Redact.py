#!/usr/bin/env python3

import sys
import math
import re
import argparse


def calculate_entropy(string):
    """Calculate the Shannon entropy of a string."""
    # Get probability of chars in string
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    # Calculate the entropy
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy


def redact_text(text, entropy_threshold=4.5):
    # Threshold of 4.5 seems to be ideal
    result = ''
    quote_stack = []
    redacting = False
    current_word = ''
    
    for i, c in enumerate(text):
        if c == "'" or c == '"':
            if current_word:
                # Check entropy of the current word before starting a new quote
                if calculate_entropy(current_word) > entropy_threshold:
                    result += '*' * len(current_word)
                else:
                    result += current_word
                current_word = ''
            
            if not quote_stack:
                # Start of outermost quoted string
                quote_stack.append(c)
                redacting = True
                result += c
            elif quote_stack[-1] == c:
                # End of outermost quoted string
                quote_stack.pop()
                redacting = False
                result += c
            else:
                # Start of nested quoted string
                quote_stack.append(c)
                result += c
        elif redacting:
            # Replace content with '*' if inside outermost quotes
            result += '*'
        elif c.isspace():
            # End of a word, check its entropy
            if current_word:
                if calculate_entropy(current_word) > entropy_threshold:
                    result += '*' * len(current_word)
                else:
                    result += current_word
                current_word = ''
            result += c
        else:
            current_word += c
    
    # Check the last word if exists
    if current_word:
        if calculate_entropy(current_word) > entropy_threshold:
            result += '*' * len(current_word)
        else:
            result += current_word
    
    return result


def final_redaction(text):
    """Replace any string of two or more * with [REDACTED]"""
    return re.sub(r'\*{2,}', '[REDACTED]', text)


def main():
    parser = argparse.ArgumentParser(description="Redact sensitive information from text.")
    parser.add_argument('-R', '--REDACT', '--REDACTED', action='store_true', help="Replace * with [REDACTED]")
    parser.add_argument('files', nargs='*', help="Files to process (if not specified, reads from stdin)")
    args = parser.parse_args()

    def process_line(line):
        redacted_line = redact_text(line.rstrip('\n'))
        if args.REDACT:
            redacted_line = final_redaction(redacted_line)
        print(redacted_line)

    if args.files:
        # Read from file(s) specified as arguments
        for filename in args.files:
            try:
                with open(filename, 'r') as f:
                    for line in f:
                        process_line(line)
            except FileNotFoundError:
                print(f"File not found: {filename}", file=sys.stderr)
    else:
        # Read from stdin
        for line in sys.stdin:
            process_line(line)

if __name__ == '__main__':
    main()