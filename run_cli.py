# run_cli.py
#export PYTHONPATH=$PYTHONPATH:$(pwd)
import asyncio
import sys
from langchain_core.messages import HumanMessage

from langgraph_app import index_app, qa_app
from src.config.settings import LLM
from state_schema import Agent_State

async def load_repo(repo_url: str) -> Agent_State:

    # Initial state for the graph
    state: Agent_State = {
        "messages": [],
        "url": repo_url,
        "repo_tree": {},
        "global_context": None,
        "selected_files": [],
        "skipped_files": [],
        "parsed_files": [],
        "intent": "",
        "keywords": [],
        "targets": {},
        "summary": [],
        "llm": LLM,
    }

    print(f"\nStarting analysis for repo:\n{repo_url}\n")

    async for step in index_app.astream(state):
        # step is a dict: {"node_name": updated_state}
        # print(step)
        node_name, delta = list(step.items())[0]
        # print(state)
        print(f"Indexing Node executed: {node_name}")
        state.update(delta)

        # Optionally print the node's output
        # updated_state = step[node_name]
        # if "messages" in updated_state:
        #     last_msg = updated_state["messages"][-1]
            # print(f"Message: {last_msg.content if hasattr(last_msg, 'content') else last_msg}")

    print("\nFinished Indexing Repository.\n")
    return state

async def qa(repo_state: Agent_State, question: str) -> Agent_State:
    state: Agent_State = {
        **repo_state,
        "messages": [HumanMessage(content=question)],
        "intent": "",
        "keywords": [],
        "targets": {},
        "selected_files": [],
        "skipped_files": [],
        "summary": "",
    }

    async for step in qa_app.astream(state):
        node_name, delta = list(step.items())[0]
        print(f"QA Node excuted: {node_name}")
        state.update(delta)

    return state

async def qa_loop(repo_state: Agent_State):
    current_state = repo_state

    while True:
        try:
            user_query = input("\nYou(or 'exit' to 'quit): ").strip()
        except(EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not user_query:
            continue
        if user_query.lower() in {"exit", "quit"}:
            print("\nGOODBYE...")
            break
        current_state = await qa(current_state, user_query)
        summary = current_state.get("summary") or "(No answer generated.)"
        print("\nAgent: \n")
        print(summary)

async def main():
    if len(sys.argv)<2:
        print("Usage: python run_cli.py <github_repo_url>")
        raise SystemExit(1)
    repo_url = sys.argv[1]
    repo_state = await load_repo(repo_url)
    print("Repository indexed. You can now ask questions about the codebase.")
    await qa_loop(repo_state)

if __name__ == "__main__":
    asyncio.run(main())



#     if state.get("summary"):
#         print(f"FINAL SUMMARY:\n{state.get('summary')}")
#     else:
#         print("No summary generated.")

# if __name__ == "__main__":
#     # Expect repo URL as CLI argument
#     if len(sys.argv) < 2:
#         print("Usage: python run_cli.py <github_repo_url>")
#         sys.exit(1)

#     repo_url = sys.argv[1]

    # asyncio.run(run(repo_url))
