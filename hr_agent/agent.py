"""HR Agent: intent routing and conversational interface."""

from __future__ import annotations

import re
from typing import Any

from .tools import (
    check_leave_balance,
    get_employee,
    get_policy,
    list_leave_requests,
    list_policies,
    search_employees,
    search_faqs,
    submit_leave_request,
)

# ---------------------------------------------------------------------------
# Intent patterns
# ---------------------------------------------------------------------------

_INTENT_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "check_leave_balance",
        re.compile(
            r"\b(leave\s*balance|days?\s*(left|remaining)|how\s*many\s*days?)\b",
            re.I,
        ),
    ),
    (
        "submit_leave",
        re.compile(
            r"\b(apply|request|submit|book|take)\b.{0,30}\b(leave|time\s*off|vacation|holiday|sick)\b",
            re.I,
        ),
    ),
    (
        "list_leave_requests",
        re.compile(
            r"\b(my\s*leave\s*requests?|leave\s*history|leave\s*status)\b",
            re.I,
        ),
    ),
    (
        "employee_lookup",
        re.compile(
            r"\b(find|look\s*up|search|who\s*is|employee)\b.{0,40}\b(employee|staff|person|colleague)\b|\bemployee\s+[A-Za-z0-9]+\b",
            re.I,
        ),
    ),
    (
        "list_policies",
        re.compile(
            r"\b(list|show|what)\b.{0,20}\b(policies|policy)\b",
            re.I,
        ),
    ),
    (
        "get_policy",
        re.compile(
            r"\b(policy|policies|rule|guideline)\b",
            re.I,
        ),
    ),
    (
        "faq",
        re.compile(
            r"\b(how|what|when|where|who|why|can\s+i|do\s+i|should\s+i)\b",
            re.I,
        ),
    ),
    (
        "greeting",
        re.compile(r"^\s*(hi|hello|hey|good\s+morning|good\s+afternoon|howdy)\b", re.I),
    ),
    (
        "help",
        re.compile(r"\b(help|what\s+can\s+you\s+do|commands?|options?)\b", re.I),
    ),
]

# ---------------------------------------------------------------------------
# Parameter extraction helpers
# ---------------------------------------------------------------------------

_EMPLOYEE_ID_RE = re.compile(r"\bE\d{3}\b", re.I)
_DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
_LEAVE_TYPE_RE = re.compile(r"\b(annual|sick|personal)\b", re.I)


def _extract_employee_id(text: str) -> str | None:
    m = _EMPLOYEE_ID_RE.search(text)
    return m.group().upper() if m else None


def _extract_dates(text: str) -> list[str]:
    return _DATE_RE.findall(text)


def _extract_leave_type(text: str) -> str | None:
    m = _LEAVE_TYPE_RE.search(text)
    return m.group().lower() if m else None


# ---------------------------------------------------------------------------
# HR Agent
# ---------------------------------------------------------------------------

WELCOME_MESSAGE = (
    "Hello! I'm your HR Agent 🤝\n"
    "I can help you with:\n"
    "  • Checking leave balances (e.g. 'Check leave balance for E001')\n"
    "  • Submitting leave requests (e.g. 'Apply for annual leave from 2026-06-01 to 2026-06-05 for E001')\n"
    "  • Viewing leave history (e.g. 'Show my leave requests for E001')\n"
    "  • Looking up employees (e.g. 'Find employee Alice')\n"
    "  • Fetching HR policies (e.g. 'Tell me the leave policy')\n"
    "  • Answering FAQs (e.g. 'How do I apply for expenses?')\n"
    "\nType 'help' at any time to see this menu again, or 'quit' to exit."
)


class HRAgent:
    """A conversational HR Agent that routes user queries to HR tools."""

    def __init__(self) -> None:
        self._context: dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def welcome(self) -> str:
        """Return the welcome / help message."""
        return WELCOME_MESSAGE

    def respond(self, user_input: str) -> str:
        """Process *user_input* and return a formatted response string."""
        text = user_input.strip()
        if not text:
            return "Please enter a message. Type 'help' to see available options."

        intent = self._classify_intent(text)
        return self._dispatch(intent, text)

    # ------------------------------------------------------------------
    # Intent classification
    # ------------------------------------------------------------------

    def _classify_intent(self, text: str) -> str:
        for intent, pattern in _INTENT_PATTERNS:
            if pattern.search(text):
                # Prefer more specific intents over generic 'faq'
                return intent
        return "unknown"

    # ------------------------------------------------------------------
    # Dispatcher
    # ------------------------------------------------------------------

    def _dispatch(self, intent: str, text: str) -> str:
        handlers = {
            "greeting": self._handle_greeting,
            "help": self._handle_help,
            "check_leave_balance": self._handle_check_leave_balance,
            "submit_leave": self._handle_submit_leave,
            "list_leave_requests": self._handle_list_leave_requests,
            "employee_lookup": self._handle_employee_lookup,
            "get_policy": self._handle_get_policy,
            "list_policies": self._handle_list_policies,
            "faq": self._handle_faq,
            "unknown": self._handle_unknown,
        }
        handler = handlers.get(intent, self._handle_unknown)
        return handler(text)

    # ------------------------------------------------------------------
    # Intent handlers
    # ------------------------------------------------------------------

    def _handle_greeting(self, _text: str) -> str:
        return "Hello! How can I assist you today? Type 'help' to see what I can do."

    def _handle_help(self, _text: str) -> str:
        return WELCOME_MESSAGE

    def _handle_check_leave_balance(self, text: str) -> str:
        employee_id = _extract_employee_id(text)
        if not employee_id:
            return (
                "Please provide your employee ID to check your leave balance.\n"
                "Example: 'Check leave balance for E001'"
            )
        result = check_leave_balance(employee_id)
        if "error" in result:
            return f"❌ {result['error']}"
        balance = result["leave_balance"]
        return (
            f"📋 Leave Balance for {result['name']} ({result['employee_id']}):\n"
            f"  • Annual  : {balance['annual']} day(s)\n"
            f"  • Sick    : {balance['sick']} day(s)\n"
            f"  • Personal: {balance['personal']} day(s)"
        )

    def _handle_submit_leave(self, text: str) -> str:
        employee_id = _extract_employee_id(text)
        leave_type = _extract_leave_type(text)
        dates = _extract_dates(text)

        missing: list[str] = []
        if not employee_id:
            missing.append("employee ID (e.g. E001)")
        if not leave_type:
            missing.append("leave type (annual / sick / personal)")
        if len(dates) < 2:
            missing.append("start and end dates (YYYY-MM-DD format)")

        if missing:
            return (
                "To submit a leave request, I need the following information:\n"
                + "\n".join(f"  • {m}" for m in missing)
                + "\n\nExample: 'Apply for annual leave from 2026-06-01 to 2026-06-05 for E001'"
            )

        result = submit_leave_request(
            employee_id=employee_id,
            leave_type=leave_type,
            start_date=dates[0],
            end_date=dates[1],
        )
        if "error" in result:
            return f"❌ {result['error']}"
        req = result["request"]
        return (
            f"✅ {result['message']}\n"
            f"  Employee : {req['employee_name']} ({req['employee_id']})\n"
            f"  Type     : {req['leave_type'].capitalize()}\n"
            f"  Dates    : {req['start_date']} → {req['end_date']}\n"
            f"  Days     : {req['days_requested']}\n"
            f"  Ref      : {req['request_id']}"
        )

    def _handle_list_leave_requests(self, text: str) -> str:
        employee_id = _extract_employee_id(text)
        if not employee_id:
            return (
                "Please provide your employee ID.\n"
                "Example: 'Show my leave requests for E001'"
            )
        result = list_leave_requests(employee_id)
        if "error" in result:
            return f"❌ {result['error']}"
        if not result["requests"]:
            return f"No leave requests found for {result['name']} ({result['employee_id']})."
        lines = [f"📅 Leave Requests for {result['name']} ({result['employee_id']}):"]
        for req in result["requests"]:
            lines.append(
                f"  [{req['request_id']}] {req['leave_type'].capitalize()} | "
                f"{req['start_date']} → {req['end_date']} | "
                f"{req['days_requested']} day(s) | Status: {req['status'].capitalize()}"
            )
        return "\n".join(lines)

    def _handle_employee_lookup(self, text: str) -> str:
        # Try direct ID lookup first
        employee_id = _extract_employee_id(text)
        if employee_id:
            emp = get_employee(employee_id)
            if emp:
                return self._format_employee(emp)
            return f"❌ No employee found with ID '{employee_id}'."

        # Fall back to name search
        name_match = re.search(
            r"(?:find|look\s*up|search|who\s*is)\s+(?:employee\s+)?([A-Za-z\s]+?)(?:\s*$|\?)",
            text,
            re.I,
        )
        if name_match:
            name_query = name_match.group(1).strip()
            employees = search_employees(name_query)
            if not employees:
                return f"❌ No employees found matching '{name_query}'."
            if len(employees) == 1:
                return self._format_employee(employees[0])
            lines = [f"Found {len(employees)} employees matching '{name_query}':"]
            for emp in employees:
                lines.append(
                    f"  • {emp['id']}: {emp['name']} — {emp['position']}, {emp['department']}"
                )
            return "\n".join(lines)

        return (
            "Please provide an employee ID or name.\n"
            "Example: 'Find employee Alice' or 'Look up E001'"
        )

    def _handle_get_policy(self, text: str) -> str:
        # Try to extract a policy topic from the input
        topic_match = re.search(
            r"\b(?:policy|policies|rule|guideline)\b\s*(?:on|for|about|regarding)?\s*([A-Za-z_\s]+?)(?:\s*$|\?)",
            text,
            re.I,
        )
        topic = topic_match.group(1).strip() if topic_match else text

        result = get_policy(topic)
        if not result["found"]:
            return f"ℹ️ {result['message']}"
        policy = result["policy"]
        return f"📖 {policy['title']}\n\n{policy['content']}"

    def _handle_list_policies(self, _text: str) -> str:
        titles = list_policies()
        lines = ["📚 Available HR Policies:"]
        for title in titles:
            lines.append(f"  • {title}")
        lines.append("\nAsk me about any policy, e.g. 'What is the remote work policy?'")
        return "\n".join(lines)

    def _handle_faq(self, text: str) -> str:
        faqs = search_faqs(text)
        if not faqs:
            return (
                "I couldn't find an answer to that question. "
                "Please contact HR at hr@company.com for further assistance."
            )
        lines: list[str] = []
        for faq in faqs[:3]:  # Limit to top 3 matches
            lines.append(f"❓ {faq['question']}\n   {faq['answer']}")
        return "\n\n".join(lines)

    def _handle_unknown(self, _text: str) -> str:
        return (
            "I'm not sure how to help with that. "
            "Type 'help' to see what I can do, or contact HR at hr@company.com."
        )

    # ------------------------------------------------------------------
    # Formatting helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _format_employee(emp: dict[str, Any]) -> str:
        manager = emp.get("manager")
        manager_info = ""
        if manager:
            from .data import EMPLOYEES  # avoid circular import
            mgr = EMPLOYEES.get(manager)
            manager_info = f"\n  Manager    : {mgr['name']} ({manager})" if mgr else f"\n  Manager ID : {manager}"
        return (
            f"👤 Employee Details:\n"
            f"  ID         : {emp['id']}\n"
            f"  Name       : {emp['name']}\n"
            f"  Department : {emp['department']}\n"
            f"  Position   : {emp['position']}\n"
            f"  Email      : {emp['email']}\n"
            f"  Phone      : {emp['phone']}\n"
            f"  Start Date : {emp['start_date']}"
            f"{manager_info}"
        )
