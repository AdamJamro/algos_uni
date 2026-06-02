def hash_match(stream: str, pattern: str, p=32) -> list[int]:
    """
    iterate match against hash
    """
    if not pattern:
        return []

    idx, current_hash = (0, () % 32)

    hash_value = _hash(pattern)
    pattern_length = len(pattern)
    matches = []

    for i in range(len(stream) - pattern_length + 1):
        if i in cache:
            if cache[i]:
                matches.append(i)
            continue

        if stream[i:i + pattern_length] == pattern:
            matches.append(i)
            cache[i] = True
        else:
            cache[i] = False

    return matches


if __name__ == "__main__":
    stream = "abababac" * 2
    pattern = "abab"
    print(hash_match(stream, pattern))