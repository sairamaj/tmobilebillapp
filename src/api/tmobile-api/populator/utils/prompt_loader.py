def load_prompt(path: str = "prompt.txt") -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()