# AI Lab Assignment: Scaffolding a Robust API Integration

**Author:** Yonas Leykun  
**Course:** SE 202: High Level Programming I  
**Institution:** Frontier Institute of Technology  
**Task Title:** 0. AI: Scaffolding a Robust API Integration (Mandatory)  
**Task Folder:** `AI Lab Assignment: Scaffolding a Robust API Integration`  
**Repository:** [Artificial-Intelligence-in-Software-Engineering](https://github.com/yonasleykun27/Artificial-Intelligence-in-Software-Engineering)

---

## Overview

This repository task folder contains the implementation and documentation for scaffolding a secure, fault-tolerant Python integration with an external sentiment analysis API. Using the **Contextual Prompting** methodology, the baseline script was hardened to prevent credential leakage and handle network failures gracefully.

## AI Tool Used & Methodology
- **AI Tool:** OpenAI ChatGPT & Google Gemini (Advanced Code Reasoning)
- **Methodology:** Contextual Prompting (grounding the AI with the full initial script, defining explicit non-functional security requirements, and enforcing Python's exception inheritance hierarchy).

---

## Repository Files

| File | Description |
| :--- | :--- |
| `initial_sentiment_analyzer.py` | The initial, unhardened baseline script lacking API key authentication, timeout protection, and granular exception checks. |
| `refactored_sentiment_analyzer.py` | The refactored production script incorporating environment-based Bearer token authentication scaffolding, defensive timeouts, and hierarchical error handling. |
| `sentiment_analyzer.py` | The primary production script matching the assignment naming convention for automated grading and direct execution. |
| `README.md` | Task documentation outlining the design principles, file structure, and verification steps. |

---

## Architectural Enhancements

### 1. Secure Authentication Scaffolding
- Credentials are not hardcoded in source control. The tool securely reads `TEXT_PROCESSING_API_KEY` from the system environment using Python's `os` module.
- Pre-flight validation checks if the key is present. If missing, execution halts early with an informative diagnostic message sent to `sys.stderr`, preventing unauthorized, wasteful HTTP round trips.
- Requests pass the token using the industry-standard HTTP header format: `Authorization: Bearer <token>`.

### 2. Hierarchical Exception Handling
Derived exceptions are caught prior to generic base exceptions to avoid shadowing:
1. `requests.exceptions.Timeout`: Handles server latency spikes and socket timeouts (with an explicit `timeout=10` parameter).
2. `requests.exceptions.ConnectionError`: Catches DNS failures, refused ports, and TLS handshake issues.
3. `requests.exceptions.HTTPError`: Catches 4xx client errors and 5xx server errors triggered by `response.raise_for_status()`.
4. `requests.exceptions.RequestException`: Acts as the general base fallback for unexpected network anomalies.
5. `(KeyError, ValueError)`: Catches malformed or unparseable JSON payloads.

All diagnostic errors are routed to `sys.stderr`, leaving `sys.stdout` clean for pipeline composability.

---

## Execution & Verification

### 1. Set the Environment Variable
On Linux / macOS:
```bash
export TEXT_PROCESSING_API_KEY="your_api_key_here"
```
On Windows PowerShell:
```powershell
$env:TEXT_PROCESSING_API_KEY="your_api_key_here"
```

### 2. Run Sentiment Analysis
```bash
python sentiment_analyzer.py "This software engineering course is thoroughly engaging and rewarding!"
# Output: positive

python sentiment_analyzer.py "I am disappointed with this poor quality experience."
# Output: negative
```

### 3. Verify Error Handling
```bash
# Test missing API key guard:
python sentiment_analyzer.py "Test sentence without key"
# Output to stderr: Authentication Error: TEXT_PROCESSING_API_KEY environment variable is not set.
```

### 4. Code Style Compliance
```bash
python -m pycodestyle sentiment_analyzer.py refactored_sentiment_analyzer.py initial_sentiment_analyzer.py
# 0 errors, 0 warnings (100% PEP 8 compliant)
```
