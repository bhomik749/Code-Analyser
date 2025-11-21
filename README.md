## Code-Analyser

**Code-Analyser** is a modular, extensible system designed to analyze GitHub repositories using reasoning capabilities of Gemini-2.5-flash and a LangGraph-based multi-step workflow.

It enables deep code understanding, including directory inspection, function usage tracing, pipeline flow extraction, type inference, dependency mapping, and multi-turn conversational analysis.

This project is under active development.

---

### Overview

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

### Features

#### Current Capabilities

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

### Repository Structure

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
```
### Workflow

The agent executes a multi-step LangGraph pipeline:

#### 1. `fetch_repo_metadata_node`
Fetches the GitHub repository tree and builds structured metadata.

#### 2. `analyze_repo_node`
Selects relevant files based on keywords extracted from the user's question.

#### 3. `fetch_and_parse_node`
Downloads raw file contents and parses them into structured representations.

#### 4. `global_context_node`
Produces a high-level summary of the repository.

#### 5. `summarize_repo_node`
Generates a final answer using:
- selected files  
- parsed content  
- global context  
- current user query  
- conversation history  

This node will later be replaced by a more advanced final-answer builder.

---

### CLI Usage

Run analysis from the command line:

```bash
python run_cli.py <repo_url>
```
### Future Additions

Code-Analyser will evolve into a complete, multi-skill code analysis agent.  
The following components are planned for upcoming releases.

#### Query Understanding
- Intent classification (function usage, type lookup, pipeline flow, directory analysis)
- Keyword extraction
- Query decomposition

#### Deep Code Analysis
- Symbol extraction (functions, classes, variables, imports)
- Function usage tracing
- Type inference for variables
- Pipeline flow reconstruction
- Directory-level purpose identification
- Import dependency graph extraction

#### Specialized Skill Nodes

Planned nodes include:
- `query_analyzer_node`
- `symbol_extractor_node`
- `function_usage_node`
- `type_lookup_node`
- `pipeline_flow_node`
- `directory_inspector_node`
- `final_answer_builder_node`
- Optional: `dependency_graph_node`

#### API and UI Layer
- FastAPI backend for streaming responses
- Web-based multi-turn chat interface

---

### Installation

```bash
git clone https://github.com/<your-username>/Code-Analyser
cd Code-Analyser
pip install -r requirements.txt
```
Set environment variables (GitHub token, LLM keys) in a `.env` file.

### Contributing

Contributions are welcome.
New analysis nodes, tools, and improvements are encouraged.
