# 🛡️ Sentinel Code Agent

**An AI-powered code analysis tool for identifying security vulnerabilities, bugs, and bad coding practices.**

Sentinel Code Agent is an intelligent code reviewer that analyzes your codebase (Python, Java, and more), generates detailed security and quality reports, and optionally pushes findings to GitHub for team collaboration.

---

## ✨ Features

- **🔍 Comprehensive Code Analysis**
  - Security vulnerability detection (SQL injection, eval/exec usage, unsafe deserialization, etc.)
  - Bug and anti-pattern identification
  - Coding best practices enforcement
- **📊 Detailed Reporting**
  - Per-file analysis with actionable recommendations
  - Natural language feedback explaining issues and fixes
  - Organized report structure in `issues/` directory
  - System-wide summary reports

- **🔄 GitHub Integration**
  - Automatic report pushing to GitHub repositories
  - Issue tracking and version control integration
- **🚀 Flexible Interfaces**
  - **CLI**: Analyze files/directories directly from terminal
  - **FastAPI**: REST API for web integration and file uploads
- **🤖 AI-Powered Intelligence**
  - Uses Google's Gemini 2.5 Flash Lite model
  - Context-aware analysis with educational feedback
  - Mentors developers with clear explanations

---

## 🏗️ Architecture

```
sentinel_agent/
├── __init__.py         # Package initialization
├── agent.py            # Core AI agent logic
├── main.py             # FastAPI server setup
└── README.md           # This file

Generated Output:
issues/
├── file1_report.md     # Individual file reports
├── file2_report.md
└── summary_report.md   # Overall analysis summary
```

**Core Components:**

- **Agent**: Powered by Google ADK and Gemini AI for intelligent code review
- **FastAPI Server**: REST API for remote code analysis
- **CLI**: Command-line interface for local analysis
- **Report Generator**: Creates markdown reports with findings

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip or conda package manager
- (Optional) GitHub account and token for GitHub integration

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/sentinel-agent.git
   cd sentinel-agent
   ```

2. **Create virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install google-adk fastapi uvicorn
   ```

4. **Configure API Keys**

   Set up your Google AI API key:

   ```bash
   export GOOGLE_API_KEY="your-api-key-here"
   ```

   For GitHub integration (optional):

   ```bash
   export GITHUB_TOKEN="your-github-token"
   ```

---

## 🚀 Usage

### CLI Mode

Analyze a single file:

```bash
python -m sentinel_agent analyze path/to/your/code.py
```

Analyze an entire directory:

```bash
python -m sentinel_agent analyze path/to/your/project/
```

View results:

```bash
cat issues/summary_report.md
```

### FastAPI Server Mode

1. **Start the server**

   ```bash
   python main.py
   ```

   Server runs at: `http://127.0.0.1:8001`

2. **API Endpoints**

   **Health Check**

   ```bash
   curl http://127.0.0.1:8001/health
   ```

   **Analyze Code via POST**

   ```bash
   curl -X POST http://127.0.0.1:8001/analyze \
     -H "Content-Type: application/json" \
     -d '{"code": "import os; os.system(user_input)", "language": "python"}'
   ```

   **Upload File for Analysis**

   ```bash
   curl -X POST http://127.0.0.1:8001/upload \
     -F "file=@your_code.py"
   ```

3. **Interactive API Docs**

   Visit `http://127.0.0.1:8001/docs` for Swagger UI

---

## 📋 Report Structure

### Individual File Report (`issues/filename_report.md`)

```markdown
# Security Analysis: filename.py

## 🚨 Critical Issues

- **Line 42**: SQL Injection vulnerability detected
  - **Risk**: High
  - **Explanation**: Direct string concatenation in SQL query
  - **Fix**: Use parameterized queries instead

## ⚠️ Warnings

- **Line 15**: Bare except clause
  - **Risk**: Medium
  - **Recommendation**: Catch specific exceptions

## 💡 Suggestions

- Consider using type hints for better code clarity
- Add docstrings to public functions
```

### Summary Report (`issues/summary_report.md`)

```markdown
# Sentinel Code Agent - Analysis Summary

**Date**: 2026-02-16
**Files Analyzed**: 12
**Total Issues**: 23

## Statistics

- Critical: 5
- High: 8
- Medium: 7
- Low: 3

## Top Issues

1. SQL Injection vulnerabilities (3 occurrences)
2. Unsafe eval/exec usage (2 occurrences)
3. Missing input validation (5 occurrences)

## Recommendations

...
```

---

## 🔧 Configuration

### Agent Settings (`agent.py`)

Customize the agent behavior:

```python
root_agent = Agent(
    model="gemini-2.5-flash-lite",  # Change model
    name="sentinel_agent",
    description="Your custom description",
    instruction="Your custom instructions...",
)
```

### Server Settings (`main.py`)

Modify host and port:

```python
uvicorn.run(app, host="0.0.0.0", port=8080)
```

---

## 🐙 GitHub Integration

### Automatic Report Pushing

To enable automatic GitHub integration:

1. Set your GitHub token:

   ```bash
   export GITHUB_TOKEN="ghp_your_token_here"
   export GITHUB_REPO="username/repo-name"
   ```

2. Run analysis with GitHub push flag:

   ```bash
   python -m sentinel_agent analyze ./code --push-to-github
   ```

3. Reports will be committed to the `reports/` branch

---

## 🎯 Example Workflow

```bash
# 1. Start with a project directory
cd my-project/

# 2. Run Sentinel analysis
python -m sentinel_agent analyze ./src

# 3. Review the summary
cat issues/summary_report.md

# 4. Check individual file reports
ls issues/

# 5. (Optional) Push to GitHub
python -m sentinel_agent analyze ./src --push-to-github

# 6. Fix issues and re-analyze
# ... make fixes ...
python -m sentinel_agent analyze ./src
```

---

## 🛠️ Supported Languages

- ✅ Python (Full support)
- 🔄 Java (In development)
- 🔄 JavaScript/TypeScript (Planned)
- 🔄 Go (Planned)

---

## 🐛 Common Issues

**Issue**: `ModuleNotFoundError: No module named 'google.adk'`

- **Solution**: Install Google ADK: `pip install google-adk`

**Issue**: `Authentication Error`

- **Solution**: Ensure `GOOGLE_API_KEY` environment variable is set

**Issue**: `Permission denied when pushing to GitHub`

- **Solution**: Verify your `GITHUB_TOKEN` has repo write permissions

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Powered by [Google ADK](https://github.com/google/agent-development-kit)
- AI model: Gemini 2.5 Flash Lite
- Built with FastAPI and Uvicorn

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/sentinel-agent/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/sentinel-agent/wiki)
- **Email**: support@yourproject.com

---

**Sentinel Code Agent** - Your AI-powered code security guardian 🛡️
