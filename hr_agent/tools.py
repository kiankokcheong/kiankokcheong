"""HR tools: individual capabilities used by the HR Agent."""

from __future__ import annotations

import re
import uuid
from datetime import date, datetime, timedelta, timezone
from typing import Any

from .data import EMPLOYEES, FAQS, LEAVE_REQUESTS, POLICIES


# ---------------------------------------------------------------------------
# Employee lookup
# ---------------------------------------------------------------------------

def get_employee(employee_id: str) -> dict[str, Any] | None:
    """Return employee record by ID (case-insensitive), or None if not found."""
    return EMPLOYEES.get(employee_id.upper())


def search_employees(name: str) -> list[dict[str, Any]]:
    """Return all employees whose names contain *name* (case-insensitive)."""
    query = name.lower()
    return [emp for emp in EMPLOYEES.values() if query in emp["name"].lower()]


# ---------------------------------------------------------------------------
# Leave management
# ---------------------------------------------------------------------------

def check_leave_balance(employee_id: str) -> dict[str, Any]:
    """Return the leave balance for an employee."""
    employee = get_employee(employee_id)
    if not employee:
        return {"error": f"Employee '{employee_id}' not found."}
    return {
        "employee_id": employee["id"],
        "name": employee["name"],
        "leave_balance": employee["leave_balance"],
    }


def submit_leave_request(
    employee_id: str,
    leave_type: str,
    start_date: str,
    end_date: str,
    reason: str = "",
) -> dict[str, Any]:
    """Submit a leave request for an employee.

    Parameters
    ----------
    employee_id:
        The employee's ID.
    leave_type:
        One of ``"annual"``, ``"sick"``, or ``"personal"``.
    start_date:
        Start date in ``YYYY-MM-DD`` format.
    end_date:
        End date in ``YYYY-MM-DD`` format.
    reason:
        Optional reason for the leave.

    Returns
    -------
    dict
        A confirmation record or an error dict.
    """
    employee = get_employee(employee_id)
    if not employee:
        return {"error": f"Employee '{employee_id}' not found."}

    leave_type = leave_type.lower()
    if leave_type not in ("annual", "sick", "personal"):
        return {
            "error": (
                f"Invalid leave type '{leave_type}'. "
                "Choose from: annual, sick, personal."
            )
        }

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}

    if end < start:
        return {"error": "End date cannot be before start date."}

    # Business days count (Mon–Fri)
    days_requested = sum(
        1
        for n in range((end - start).days + 1)
        if (start + timedelta(days=n)).weekday() < 5
    )

    balance = employee["leave_balance"][leave_type]
    if days_requested > balance:
        return {
            "error": (
                f"Insufficient {leave_type} leave balance. "
                f"Requested: {days_requested} day(s), Available: {balance} day(s)."
            )
        }

    request_id = f"LR-{uuid.uuid4().hex[:8].upper()}"
    record = {
        "request_id": request_id,
        "employee_id": employee["id"],
        "employee_name": employee["name"],
        "leave_type": leave_type,
        "start_date": start_date,
        "end_date": end_date,
        "days_requested": days_requested,
        "reason": reason,
        "status": "pending",
        "submitted_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    LEAVE_REQUESTS.append(record)

    # Deduct from balance (optimistic update; reverted if rejected by manager)
    EMPLOYEES[employee["id"]]["leave_balance"][leave_type] -= days_requested

    return {
        "success": True,
        "message": (
            f"Leave request submitted successfully. "
            f"Reference: {request_id}. "
            f"Status: Pending manager approval."
        ),
        "request": record,
    }


def list_leave_requests(employee_id: str) -> dict[str, Any]:
    """Return all leave requests for an employee."""
    employee = get_employee(employee_id)
    if not employee:
        return {"error": f"Employee '{employee_id}' not found."}

    requests = [r for r in LEAVE_REQUESTS if r["employee_id"] == employee["id"]]
    return {
        "employee_id": employee["id"],
        "name": employee["name"],
        "requests": requests,
        "total": len(requests),
    }


# ---------------------------------------------------------------------------
# Policy lookup
# ---------------------------------------------------------------------------

def get_policy(topic: str) -> dict[str, Any]:
    """Return the policy document closest to *topic*."""
    topic_lower = topic.lower()
    # Exact or partial key match
    for key, policy in POLICIES.items():
        if key in topic_lower or topic_lower in key:
            return {"found": True, "policy": policy}
    # Title match
    for policy in POLICIES.values():
        if topic_lower in policy["title"].lower():
            return {"found": True, "policy": policy}
    # Keyword scan inside content
    for policy in POLICIES.values():
        if topic_lower in policy["content"].lower():
            return {"found": True, "policy": policy}
    return {
        "found": False,
        "message": (
            f"No policy found for '{topic}'. "
            f"Available topics: {', '.join(POLICIES.keys())}."
        ),
    }


def list_policies() -> list[str]:
    """Return the titles of all available policies."""
    return [p["title"] for p in POLICIES.values()]


# ---------------------------------------------------------------------------
# FAQ search
# ---------------------------------------------------------------------------

def search_faqs(query: str) -> list[dict[str, str]]:
    """Return FAQs that match *query* by keyword or substring."""
    query_lower = query.lower()
    tokens = set(re.findall(r"\w+", query_lower))
    results = []
    for faq in FAQS:
        keyword_hit = any(kw.lower() in query_lower for kw in faq["keywords"])
        token_hit = bool(tokens & set(re.findall(r"\w+", faq["question"].lower())))
        if keyword_hit or token_hit:
            results.append({"question": faq["question"], "answer": faq["answer"]})
    return results
