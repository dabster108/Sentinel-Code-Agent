from pathlib import Path
from datetime import datetime
import logging
import subprocess
import os

logger = logging.getLogger(__name__)


class GitHubPusher:
    
    BRANCH_NAME = "sentinel-reports"
    
    def __init__(self, project_path: Path, github_token: str = None):
        self.project_path = project_path
        self.github_token = github_token or os.environ.get('GITHUB_TOKEN')
        self.issues_dir = project_path / 'issues'
        
        if not self._is_git_repo():
            raise ValueError(f"Directory is not a Git repository: {project_path}")
    
    def _is_git_repo(self) -> bool:
        """
        Check if the directory is a Git repository.
        
        Returns:
            True if it's a Git repo, False otherwise
        """
        git_dir = self.project_path / '.git'
        return git_dir.exists() and git_dir.is_dir()
    
    def _run_git_command(self, command: list) -> tuple:
        """
        Run a Git command and return the result.
        
        Args:
            command: List of command arguments
            
        Returns:
            Tuple of (success: bool, output: str)
        """
        try:
            result = subprocess.run(
                command,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {' '.join(command)}")
            logger.error(f"Error: {e.stderr}")
            return False, e.stderr
    
    def _configure_git_auth(self):
        """
        Configure Git authentication using the GitHub token.
        """
        if self.github_token:
            logger.info("Configuring Git authentication with GitHub token")
            
            success, remote_url = self._run_git_command(['git', 'remote', 'get-url', 'origin'])
            if success and remote_url:
                if remote_url.startswith('https://github.com/'):
                    repo_path = remote_url.replace('https://github.com/', '')
                    authenticated_url = f"https://{self.github_token}@github.com/{repo_path}"
                    self._run_git_command(['git', 'remote', 'set-url', 'origin', authenticated_url])
    
    def _get_current_branch(self) -> str:
        """
        Get the current Git branch name.
        
        Returns:
            Current branch name
        """
        success, branch = self._run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        return branch if success else 'main'
    
    def _branch_exists(self, branch_name: str) -> bool:
        """
        Check if a branch exists locally.
        
        Args:
            branch_name: Name of the branch
            
        Returns:
            True if branch exists, False otherwise
        """
        success, _ = self._run_git_command(['git', 'rev-parse', '--verify', branch_name])
        return success
    
    def push_reports(self) -> bool:
        """
        Stage, commit, and push reports to GitHub.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Starting GitHub push process...")
            
            if self.github_token:
                self._configure_git_auth()
            
            original_branch = self._get_current_branch()
            logger.info(f"Current branch: {original_branch}")
            
            if self._branch_exists(self.BRANCH_NAME):
                logger.info(f"Switching to existing branch: {self.BRANCH_NAME}")
                success, _ = self._run_git_command(['git', 'checkout', self.BRANCH_NAME])
                if not success:
                    logger.error(f"Failed to checkout branch: {self.BRANCH_NAME}")
                    return False
            else:
                logger.info(f"Creating new branch: {self.BRANCH_NAME}")
                success, _ = self._run_git_command(['git', 'checkout', '-b', self.BRANCH_NAME])
                if not success:
                    logger.error(f"Failed to create branch: {self.BRANCH_NAME}")
                    return False
            
            logger.info("Staging report files...")
            success, _ = self._run_git_command(['git', 'add', 'issues/'])
            if not success:
                logger.error("Failed to stage files")
                return False
            
            status_success, status = self._run_git_command(['git', 'status', '--porcelain'])
            if status_success and not status:
                logger.info("No changes to commit")
                self._run_git_command(['git', 'checkout', original_branch])
                return True
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Sentinel Analysis Report - {timestamp}"
            
            logger.info(f"Committing changes: {commit_message}")
            success, _ = self._run_git_command(['git', 'commit', '-m', commit_message])
            if not success:
                logger.error("Failed to commit changes")
                self._run_git_command(['git', 'checkout', original_branch])
                return False
            
            logger.info(f"Pushing to remote: {self.BRANCH_NAME}")
            success, output = self._run_git_command(['git', 'push', '-u', 'origin', self.BRANCH_NAME])
            
            if not success:
                if "fatal: Authentication failed" in output or "fatal: could not read Password" in output:
                    logger.error("GitHub authentication failed. Please set GITHUB_TOKEN environment variable")
                else:
                    logger.error("Failed to push to GitHub")
                
                self._run_git_command(['git', 'checkout', original_branch])
                return False
            
            logger.info("✓ Successfully pushed reports to GitHub")
            
            self._run_git_command(['git', 'checkout', original_branch])
            logger.info(f"Switched back to branch: {original_branch}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error during GitHub push: {str(e)}")
            try:
                self._run_git_command(['git', 'checkout', original_branch])
            except:
                pass
            return False
