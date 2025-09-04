#!/usr/bin/env python3
"""Download required NLTK corpora for Naestro orchestrator."""

import nltk


def main() -> None:
    nltk.download("punkt")
    nltk.download("averaged_perceptron_tagger")


if __name__ == "__main__":  # pragma: no cover
    main()
