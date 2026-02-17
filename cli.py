#!/usr/bin/env python3

import argparse
import logging
import sys
from pathlib import Path
from typing import List
from dotenv import load_dotenv

load_dotenv()

from scanner import CodeScanner
from analyzer import CodeAnalyzer
from reporter import ReportGenerator
from github_pusher import GitHubPusher


def setup_logging(verbose: bool = False):
    """
    Configure logging for the application.
    
    Args:
        verbose: Enable debug logging if True
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main():
    """
    Main entry point for Sentinel Code Agent CLI.
    """
    parser = argparse.ArgumentParser(
        description='Sentinel Code Agent - Automated security and code quality analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sentinel_agent /path/to/project
  sentinel_agent /path/to/project --push
  sentinel_agent /path/to/project --push --github-token ghp_xxxxx
  sentinel_agent /path/to/project --verbose
        """
    )
    
    parser.add_argument(
        'project_path',
        type=str,
        help='Path to the project directory to analyze'
    )
    
    parser.add_argument(
        '--push',
        action='store_true',
        help='Push reports to GitHub after analysis'
    )
    
    parser.add_argument(
        '--github-token',
        type=str,
        help='GitHub personal access token (or set GITHUB_TOKEN env var)'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose debug logging'
    )
    
    parser.add_argument(
        '--max-files',
        type=int,
        default=None,
        help='Maximum number of files to analyze (useful for testing)'
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("=" * 70)
        logger.info("🛡️  SENTINEL CODE AGENT - Security Analysis Starting")
        logger.info("=" * 70)
        
        scanner = CodeScanner(args.project_path)
        code_files = scanner.scan()
        
        if not code_files:
            logger.warning("No code files found to analyze")
            sys.exit(0)
        
        if args.max_files:
            code_files = code_files[:args.max_files]
            logger.info(f"Limiting analysis to {args.max_files} files")
        
        logger.info(f"Analyzing {len(code_files)} files...")
        logger.info("-" * 70)
        
        analyzer = CodeAnalyzer()
        reporter = ReportGenerator(Path(args.project_path))
        
        all_results = []
        
        for idx, file_path in enumerate(code_files, 1):
            logger.info(f"[{idx}/{len(code_files)}] Processing: {file_path.name}")
            
            try:
                content = scanner.get_file_content(file_path)
                language = scanner.get_language(file_path)
                
                analysis_result = analyzer.analyze_file(file_path, content, language)
                all_results.append(analysis_result)
                
                reporter.generate_file_report(analysis_result)
                
                logger.info(f"✓ Completed: {file_path.name}")
                
            except Exception as e:
                logger.error(f"✗ Failed to process {file_path.name}: {str(e)}")
                all_results.append({
                    'file_path': str(file_path),
                    'file_name': file_path.name,
                    'language': scanner.get_language(file_path),
                    'status': 'error',
                    'analysis': f"Processing error: {str(e)}"
                })
        
        logger.info("-" * 70)
        logger.info("Generating summary report...")
        
        summary = analyzer.create_summary(all_results)
        reporter.generate_summary_report(summary)
        
        logger.info("✓ All reports generated successfully")
        logger.info(f"Reports location: {reporter.issues_dir}")
        
        if args.push:
            logger.info("-" * 70)
            logger.info("Pushing reports to GitHub...")
            
            try:
                pusher = GitHubPusher(
                    Path(args.project_path),
                    github_token=args.github_token
                )
                
                if pusher.push_reports():
                    logger.info("✓ Reports successfully pushed to GitHub")
                else:
                    logger.error("✗ Failed to push reports to GitHub")
                    sys.exit(1)
                    
            except ValueError as e:
                logger.error(f"✗ GitHub push error: {str(e)}")
                logger.info("Reports are still available locally in the issues/ directory")
                sys.exit(1)
            except Exception as e:
                logger.error(f"✗ Unexpected error during GitHub push: {str(e)}")
                logger.info("Reports are still available locally in the issues/ directory")
                sys.exit(1)
        
        logger.info("=" * 70)
        logger.info("🛡️  SENTINEL CODE AGENT - Analysis Complete")
        logger.info("=" * 70)
        
        logger.info(f"\n📊 Summary:")
        logger.info(f"   Files Analyzed: {len(all_results)}")
        logger.info(f"   Successful: {sum(1 for r in all_results if r['status'] == 'success')}")
        logger.info(f"   Failed: {sum(1 for r in all_results if r['status'] == 'error')}")
        logger.info(f"\n📂 Reports saved to: {reporter.issues_dir}")
        
        if args.push:
            logger.info(f"🔗 GitHub branch: sentinel-reports")
        
        logger.info("\n✓ All operations completed successfully\n")
        
    except FileNotFoundError as e:
        logger.error(f"✗ Error: {str(e)}")
        sys.exit(1)
    except NotADirectoryError as e:
        logger.error(f"✗ Error: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.warning("\n\n⚠️  Analysis interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"✗ Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
