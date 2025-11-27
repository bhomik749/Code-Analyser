# state_schema.py

from typing import Annotated, Sequence, TypedDict, Union, Dict, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from src.config.settings import LLM


class Agent_State(TypedDict):
    """
    LangGraph state structure for the Repo Analyzer + Summarizer Agent.
    
    This is the central shared memory between all nodes.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    url: Union[str, None]
    repo_tree: Dict[str, any]
    global_context: Union[str, None]
    selected_files: List[Dict[str, any]]
    skipped_files: List[str]
    parsed_files: List[Dict[str, str]]
    intent: str
    keywords: List[str]
    targets: Dict[str, any]
    summary: str #Annotated[Sequence[BaseMessage], add_messages]
    llm: LLM
