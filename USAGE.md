# Sentinel Code Agent - Quick Start Guide

## Installation

### Option 1: Install as Package (Recommended)

```bash
cd sentinel_agent
pip install -e .
```

After installation, you can use the `sentinel-agent` command from anywhere:

```bash
sentinel-agent /path/to/your/project
```

### Option 2: Direct Execution

```bash
cd sentinel_agent
python run_sentinel.py /path/to/your/project
```

### Option 3: Module Execution

```bash
cd sentinel_agent
python -m cli /path/to/your/project
```

## Prerequisites

1. **Python 3.8+**

2. **Google AI API Key**: Set your API key as an environment variable

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

Or add it to a `.env` file in the sentinel_agent directory:

```
GOOGLE_API_KEY=your-api-key-here
```

3. **GitHub Token** (optional, for pushing reports):

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

## Usage Examples

### Basic Analysis

Analyze a project and generate reports locally:

```bash
sentinel-agent /path/to/your/project
```

### With GitHub Push

Analyze and automatically push reports to GitHub:

```bash
sentinel-agent /path/to/your/project --push
```

### Specify GitHub Token

```bash
sentinel-agent /path/to/your/project --push --github-token ghp_xxxxx
```

### Verbose Logging

For detailed debug information:

```bash
sentinel-agent /path/to/your/project --verbose
```

### Test with Limited Files

Analyze only the first N files (useful for testing):

```bash
sentinel-agent /path/to/your/project --max-files 5
```

### Combined Options

```bash
sentinel-agent /path/to/your/project --push --verbose --max-files 10
```

## GitHub Setup

### First Time Setup

1. **Initialize Git Repository** (if not already done):

```bash
cd /path/to/your/project
git init
git remote add origin https://github.com/username/repo.git
```

2. **Create GitHub Personal Access Token**:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` scope
   - Copy the token

3. **Set Token**:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

4. **Run Analysis with Push**:

```bash
sentinel-agent /path/to/your/project --push
```

The reports will be committed to a `sentinel-reports` branch.

## Output Structure

After running the analysis, you'll find:

```
your-project/
├── issues/
│   ├── SUMMARY.md           # Overall summary
│   ├── file1_report.md      # Individual reports
│   ├── file2_report.md
│   └── ...
└── [your code files]
```

## FastAPI Server Mode

To run as a web service:

```bash
cd sentinel_agent
python main.py
```

Access the API at `http://127.0.0.1:8001`

Interactive docs: `http://127.0.0.1:8001/docs`

## Troubleshooting

### "No module named 'google.adk'"

```bash
pip install google-adk
```

### "Authentication failed" when pushing to GitHub

1. Verify your GitHub token has `repo` permissions
2. Check that the token is correctly set:
   ```bash
   echo $GITHUB_TOKEN
   ```

### "Directory is not a Git repository"

Initialize Git in your project:

```bash
cd /path/to/your/project
git init
git remote add origin https://github.com/username/repo.git
```

### Permission Denied

Make scripts executable:

```bash
chmod +x run_sentinel.py
chmod +x cli.py
```

## Supported Languages

The agent currently analyzes:

- Python (.py)
- Java (.java)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Go (.go)
- Ruby (.rb)
- PHP (.php)
- C/C++ (.c, .cpp)
- C# (.cs)
- Swift (.swift)
- Kotlin (.kt)
- Rust (.rs)
- Scala (.scala)

## Examples of Full Workflows

### Local Analysis Only

```bash
export GOOGLE_API_KEY="your-key"
sentinel-agent ~/my-python-project
cat ~/my-python-project/issues/SUMMARY.md
```

### Analyze and Share on GitHub

```bash
export GOOGLE_API_KEY="your-key"
export GITHUB_TOKEN="ghp_your_token"
sentinel-agent ~/my-python-project --push
```

### Test on a Small Sample

```bash
export GOOGLE_API_KEY="your-key"
sentinel-agent ~/my-large-project --max-files 3 --verbose
```

## Environment Variables Summary

| Variable         | Required | Purpose                      |
| ---------------- | -------- | ---------------------------- |
| `GOOGLE_API_KEY` | Yes      | Google AI API authentication |
| `GITHUB_TOKEN`   | No       | GitHub push authentication   |

## Getting Help

```bash
sentinel-agent --help
```

## Next Steps

1. Review the generated reports in `issues/` directory
2. Fix CRITICAL and HIGH severity issues first
3. Re-run analysis to verify fixes
4. Set up CI/CD integration for automated scanning
