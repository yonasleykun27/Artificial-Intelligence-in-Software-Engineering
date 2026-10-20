#!/usr/bin/env python3
"""
Sentiment Analysis Tool (Hardened & Scaffolding Version)
Analyzes the sentiment of a given sentence using a public API.
Implements secure environment variable authentication and
granular, hierarchical error handling.
"""
import os
import requests
import sys


def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text using the Text Processing API.

    Reads the API key securely from TEXT_PROCESSING_API_KEY environment
    variable and attaches it via HTTP Authorization Bearer token header.
    Implements defensive exception handling for timeouts, network drops,
    HTTP error codes, and payload formatting errors.

    Args:
        text (str): The sentence to analyze.

    Returns:
        str: The sentiment label ('positive', 'negative', or 'neutral'),
             or None if the request failed.
    """
    api_key = os.getenv("TEXT_PROCESSING_API_KEY")
    if not api_key:
        print(
            "Authentication Error: TEXT_PROCESSING_API_KEY environment "
            "variable is not set. Please export your API key before running.",
            file=sys.stderr
        )
        return None

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    url = os.getenv(
        "TEXT_PROCESSING_API_URL",
        "https://text-processing.com/api/sentiment/"
    )
    payload = {"text": text}

    try:
        response = requests.post(
            url,
            data=payload,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        label = data.get('label', 'neutral')

        sentiment_map = {
            'pos': 'positive',
            'neg': 'negative',
            'neutral': 'neutral'
        }
        return sentiment_map.get(label, 'neutral')

    except requests.exceptions.Timeout as e:
        print(
            f"Timeout Error: Request to {url} timed out after 10 seconds: {e}",
            file=sys.stderr
        )
        return None
    except requests.exceptions.ConnectionError as e:
        print(
            f"Connection Error: Network connection to {url} failed: {e}",
            file=sys.stderr
        )
        return None
    except requests.exceptions.HTTPError as e:
        print(
            f"HTTP Error: Remote server returned error status code: {e}",
            file=sys.stderr
        )
        return None
    except requests.exceptions.RequestException as e:
        print(
            f"Request Failed: An unexpected network error occurred: {e}",
            file=sys.stderr
        )
        return None
    except (KeyError, ValueError) as e:
        print(
            f"Invalid Response Format: Unable to parse JSON response: {e}",
            file=sys.stderr
        )
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./sentiment_analyzer.py <sentence>")
        sys.exit(1)
    sentence = " ".join(sys.argv[1:])
    result = analyze_sentiment(sentence)
    if result:
        print(result)
    else:
        sys.exit(1)
