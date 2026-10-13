import re


def triage(ticket: dict) -> dict:
    title = ticket.get("title", "")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title must be a non-empty string")

    affected_users = ticket.get("affected_users", 1)
    if type(affected_users) is not int or affected_users < 1:
        raise ValueError("affected_users must be a positive integer")

    customer_tier = ticket.get("customer_tier", "standard")
    if customer_tier not in ("standard", "vip"):
        raise ValueError("customer_tier must be 'standard' or 'vip'")

    description = ticket.get("description", "")
    if description is None:
        raise ValueError("check your description and run again")

    text = f"{title} {description}"

    def has_word(*words: str) -> bool:
        pattern = r"\b(?:" + "|".join(re.escape(word) for word in words) + r")\b"
        return re.search(pattern, text, re.IGNORECASE) is not None

    if affected_users >= 50 or has_word("outage", "down"):
        priority = "P1"
    elif affected_users >= 10 or has_word("urgent", "blocked"):
        priority = "P2"
    elif affected_users >= 2:
        priority = "P3"
    else:
        priority = "P4"

    if customer_tier == "vip":
        priority = {"P1": "P1", "P2": "P1", "P3": "P2", "P4": "P3"}[priority]

    if has_word("phishing", "breach", "malware"):
        queue = "Security"
    elif has_word("vpn", "wifi", "network"):
        queue = "Network"
    elif has_word("password", "login", "locked"):
        queue = "Access"
    elif has_word("laptop", "keyboard", "screen"):
        queue = "Hardware"
    else:
        queue = "General"

    sla_hours = {"P1": 2, "P2": 8, "P3": 24, "P4": 72}[priority]
    return {"priority": priority, "queue": queue, "sla_hours": sla_hours}