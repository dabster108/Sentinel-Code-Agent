import os
from pathlib import Path
from typing import List, Set
import logging

logger = logging.getLogger(__name__)


class CodeScanner:
    
    SUPPORTED_EXTENSIONS = {
        '.py', '.java', '.js', '.ts', '.jsx', '.tsx',
        '.go', '.rb', '.php', '.cpp', '.c', '.cs',
        '.swift', '.kt', '.rs', '.scala'
    }
    
    EXCLUDED_DIRS = {
        'node_modules', '__pycache__', '.git', '.venv',
        'venv', 'env', 'build', 'dist', '.adk',
        'target', 'bin', 'obj', '.next', '.cache'
    }
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        if not self.project_path.exists():
            raise FileNotFoundError(f"Project directory not found: {project_path}")
        if not self.project_path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {project_path}")
    
    def scan(self) -> List[Path]:
        """
        Scan the project directory for code files.
        
        Returns:
            List of Path objects for code files found
        """
        logger.info(f"Scanning directory: {self.project_path}")
        code_files = []
        
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in self.EXCLUDED_DIRS]
            
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                    code_files.append(file_path)
                    logger.debug(f"Found code file: {file_path.relative_to(self.project_path)}")
        
        logger.info(f"Found {len(code_files)} code files")
        return code_files
    
    def get_file_content(self, file_path: Path) -> str:
        """
        Read and return the content of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Content of the file as string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            logger.warning(f"Could not decode file {file_path}, trying with latin-1 encoding")
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    def get_language(self, file_path: Path) -> str:
        """
        Determine the programming language based on file extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Language name as string
        """
        extension_map = {
            '.py': 'Python',
            '.java': 'Java',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'JavaScript React',
            '.tsx': 'TypeScript React',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.rs': 'Rust',
            '.scala': 'Scala'
        }
        return extension_map.get(file_path.suffix.lower(), 'Unknown')
