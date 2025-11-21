# Code-Analyser

**Code-Analyser** is a modular, extensible system designed to analyze GitHub repositories using reasoning capabilities of Gemini-2.5-flash and a LangGraph-based multi-step workflow.

It enables deep code understanding, including directory inspection, function usage tracing, pipeline flow extraction, type inference, dependency mapping, and multi-turn conversational analysis.

This project is under active development.

---

## Overview

Code-Analyser performs a structured series of steps to understand and query any codebase:

- Fetches a full GitHub repository structure  
- Selects relevant files based on user intent  
- Downloads and parses code files  
- Extracts functions, classes, variables, and imports  
- Builds a structured internal representation  
- Applies specialized skills depending on the question  
- Produces an accurate, context-aware answer

The workflow is orchestrated using **LangGraph**, providing controlled, multi-step reasoning.

---

## Features

### Current Capabilities

- GitHub repository metadata extraction  
- File tree construction  
- Raw file content fetching  
- Keyword-based file selection  
- Parsing support for:
  - Python
  - Markdown
  - JSON / YAML
  - Jupyter Notebooks  
- Global repository context generation  
- Multi-turn conversation memory  
- Basic question answering & summarization

---

## Repository Structure

```text
Code-Analyser/
│
├── langgraph_app.py                # LangGraph pipeline definition
├── run_cli.py                      # CLI entrypoint
├── state_schema.py                 # Graph state structure
│
├── src/
│   ├── config/
│   │   └── settings.py             # API keys, constants, settings
│   │
│   ├── github_repo_parser.py       # GitHub metadata + raw file fetcher
│   │
│   ├── nodes/
│   │   ├── fetch_repo_metadata_node.py
│   │   ├── analyze_repo_node.py
│   │   ├── global_context_node.py
│   │   ├── fetch_and_parse_node.py
│   │   └── summarize_repo_node.py
│   │
│   ├── tools/
│   │   ├── parse_python.py
│   │   ├── parse_markdown.py
│   │   ├── parse_json_yaml.py
│   │   ├── parse_notebook.py
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── flatten_tree.py
│       ├── fetch_blob.py
│       └── summarize_state.py
│
├── requirements.txt
└── README.md
