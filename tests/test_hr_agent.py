"""Unit tests for the HR Agent."""

from __future__ import annotations

import pytest

from hr_agent import HRAgent
from hr_agent.tools import (
    check_leave_balance,
    get_employee,
    get_policy,
    list_policies,
    search_employees,
    search_faqs,
    submit_leave_request,
    list_leave_requests,
)
from hr_agent.data.employees import EMPLOYEES


# ---------------------------------------------------------------------------
# Tool tests
# ---------------------------------------------------------------------------

class TestGetEmployee:
    def test_existing_employee(self):
        emp = get_employee("E001")
        assert emp is not None
        assert emp["name"] == "Alice Johnson"

    def test_case_insensitive(self):
        emp = get_employee("e001")
        assert emp is not None
        assert emp["id"] == "E001"

    def test_nonexistent_employee(self):
        assert get_employee("E999") is None


class TestSearchEmployees:
    def test_search_by_first_name(self):
        results = search_employees("Alice")
        assert len(results) == 1
        assert results[0]["id"] == "E001"

    def test_search_case_insensitive(self):
        results = search_employees("alice")
        assert len(results) == 1

    def test_search_no_results(self):
        results = search_employees("Zephyr")
        assert results == []

    def test_search_partial_name(self):
        results = search_employees("son")
        assert any(e["id"] == "E001" for e in results)


class TestCheckLeaveBalance:
    def test_valid_employee(self):
        result = check_leave_balance("E001")
        assert "error" not in result
        assert "leave_balance" in result
        assert result["employee_id"] == "E001"

    def test_invalid_employee(self):
        result = check_leave_balance("E999")
        assert "error" in result


class TestSubmitLeaveRequest:
    def test_valid_request(self):
        # Use E002 so we don't affect E001 used by balance tests
        result = submit_leave_request(
            employee_id="E002",
            leave_type="annual",
            start_date="2026-07-01",
            end_date="2026-07-03",
        )
        assert result.get("success") is True
        assert "request_id" in result["request"]

    def test_invalid_employee(self):
        result = submit_leave_request(
            employee_id="E999",
            leave_type="annual",
            start_date="2026-07-01",
            end_date="2026-07-03",
        )
        assert "error" in result

    def test_invalid_leave_type(self):
        result = submit_leave_request(
            employee_id="E003",
            leave_type="vacation",
            start_date="2026-07-01",
            end_date="2026-07-01",
        )
        assert "error" in result

    def test_invalid_date_format(self):
        result = submit_leave_request(
            employee_id="E003",
            leave_type="sick",
            start_date="01-07-2026",
            end_date="01-07-2026",
        )
        assert "error" in result

    def test_end_before_start(self):
        result = submit_leave_request(
            employee_id="E003",
            leave_type="sick",
            start_date="2026-07-05",
            end_date="2026-07-01",
        )
        assert "error" in result

    def test_insufficient_balance(self):
        # Requesting far more days than balance
        result = submit_leave_request(
            employee_id="E004",
            leave_type="sick",
            start_date="2026-01-01",
            end_date="2026-12-31",
        )
        assert "error" in result


class TestListLeaveRequests:
    def test_no_requests_initially(self):
        # E005 should have no requests unless a previous test submitted one
        result = list_leave_requests("E005")
        assert "error" not in result
        assert isinstance(result["requests"], list)

    def test_invalid_employee(self):
        result = list_leave_requests("E999")
        assert "error" in result


class TestGetPolicy:
    def test_leave_policy(self):
        result = get_policy("leave")
        assert result["found"] is True
        assert "Leave" in result["policy"]["title"]

    def test_remote_work_policy(self):
        result = get_policy("remote_work")
        assert result["found"] is True

    def test_unknown_policy(self):
        result = get_policy("intergalactic_travel")
        assert result["found"] is False


class TestListPolicies:
    def test_returns_list(self):
        policies = list_policies()
        assert isinstance(policies, list)
        assert len(policies) > 0


class TestSearchFaqs:
    def test_leave_question(self):
        results = search_faqs("How do I apply for leave?")
        assert len(results) > 0

    def test_benefits_question(self):
        results = search_faqs("What benefits does the company offer?")
        assert len(results) > 0

    def test_no_match(self):
        results = search_faqs("xyzzy gibberish nonsense")
        assert results == []


# ---------------------------------------------------------------------------
# Agent tests
# ---------------------------------------------------------------------------

class TestHRAgent:
    def setup_method(self):
        self.agent = HRAgent()

    def test_welcome(self):
        msg = self.agent.welcome()
        assert "HR Agent" in msg
        assert "help" in msg.lower()

    def test_greeting(self):
        response = self.agent.respond("Hello")
        assert response  # non-empty

    def test_help_command(self):
        response = self.agent.respond("help")
        assert "leave" in response.lower()

    def test_leave_balance_with_id(self):
        response = self.agent.respond("Check leave balance for E001")
        assert "Alice Johnson" in response
        assert "Annual" in response or "annual" in response

    def test_leave_balance_without_id(self):
        response = self.agent.respond("Check my leave balance")
        assert "employee ID" in response.lower() or "provide" in response.lower()

    def test_submit_leave_full_input(self):
        response = self.agent.respond(
            "Apply for annual leave from 2026-08-01 to 2026-08-03 for E001"
        )
        assert "✅" in response or "LR-" in response

    def test_submit_leave_missing_info(self):
        response = self.agent.respond("I want to take leave")
        assert "employee ID" in response.lower() or "leave type" in response.lower()

    def test_employee_lookup_by_id(self):
        response = self.agent.respond("Look up employee E003")
        assert "Carol White" in response

    def test_employee_lookup_by_name(self):
        response = self.agent.respond("Find employee Bob")
        assert "Bob Smith" in response

    def test_policy_lookup(self):
        response = self.agent.respond("What is the remote work policy?")
        assert "remote" in response.lower()

    def test_list_policies(self):
        response = self.agent.respond("List all policies")
        assert "Policy" in response

    def test_faq_expense(self):
        response = self.agent.respond("How do I claim expenses?")
        assert response  # non-empty

    def test_unknown_input(self):
        response = self.agent.respond("lalalalala")
        assert response  # graceful fallback

    def test_empty_input(self):
        response = self.agent.respond("")
        assert response  # non-empty

    def test_list_leave_requests(self):
        response = self.agent.respond("Show my leave requests for E001")
        assert response  # non-empty
