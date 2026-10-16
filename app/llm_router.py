"""Routes prompts across hosted foundation models and open-weight models.

Gives the AI-BOM a mix of providers: OpenAI, Anthropic, and Hugging Face models.
"""
import os

import anthropic
from openai import OpenAI
from transformers import pipeline

OPENAI_CHAT_MODEL = "gpt-4o"
OPENAI_CHEAP_MODEL = "gpt-4o-mini"
ANTHROPIC_MODEL = "claude-sonnet-4-5"
LOCAL_MODEL = "meta-llama/Llama-3.1-8B-Instruct"
LOCAL_SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"


def ask_openai(prompt: str) -> str:
    client = OpenAI()
    resp = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content


def ask_anthropic(prompt: str) -> str:
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def classify_locally(text: str) -> str:
    clf = pipeline("sentiment-analysis", model=LOCAL_SENTIMENT_MODEL)
    return clf(text)[0]["label"]


def route(prompt: str) -> str:
    """Pick a provider based on which credentials are present."""
    if os.getenv("OPENAI_API_KEY"):
        return ask_openai(prompt)
    if os.getenv("ANTHROPIC_API_KEY"):
        return ask_anthropic(prompt)
    return f"(local) sentiment={classify_locally(prompt)}"


if __name__ == "__main__":
    print(route("Snyk AI-BOM makes this supply chain visible."))
