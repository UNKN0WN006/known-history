def score_content(text: str) -> dict:
    """
    Mock credibility scorer using simple heuristics.
    Replace with HF/DO Gradient API when available.
    """
    length = min(len(text), 1000)
    # Heuristic: longer, more detailed content tends to be more credible
    score = round(0.3 + 0.6 * (length / 1000.0), 3)
    
    if score > 0.65:
        label = "credible"
    elif score > 0.4:
        label = "neutral"
    else:
        label = "questionable"
    
    return {"label": label, "score": score}