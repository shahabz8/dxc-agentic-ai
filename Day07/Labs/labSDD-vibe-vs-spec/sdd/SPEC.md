# SPEC: AskIT Ticket Triage v1

## Purpose
Classify an IT support ticket into a priority, a queue and an SLA. Pure function, no I/O, no LLM.

## Interface
`triage(ticket: dict) -> dict` in `triage.py`

Input keys: `title` (str, required), `description` (str, optional), `affected_users` (int, optional, default 1), `customer_tier` (str, optional, default "standard"; allowed values: "standard" or "vip")
Output keys: `priority` ("P1".."P4"), `queue` (str), `sla_hours` (int)

## Rules
- R1 Text = title + description, matched case-insensitive, **whole words only** ("download" does not match "down").
- R2 Priority, first match wins:
  P1 if affected_users >= 50 or text has the word `outage` or `down`
  P2 if affected_users >= 10 or text has the word `urgent` or `blocked`
  P3 if affected_users >= 2
  P4 otherwise
- R2b `customer_tier` must be "standard" or "vip"; otherwise raise ValueError. After R2, a VIP ticket's priority is raised one level: P4 to P3, P3 to P2, P2 to P1, and P1 stays P1. SLA follows the final priority.
- R3 Queue, first match wins:
  Security: phishing, breach, malware
  Network: vpn, wifi, network
  Access: password, login, locked
  Hardware: laptop, keyboard, screen
  General: none of the above
- R4 SLA hours: P1 = 2, P2 = 8, P3 = 24, P4 = 72
- R5 Empty, blank or spaces-only title: raise ValueError
- R6 affected_users missing: treat as 1. affected_users < 1 or not an int: raise ValueError
- R7 If `description` is `None`, raise `ValueError` with the message `check your description and run again`.
- R8 Do not log anything, to preserve the pure function's no-I/O requirement.

## Acceptance Criteria
- AC1 60 affected users -> P1, SLA 2
- AC2 "Email outage" -> P1
- AC3 "Slow download speed" -> P4 (whole word rule)
- AC4 12 users -> P2, SLA 8
- AC5 "URGENT: cannot print" -> P2
- AC6 3 users -> P3, SLA 24
- AC7 "Laptop wifi broken" -> queue Network (order matters)
- AC8 "Password reset" -> queue Access
- AC9 empty title -> ValueError; 0 users -> ValueError
- AC10 VIP ticket otherwise classified as P4 -> P3, SLA 24; unsupported `customer_tier` -> ValueError
- AC11 60 affected users -> P1, SLA 2
- AC12 "wifi phishing" -> queue Security

## Out of scope
Persistence, authentication, ML, UI.

## Changelog
- v1 initial
- v2 client change: VIP, Security queue, P1 SLA 2h