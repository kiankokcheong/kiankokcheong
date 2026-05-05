# 👋 Hi, I'm @kiankokcheong

- 👀 I'm interested in Python
- 🌱 I'm currently learning Python
- ��️ I'm looking to collaborate on Python
- 📫 How to reach me: kian.kok.cheong@intel.com

---

## 🤝 HR Agent

A conversational HR Agent built in Python that handles common HR queries through a simple CLI interface — no external APIs required.

### Features

| Capability | Example query |
|---|---|
| Check leave balance | `Check leave balance for E001` |
| Submit a leave request | `Apply for annual leave from 2026-06-01 to 2026-06-05 for E001` |
| View leave history | `Show my leave requests for E001` |
| Employee lookup | `Find employee Alice` / `Look up E003` |
| HR policy lookup | `What is the remote work policy?` |
| List all policies | `List all policies` |
| FAQ answering | `How do I claim expenses?` |

### Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the agent
python main.py
```

### Running Tests

```bash
python -m pytest tests/ -v
```

### Project Structure

```
hr_agent/
├── __init__.py        # Package entry point
├── agent.py           # HRAgent: intent classification & response routing
├── tools.py           # HR tools: leave, employee lookup, policies, FAQs
└── data/
    ├── __init__.py
    ├── employees.py   # Sample employee records & leave balances
    └── policies.py    # HR policies & FAQ bank
main.py                # CLI entry point
tests/
└── test_hr_agent.py   # Unit tests (39 tests)
requirements.txt
```

<!---
kiankokcheong/kiankokcheong is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
