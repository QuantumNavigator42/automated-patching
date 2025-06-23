# 🛠️ Automated Patching

A self-healing Python execution framework powered by OpenAI’s GPT models. This system detects runtime failures, generates intelligent code patches, and attempts repair cycles—fully automated from log to patch.

---

## 🚀 Overview

This project runs a Python script, captures any errors, and invokes a language model to automatically fix the code. Each patch is applied and re-run in a controlled loop with safety limits.

### ✨ Features
- **Self-healing loop**: Automatically retries up to MAX_ITERATIONS = 2
- **LLM-based refactoring**: Uses OpenAI to propose and apply fixes
- **Logging**: All runs and outputs stored in the logs/ directory
- **Safe target execution**: Isolated test script in 	argets/
- **Stub modules**: Hooks for future uploads and maintenance tools

---

## 🗂️ Project Structure

\\\
automated-patching/
├── src/
│   ├── auto_runner.py       # Main orchestrator
│   └── utils/
│       ├── refactor.py      # GPT-powered patch generator
│       ├── upload.py        # (stub) upload system
│       └── maintenance.py   # (stub) auto-formatting and cleanup
├── targets/
│   └── demo_target.py       # Sample script to test healing
├── tests/
│   └── test_demo_target.py  # Pytest placeholder
├── logs/                    # Logs from each run
├── requirements.txt
└── README.md
\\\

---

## 🧪 Usage

1. Set environment variables:
   \\\ash
   export OPENAI_API_KEY_CYC=your-key
   \\\

2. Run the runner:
   \\\ash
   python src/auto_runner.py
   \\\

3. Watch logs:
   - \logs/runner.log\
   - \logs/iter_1.log\, \logs/iter_2.log\, ...

---

## 🔧 Configuration

Edit these values in \uto_runner.py\:
\\\python
MAX_ITERATIONS = 2
UPLOAD_ENABLED = False
\\\

---

## 📦 Installation

\\\ash
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
pip install -r requirements.txt
\\\

---

## 📄 License

MIT License
