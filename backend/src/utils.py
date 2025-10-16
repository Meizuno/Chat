def to_camel(string: str) -> str:
    """Convert snake_case to camelCase"""

    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])
