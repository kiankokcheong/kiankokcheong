"""Company HR policies and FAQs."""

POLICIES = {
    "leave": {
        "title": "Leave Policy",
        "content": (
            "Annual Leave: Full-time employees receive 10–20 days of annual leave per year "
            "depending on tenure (0-2 years: 10 days, 2-5 years: 15 days, 5+ years: 20 days). "
            "Leave must be approved by your direct manager at least 3 business days in advance. "
            "Unused annual leave can be carried over up to a maximum of 5 days to the next year.\n\n"
            "Sick Leave: Employees receive 10 sick days per year. A medical certificate is required "
            "for absences exceeding 2 consecutive days.\n\n"
            "Personal Leave: Employees receive 3 personal leave days per year for personal matters. "
            "No documentation is required.\n\n"
            "Parental Leave: Primary caregivers receive 16 weeks of paid parental leave. "
            "Secondary caregivers receive 4 weeks of paid parental leave."
        ),
    },
    "remote_work": {
        "title": "Remote Work Policy",
        "content": (
            "Employees may work remotely up to 3 days per week with manager approval. "
            "Remote work must be done from a secure, private location. "
            "Employees are expected to be reachable during core hours (10 AM – 4 PM local time). "
            "All remote work arrangements must be documented and reviewed every 6 months."
        ),
    },
    "code_of_conduct": {
        "title": "Code of Conduct",
        "content": (
            "All employees are expected to treat each other with respect and professionalism. "
            "Harassment, discrimination, and bullying of any kind are strictly prohibited. "
            "Violations should be reported to HR immediately and will be investigated thoroughly. "
            "Retaliation against anyone who reports a concern in good faith is not tolerated."
        ),
    },
    "onboarding": {
        "title": "Onboarding Process",
        "content": (
            "New employees should complete the following steps within their first week:\n"
            "1. Complete all HR paperwork and compliance training via the HR portal.\n"
            "2. Set up company accounts (email, Slack, VPN, etc.) with IT support.\n"
            "3. Meet with your direct manager to discuss role expectations and 30/60/90-day goals.\n"
            "4. Attend the company-wide orientation session (held every other Monday).\n"
            "5. Complete the security awareness training within the first 5 business days."
        ),
    },
    "performance_review": {
        "title": "Performance Review Policy",
        "content": (
            "Performance reviews are conducted twice a year (June and December). "
            "Employees complete a self-assessment, which is reviewed by their manager. "
            "Ratings range from 1 (Needs Improvement) to 5 (Exceptional). "
            "Salary adjustments and promotions are considered during the December review cycle. "
            "Employees who receive a rating of 1 will be placed on a Performance Improvement Plan (PIP)."
        ),
    },
    "expense_reimbursement": {
        "title": "Expense Reimbursement Policy",
        "content": (
            "Business expenses must be submitted within 30 days of being incurred. "
            "All expenses over $50 require a receipt. "
            "Expenses must be approved by your manager before submission to Finance. "
            "Reimbursements are processed within 2 weeks of submission approval. "
            "Travel expenses for flights over $500 require pre-approval from your department head."
        ),
    },
}

FAQS = [
    {
        "question": "How do I apply for leave?",
        "answer": (
            "Submit a leave request through the HR portal at least 3 business days in advance. "
            "Your manager will be notified by email and must approve or reject the request. "
            "You will receive a confirmation email once the request is processed."
        ),
        "keywords": ["apply", "leave", "request", "vacation", "time off", "holiday"],
    },
    {
        "question": "How do I check my leave balance?",
        "answer": (
            "You can check your leave balance through the HR portal under 'My Leave'. "
            "You can also ask the HR Agent by providing your employee ID."
        ),
        "keywords": ["check", "balance", "leave", "remaining", "days left", "how many days"],
    },
    {
        "question": "What is the process for expense reimbursement?",
        "answer": (
            "Submit expense claims via the Finance portal with all required receipts. "
            "Get your manager's approval, then submit to the Finance team. "
            "Reimbursements are processed within 2 weeks."
        ),
        "keywords": ["expense", "reimbursement", "claim", "receipt", "money back"],
    },
    {
        "question": "Who do I contact for IT issues?",
        "answer": (
            "For IT issues, contact the IT Help Desk at helpdesk@company.com or call +1-555-0999. "
            "For urgent issues, use the IT emergency line: +1-555-0998."
        ),
        "keywords": ["IT", "computer", "laptop", "software", "hardware", "helpdesk", "tech support"],
    },
    {
        "question": "How do I update my personal information?",
        "answer": (
            "Log into the HR portal and navigate to 'My Profile' to update personal details "
            "such as address, emergency contacts, and bank details. "
            "For legal name changes, please submit supporting documents to HR directly."
        ),
        "keywords": ["update", "personal", "information", "profile", "address", "name", "bank"],
    },
    {
        "question": "What are the core working hours?",
        "answer": (
            "Core working hours are 10 AM to 4 PM in your local time zone, Monday to Friday. "
            "Outside of core hours, flexible scheduling is permitted with manager approval."
        ),
        "keywords": ["working hours", "core hours", "schedule", "work time", "office hours"],
    },
    {
        "question": "How do I report a workplace concern?",
        "answer": (
            "Workplace concerns can be reported to HR via email at hr@company.com, "
            "or anonymously through the Ethics Hotline at ethics@company.com. "
            "All reports are handled confidentially."
        ),
        "keywords": ["report", "concern", "complaint", "harassment", "issue", "problem", "ethics"],
    },
    {
        "question": "What benefits does the company offer?",
        "answer": (
            "The company offers: health, dental, and vision insurance; 401(k) with 4% company match; "
            "employee stock purchase plan; wellness reimbursement up to $500/year; "
            "learning & development budget of $1,000/year; and commuter benefits."
        ),
        "keywords": ["benefits", "insurance", "health", "dental", "vision", "401k", "retirement", "perks"],
    },
]
