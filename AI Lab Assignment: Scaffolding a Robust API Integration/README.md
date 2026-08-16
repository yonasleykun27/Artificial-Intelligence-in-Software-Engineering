# AI Lab Assignment: Scaffolding a Robust API Integration

## Overview
This task demonstrates how to integrate AI into a software development workflow using Contextual Prompting. The sentiment analysis script was refactored to securely read an API key from an environment variable and handle specific network exceptions.

## AI Tool Used
- **Tool:** ChatGPT / Claude (Specify whichever AI tool you used)
- **Technique:** Contextual Prompting

## Files
- `sentiment_analyzer.py`: Python script for sentiment analysis featuring secure environment variable handling and robust exception catching (`Timeout`, `ConnectionError`, `HTTPError`).

## Requirements & Execution
1. Set the environment variable:
   ```bash
   export TEXT_PROCESSING_API_KEY="your_api_key_here"
