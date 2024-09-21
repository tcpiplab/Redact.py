# Redact Sensitive Data in STDOUT

The `redact.py` script is designed to redact sensitive data enclosed within single or double quotes from text input. It will also detect and redact high entropy strings such as API tokens, cookie values, etc. It can be used to sanitize logs, outputs, or other text data that may contain sensitive information such as API keys, passwords, or other confidential values.

## Useful for pentesters

This is not exactly a security tool; it is mostly intended for redacting secrets that are discovered in plaintext files. The idea is to provide output that is suitable for your pentest report where you're telling the client to not hardcode secrets in source code and shell scripts. 

## Install and make an alias

1. Clone this repo
2. Make an alias in your environment file
    ```bash
    alias redact="~/Tools/Redact/redact.py"
    ```
3. Pipe sensitive output through it
    ```bash
    $ grep API ~/.zshrc | redact
    export GPT_API_KEY="***************************************************"
    ```

## Usage:

### Pipe text input into the script:
```bash
    $ echo 'This is "sensitive data"' | python redact.py
    This is "*************"
```

### Alternatively, provide one or more file paths as arguments:
```bash
    $ python redact.py file1.txt file2.log
```
This will read the contents of the specified files, redact any sensitive data enclosed in quotes, and print the redacted output to the console.

### Help Menu

```bash
$ redact.py --help
usage: redact.py [-h] [-R] [files ...]

Redact sensitive information from text.

positional arguments:
  files                 Files to process (if not specified, reads from stdin)

options:
  -h, --help            show this help message and exit
  -R, --REDACT, --REDACTED
                        Replace * with [REDACTED]
```

## Features

- The redaction process replaces the entire content between the outermost single or double quotes or any high entropy string. Nested quotes within the outermost quotes are preserved.
- Redacted strings are replaced with asterisks (`*`) by default.
- Redacted strings are replaced with `[REDACTED]` if you provide the `-R` or `--REDACTED` options at runtime.
- Review the redacted output carefully before sharing or storing it.


## Instead, you should actually *secure* your secrets

**IMPORTANT**: If you're using this script to redact hard-coded secrets stored in plain text files, you have a larger security problem. You should not be doing that. Instead, access the secrets from your shell scripts or Python scripts using one of the solutions listed below:

- **Environment Variables**: Store secrets as environment variables and access them in your scripts using `os.environ` in Python or `$VARIABLE` in shell scripts. Ensure that the environment variables are set securely and not exposed in logs or error messages.

- **Configuration Files with Proper Permissions**: Use configuration files (e.g., `.env` files) that are not checked into version control and have restricted permissions. Load them securely using libraries like `python-dotenv` for Python scripts.

- **Secret Management Services**:
  - **HashiCorp Vault**: A tool for securely accessing secrets via API calls with fine-grained access control.
  - **Cloud Provider Secret Managers**:
    - **AWS Secrets Manager** or **AWS Parameter Store**
    - **Azure Key Vault**
    - **Google Cloud Secret Manager**
    These services allow you to store, rotate, and access secrets securely in cloud environments.

- **Ansible Vault or Similar Tools**: If you're using configuration management tools like Ansible, use Ansible Vault to encrypt sensitive variables and data files.

- **Use of Keyring Libraries**: Utilize keyring libraries that interact with the OS's secure credential storage, such as the `keyring` library in Python.

- **Kubernetes Secrets**: If you're deploying applications on Kubernetes, use Kubernetes Secrets to manage sensitive information.

- **Docker Secrets**: When using Docker Swarm, you can use Docker Secrets to manage sensitive data that a container needs at runtime.

- **Hardware Security Modules (HSMs)**: For highly sensitive applications, consider using HSMs to store cryptographic keys and perform operations in a secure hardware environment.

- **Third-Party Secret Management Tools**:
  - **1Password Secrets Automation**
  - **Doppler**
  - **CyberArk Conjur**
  These tools provide APIs and integrations for managing secrets across different environments and applications.

Always ensure that secrets are encrypted in transit and at rest, and that access to them is logged and monitored.