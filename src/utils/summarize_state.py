def summarize_state(state):
    out = {}
    for k, v in state.items():
        if isinstance(v, (list, tuple, set)):
            out[k] = f"<{type(v).__name__}> len={len(v)}"
        elif isinstance(v, dict):
            out[k] = f"<dict> keys={list(v.keys())[:5]} (total={len(v)})"
        else:
            out[k] = f"{type(v).__name__}: {str(v)[:80]}..."
    return out
