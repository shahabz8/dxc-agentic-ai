def triage(ticket):
    """Prioritize an IT support ticket into priority, queue, and SLA hours.

    ticket: dict with keys title, description, affected_users, customer_tier
    returns: dict with keys priority, queue, sla_hours
    """
    if not isinstance(ticket, dict):
        raise TypeError("ticket must be a dict")

    title = ticket.get("title", "")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title must be a non-empty string")

    description = ticket.get("description", "")
    if description is None:
        description = ""
    description = str(description)

    affected_users = ticket.get("affected_users", 1)
    if not isinstance(affected_users, int) or affected_users <= 0:
        raise ValueError("affected_users must be a positive integer")

    customer_tier = ticket.get("customer_tier", "standard")
    if customer_tier not in ("standard", "vip"):
        raise ValueError("customer_tier must be 'standard' or 'vip'")

    text = f"{title} {description}".lower()
    words = set(text.replace(":", " ").replace("-", " ").split())

    if "outage" in text or "down" in words or affected_users >= 50:
        priority = "P1"
    elif "urgent" in text or affected_users >= 10:
        priority = "P2"
    elif affected_users >= 2:
        priority = "P3"
    else:
        priority = "P4"

    if customer_tier == "vip":
        priority = {"P1": "P1", "P2": "P1", "P3": "P2", "P4": "P3"}[priority]

    if "phishing" in text or "breach" in text or "malware" in text:
        queue = "Security"
    elif "vpn" in text or "wifi" in text or "network" in text:
        queue = "Network"
    elif "password" in text or "login" in text or "account locked" in text:
        queue = "Access"
    elif "keyboard" in text:
        queue = "Hardware"
    else:
        queue = "General"

    sla_by_priority = {
        "P1": 2,
        "P2": 8,
        "P3": 24,
        "P4": 72,
    }

    return {
        "priority": priority,
        "queue": queue,
        "sla_hours": sla_by_priority[priority],
    }