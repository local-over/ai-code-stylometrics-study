---

## 1. Introduction

Generative AI models for code synthesis are now deployed across commercial software development environments. However, evaluation benchmarks primarily measure functional correctness (such as unit test pass rates on HumanEval or MBPP) rather than long-term maintainability, security, or structural readability.

Standard linters score code formatting against rigid syntax rules, but they fail to capture structural shifts in how logic is organized. A program can pass every linter check while introducing structural bloat, excessive vertical whitespace, or security vulnerabilities.

To measure these structural differences, we constructed a 6-Layer Architecture Pipeline combining deterministic static analysis tools (Tree-sitter, Semgrep, Lizard) with LLM subagents. We evaluated **2,028,180 code snippets** across **507,045 parallel task quadruplets** where human solutions and three AI model outputs solve identical algorithmic requirements in Python and Java.
