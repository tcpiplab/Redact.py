#!/usr/bin/env python3

import sys

def redact_text(text):
    result = ''
    quote_stack = []
    redacting = False
    for i, c in enumerate(text):
        if c == "'" or c == '"':
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
        else:
            result += c
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