def compute_ciddp_score(evaluation: dict) -> float:
    if not evaluation:
        return 0.0
    # Expecting exactly 5 keys: Clarity, Integrity, Depth, Practicality, Pertinence
    total = sum(evaluation.values())
    count = len(evaluation)
    print(evaluation.values())
    print(total/count)
    return total / count  # This will be /5 if all 5 are present