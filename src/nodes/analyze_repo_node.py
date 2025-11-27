import re
from langchain_core.messages import SystemMessage, HumanMessage

from src.utils.flatten_tree import flatten_tree
from src.config.settings import MAX_SIZE_KB, IMPORTANT_EXT, IMPORTANT_NAMES

def matches_keywords(path, keywords):
        path_lower = path.lower()
        return any(kw.lower() in path_lower for kw in keywords)

async def analyze_tree_node(state: dict) -> dict:
    """
    Query-aware Analyze Node.
    Decides which files to parse deeply based on:
      - repo metadata
      - user query (latest HumanMessage)
      - file importance (README, setup, main, config, etc.)
      - file sizes and extensions
    """

    print("Initializing Analyze Tree Node...")

    repo_tree = state.get("repo_tree", None)
    intent = state.get("intent")
    keywords = state.get("keywords", [])
    targets = state.get("targets", {})
    
    if not repo_tree:
        return {
                "selected": [],
                "messages": state.get("messages", []) + [
                    SystemMessage(content="No repository tree available.")
                ]}

    flattened = flatten_tree(repo_tree)

    user_query = ""
    for msg in reversed(state.get("messages", [])):
        if isinstance(msg, HumanMessage):
            user_query = msg.content.lower()
            break

    print(f"Latest user query: {user_query}")

    # Get words like ["train", "metrics", "dataset", "model"]
    query_keywords = re.findall(r"[a-zA-Z_]+", user_query)
    # print(f"Extracted query keywords: {query_keywords}")

    selected, skipped = [], []

    for meta in flattened:
        path = meta["path"].lower()
        size = meta["size_kb"]
        ext  = meta["ext"].lower()

        # Skip too-large files
        if size > MAX_SIZE_KB:
            skipped.append(path)
            continue

        # Always include important names
        if any(key in path for key in IMPORTANT_NAMES):
            selected.append(meta)
            continue

        # Include files matching keywords in user query
        if any(key in path for key in query_keywords):
            selected.append(meta)
            continue

        # Keep primary code/documentation files
        if ext in IMPORTANT_EXT:
            selected.append(meta)
        else:
            skipped.append(path)

        if intent == "function_usage":
            fn = targets.get("function")
            if fn:
                if fn.lower() in path.lower():
                    selected.append(meta)
                    continue
            # fallback to keyword match
            if matches_keywords(path, keywords):
                selected.append(meta)
                continue

        # 2. TYPE LOOKUP
        elif intent == "type_lookup":
            var = targets.get("variable")
            if var:
                if var.lower() in path.lower():
                    selected.append(meta)
                    continue
            if matches_keywords(path, keywords):
                selected.append(meta)
                continue

        # 3. DIRECTORY QUESTION
        elif intent == "directory_question":
            directory = targets.get("directory")
            if directory and path.startswith(directory):
                selected.append(meta)
                continue

        # 4. PIPELINE FLOW
        elif intent == "pipeline_flow":
            # prioritize orchestrator-style files
            pipeline_markers = ["train", "main", "pipeline", "runner", "engine"]
            if any(m in path.lower() for m in pipeline_markers):
                selected.append(meta)
                continue

        # 5. ARCHITECTURE SUMMARY
        elif intent == "architecture_summary":
            # prioritize high-level Python files
            if path.count("/") <= 1 and path.endswith(".py"):
                selected.append(meta)
                continue

        # 6. FALLBACK: KEYWORD SEARCH
        elif intent == "high_level_summary":
            if matches_keywords(path, keywords):
                selected.append(meta)
                continue

    print(f"Selected {len(selected)} files, skipped {len(skipped)}.")

    return {
        "selected": selected,
        "skipped_files": skipped,
        "messages": state.get("messages", []) + [
            SystemMessage(content=f"Selected {len(selected)} files based on query: '{user_query}'.")
        ]
    }
