## Code-Analyser

Code-Analyser is a multi-phase code understanding engine designed to analyze GitHub repositories and answer user questions interactively with the backend of Langgraph.

Currently, the system is capable of performing following tasks:

- Repository Indexing
- Incremental Code Parsing
- Query-Aware file selection
- Multi-turn Q&A

The project is optimized for long-term exploration of large repositories. The more you chat, the more code gets parsed, making future answers faster and richer.

This project is under active development.

---

### Overview

**Core Functionality**

- Fetch the complete GitHub repository structure
- Generate a high-level global context for the repo
- Extract and parse file contents incrementally
- Support arbitrary user questions
- Use intents, keywords, and targets through the provided user prompt, to select the relevant files.
- Multi-turn conversational question answering

**Architecture Highlights**

- Two-phase Langgraph workflow:
  - Indexing Phase
  - QA Phase
- Incremental Parsing to avoid repeated processing
---

### How it works

The system is split into two workflows:

1. Indexing workflow

Runs ONCE per repository when the user loads a new repo.

<img width="256" height="1024" alt="indexing_pipeline_flowchart" src="https://github.com/user-attachments/assets/f5a0d609-2e1e-42d1-9739-b7df265e1d41" />

**Purpose**

- Crawl the Repository
- Build `repo_tree`
- Create Global Context for the whole repository
- Select initial important files
- Parse them
- Store everything in `repo_state` state variable
- Reuse this for all future questions

2. QA Workflow
  
Runs for EVERY question the user asks

<img width="256" height="1024" alt="QA_pipeline_flowchart" src="https://github.com/user-attachments/assets/f6c327c7-2a4a-412e-9dbe-bf1bf2d9f27d" />


**Purpose**

- Interpret the user's question
- Select relevant files, based on user's query using `keywords`, `intent` and `target` variables
- Parse only new files
- Produce final answer using:
  - parsed code
  - global context
  - conversation history
---

### Repository Structure

```text
Code-Analyser/
│
├── run_cli.py                    
├── langgraph_app.py              
├── state_schema.py                
│
├── src/
│   ├── config/
│   │   └── settings.py            
│   │
│   ├── github_repo_parser.py      
│   │
│   ├── nodes/
│   │   ├── fetch_repo_metadata_node.py
│   │   ├── global_context_node.py
│   │   ├── query_analyzer_node.py
│   │   ├── analyze_repo_node.py
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
---
### Usage

1. Index the repository

```bash
python run_cli.py https://github.com/<owner>/<repo>
```

The system will crawl the repo, parse initial files, and store everything in memory.

2. Multi-Chat Functionality
After Indexing is done:

```bash
You: Where is the pipeline implemented?
Agent: ...
You: Explain preprocess.py
Agent: ...
You: Which function loads the model?
Agent: ...
```
Each question uses:
- cached parsed files
- incremental parsing
- multi-chat contenxt
---

### Future Additions

1. In-depth code analysis
   - Symbol extraction(classes, functions, globals)
   - Function usage tracing
   - Type inference
   - Module-level dependency graphs
2. Query Understanding
4. Persistant Layer
   - Store indexed repos in local DB
   - Avoid repeating indexing on restart
6. Backend and UI
   - FastAPI server
   - Chat-based frontend
---

### Installation

```bash
git clone https://github.com/bhomik749/Code-Analyser
cd Code-Analyser
pip install -r requirements.txt
```
Set environment variables in a `.env` file. 
- GitHub token
- LLM keys 

### Contributing

Contributions are welcome.

Feel free to open issues or PRs for:

- New analysis nodes
- Better parsing logic
- UI components
- Documentation improvements
