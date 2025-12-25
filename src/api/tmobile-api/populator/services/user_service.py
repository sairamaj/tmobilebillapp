def get_user_data(path: str = "users.json") -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()