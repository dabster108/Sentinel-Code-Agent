"""
Sentinel Code Agent - AI-powered code security and quality analysis tool.

This package provides automated code review capabilities using AI to detect
security vulnerabilities, bugs, and bad coding practices.
"""

__version__ = "1.0.0"
__author__ = "Sentinel Team"

from .scanner import CodeScanner
from .analyzer import CodeAnalyzer
from .reporter import ReportGenerator
from .github_pusher import GitHubPusher

__all__ = [
    'CodeScanner',
    'CodeAnalyzer',
    'ReportGenerator',
    'GitHubPusher',
]
