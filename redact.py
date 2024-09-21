#!/usr/bin/env python3

import sys
import math

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


def main():
    if len(sys.argv) > 1:
        # Read from file(s) specified as arguments
        for filename in sys.argv[1:]:
            try:
                with open(filename, 'r') as f:
                    for line in f:
                        redacted_line = redact_text(line.rstrip('\n'))
                        print(redacted_line)
            except FileNotFoundError:
                print(f"File not found: {filename}", file=sys.stderr)
    else:
        # Read from stdin
        for line in sys.stdin:
            redacted_line = redact_text(line.rstrip('\n'))
            print(redacted_line)

if __name__ == '__main__':
    main()