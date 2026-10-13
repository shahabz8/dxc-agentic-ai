import pytest

from sdd.triage import triage


def test_ac1_60_affected_users_is_p1_with_two_hour_sla():
    result = triage({"title": "Printer issue", "affected_users": 60})
    assert result["priority"] == "P1"
    assert result["sla_hours"] == 2


def test_ac2_outage_is_p1():
    assert triage({"title": "Email outage"})["priority"] == "P1"


def test_ac3_download_does_not_match_down():
    assert triage({"title": "Slow download speed"})["priority"] == "P4"


def test_ac4_12_users_is_p2_with_eight_hour_sla():
    result = triage({"title": "Printer issue", "affected_users": 12})
    assert result["priority"] == "P2"
    assert result["sla_hours"] == 8


def test_ac5_urgent_is_case_insensitive():
    assert triage({"title": "URGENT: cannot print"})["priority"] == "P2"


def test_ac6_3_users_is_p3_with_24_hour_sla():
    result = triage({"title": "Printer issue", "affected_users": 3})
    assert result["priority"] == "P3"
    assert result["sla_hours"] == 24


def test_ac7_network_queue_precedes_hardware():
    assert triage({"title": "Laptop wifi broken"})["queue"] == "Network"


def test_ac8_password_uses_access_queue():
    assert triage({"title": "Password reset"})["queue"] == "Access"


def test_ac9_empty_title_and_zero_users_raise_value_error():
    with pytest.raises(ValueError):
        triage({"title": ""})
    with pytest.raises(ValueError):
        triage({"title": "Printer issue", "affected_users": 0})


def test_none_description_raises_value_error():
    with pytest.raises(ValueError, match="check your description and run again"):
        triage({"title": "Email outage", "description": None})


def test_ac10_vip_raises_priority_and_invalid_tier_is_rejected():
    result = triage({"title": "Routine request", "customer_tier": "vip"})
    assert result["priority"] == "P3"
    assert result["sla_hours"] == 24
    with pytest.raises(ValueError):
        triage({"title": "Routine request", "customer_tier": "gold"})


def test_ac11_p1_has_two_hour_sla():
    result = triage({"title": "Printer issue", "affected_users": 60})
    assert result["priority"] == "P1"
    assert result["sla_hours"] == 2


def test_ac12_security_queue_precedes_network():
    assert triage({"title": "wifi phishing"})["queue"] == "Security"