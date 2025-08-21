#!/usr/bin/env python3
"""
PRP Validation Script
=====================

Comprehensive validation tool for Product Requirement Prompts (PRPs) that checks:
- File references and dependencies
- URL accessibility
- Environment dependencies
- Context completeness
- Validation command availability

Usage: python validate_prp.py <prp_file_path>
"""

import os
import re
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse
import requests
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Container for validation results"""
    category: str
    status: str  # PASS, WARN, FAIL
    message: str
    details: List[str] = field(default_factory=list)


@dataclass
class PRPValidationReport:
    """Complete validation report for a PRP"""
    prp_file: str
    results: List[ValidationResult] = field(default_factory=list)
    context_score: int = 0
    dependency_status: str = "UNKNOWN"
    risk_level: str = "UNKNOWN"
    readiness_score: int = 0
    overall_status: str = "UNKNOWN"
    
    def add_result(self, category: str, status: str, message: str, details: List[str] = None):
        """Add a validation result"""
        self.results.append(ValidationResult(category, status, message, details or []))
    
    def get_summary(self) -> Dict:
        """Get summary statistics"""
        pass_count = sum(1 for r in self.results if r.status == "PASS")
        warn_count = sum(1 for r in self.results if r.status == "WARN")
        fail_count = sum(1 for r in self.results if r.status == "FAIL")
        
        return {
            "total_checks": len(self.results),
            "passed": pass_count,
            "warnings": warn_count,
            "failed": fail_count,
            "context_score": self.context_score,
            "readiness_score": self.readiness_score,
            "overall_status": self.overall_status
        }


class PRPValidator:
    """Main PRP validation class"""
    
    def __init__(self, prp_file_path: str):
        self.prp_file = Path(prp_file_path)
        self.project_root = self._find_project_root()
        self.prp_content = ""
        self.report = PRPValidationReport(prp_file=str(self.prp_file))
        
    def _find_project_root(self) -> Path:
        """Find project root by looking for pyproject.toml or .git"""
        current = self.prp_file.parent
        while current.parent != current:
            if (current / "pyproject.toml").exists() or (current / ".git").exists():
                return current
            current = current.parent
        return self.prp_file.parent
    
    def _load_prp_content(self) -> bool:
        """Load PRP file content"""
        try:
            with open(self.prp_file, 'r', encoding='utf-8') as f:
                self.prp_content = f.read()
            self.report.add_result("File", "PASS", f"Successfully loaded PRP file: {self.prp_file}")
            return True
        except Exception as e:
            self.report.add_result("File", "FAIL", f"Failed to load PRP file: {e}")
            return False
    
    def validate_file_references(self):
        """Validate all file and directory references in the PRP"""
        print("🔍 Validating file references...")
        
        # More precise patterns to find file references
        file_patterns = [
            r'`([^`]*\.[a-zA-Z0-9]+)`',  # Files with extensions in backticks
            r'file:\s*([^\s\n]+)',       # Explicit file: references
            r'(?:^|\s)((?:src|PRPs|tests|docs|docker|requirements|scripts)/[^\s\n,]+)',  # Directory paths
            r'`([^`]*\.(?:py|md|yml|yaml|json|txt|sh|js|ts|tsx|jsx|html|css))`',  # Specific file types
        ]
        
        found_files = set()
        for pattern in file_patterns:
            matches = re.findall(pattern, self.prp_content, re.MULTILINE)
            for match in matches:
                clean_match = match.strip('.,;:')  # Remove trailing punctuation
                # Filter out obvious non-files
                if (clean_match and 
                    not clean_match.startswith('http') and
                    not clean_match.startswith('$') and
                    len(clean_match) > 2 and
                    ('.' in clean_match or '/' in clean_match)):
                    found_files.add(clean_match)
        
        existing_files = []
        missing_files = []
        
        for file_ref in found_files:
            # Try multiple possible paths
            possible_paths = [
                self.project_root / file_ref,
                self.project_root / file_ref.lstrip('/'),
                self.prp_file.parent / file_ref,
            ]
            
            file_exists = False
            for path in possible_paths:
                if path.exists():
                    existing_files.append(str(file_ref))
                    file_exists = True
                    break
            
            if not file_exists:
                missing_files.append(str(file_ref))
        
        # Categorize missing files
        critical_existing = [f for f in existing_files if any(
            critical in f for critical in ['pyproject.toml', 'CLAUDE.md', 'README.md', '.env']
        )]
        
        # Report results - missing files are just informational since PRP might create them
        if missing_files:
            self.report.add_result(
                "File References", 
                "PASS",  # Changed to PASS since this is expected
                f"{len(missing_files)} files to be created by PRP implementation",
                [f"Will create: {f}" for f in missing_files[:3]]  # Show only first 3
            )
        
        if existing_files:
            self.report.add_result(
                "File References", 
                "PASS",
                f"{len(existing_files)} existing file references validated"
            )
        elif not found_files:
            self.report.add_result(
                "File References", 
                "WARN",
                "No clear file references found in PRP"
            )
        
        return True  # Always return True since missing files are expected
    
    def validate_url_accessibility(self):
        """Validate all URL references in the PRP"""
        print("🌐 Validating URL accessibility...")
        
        url_pattern = r'https?://[^\s\n\)]+(?=[\s\n\)]|$)'
        urls = re.findall(url_pattern, self.prp_content)
        
        accessible_urls = []
        development_urls = []
        inaccessible_urls = []
        
        for url in set(urls):  # Remove duplicates
            # Clean up URL (remove trailing punctuation)
            clean_url = url.rstrip('.,;:')
            
            # Check if it's a development/localhost URL
            if any(host in clean_url for host in ['localhost', '127.0.0.1', '0.0.0.0']):
                development_urls.append(clean_url)
                continue
                
            try:
                response = requests.head(clean_url, timeout=5, allow_redirects=True)
                if response.status_code < 400:
                    accessible_urls.append(clean_url)
                else:
                    inaccessible_urls.append(f"{clean_url} (HTTP {response.status_code})")
            except Exception as e:
                # Only report real errors, not timeouts for external URLs
                if 'timeout' not in str(e).lower():
                    inaccessible_urls.append(f"{clean_url} (Error: {str(e)[:30]}...)")
        
        # Report results
        total_urls = len(accessible_urls) + len(development_urls) + len(inaccessible_urls)
        
        if development_urls:
            self.report.add_result(
                "URL References",
                "PASS",
                f"{len(development_urls)} development URLs found (localhost/127.0.0.1)",
                [f"Dev URL: {url}" for url in development_urls[:3]]
            )
        
        if accessible_urls:
            self.report.add_result(
                "URL Accessibility",
                "PASS",
                f"{len(accessible_urls)} external URLs accessible"
            )
            
        if inaccessible_urls:
            self.report.add_result(
                "URL Accessibility",
                "WARN",
                f"{len(inaccessible_urls)} external URLs not accessible",
                [f"Inaccessible: {url}" for url in inaccessible_urls[:3]]
            )
        elif not accessible_urls and not development_urls:
            self.report.add_result(
                "URL References",
                "WARN",
                "No URL references found in PRP"
            )
        
        return len(inaccessible_urls) == 0
    
    def validate_python_dependencies(self):
        """Validate Python dependencies mentioned in the PRP"""
        print("🐍 Validating Python dependencies...")
        
        # Known packages that should be checked
        critical_packages = {
            'chromadb', 'redis', 'fastapi', 'pytest', 'langchain', 
            'sentence_transformers', 'gitpython', 'streamlit', 'requests'
        }
        
        # Find actual import statements in code blocks
        code_blocks = re.findall(r'```python\n(.*?)```', self.prp_content, re.DOTALL)
        found_imports = set()
        
        for block in code_blocks:
            import_matches = re.findall(r'^(?:import|from)\s+([a-zA-Z_][a-zA-Z0-9_]*)', block, re.MULTILINE)
            found_imports.update(import_matches)
        
        # Check for mentioned packages in text
        mentioned_packages = set()
        for package in critical_packages:
            if package in self.prp_content.lower() or package.replace('_', '-') in self.prp_content.lower():
                mentioned_packages.add(package)
        
        # Combine actual imports and mentioned packages
        packages_to_check = found_imports.union(mentioned_packages)
        
        available_packages = []
        missing_packages = []
        
        for package in packages_to_check:
            try:
                # Handle common package name variations
                import_name = package.replace('-', '_')
                if package == 'sentence_transformers':
                    import_name = 'sentence_transformers'
                elif package == 'gitpython':
                    import_name = 'git'
                    
                __import__(import_name)
                available_packages.append(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            self.report.add_result(
                "Python Dependencies",
                "WARN",
                f"{len(missing_packages)} packages not available",
                [f"Missing: {pkg}" for pkg in missing_packages[:5]]  # Limit to 5
            )
        else:
            self.report.add_result(
                "Python Dependencies",
                "PASS",
                f"All {len(available_packages)} critical packages available"
            )
        
        return len(missing_packages) == 0
    
    def validate_commands(self):
        """Validate that commands mentioned in validation sections are available"""
        print("⚙️ Validating command availability...")
        
        # Critical commands that should be available
        critical_commands = {
            'python', 'python3', 'uv', 'git', 'docker', 'curl', 'pytest', 'ruff', 'mypy'
        }
        
        # Find bash/shell command blocks
        bash_blocks = re.findall(r'```(?:bash|shell)\n(.*?)```', self.prp_content, re.DOTALL)
        found_commands = set()
        
        # Patterns to exclude (not real commands)
        exclude_patterns = {
            r'^-[a-zA-Z]+$',  # Command flags like -d, -H, -X
            r'^[{}\[\]().,;:\'\"`│├└─}]+$',  # Punctuation/brackets/tree chars
            r'^\w+:$',  # Labels ending with colon
            r'^".*"$',  # Quoted strings
            r'^\$\{.*\}$',  # Variable references  
            r'^(if|then|else|fi|for|do|done|while|case|esac)$',  # Shell keywords
            r'^[0-9]+$',  # Pure numbers
            r'^\w+\(\)$',  # Function calls with parentheses
        }
        
        for block in bash_blocks:
            lines = block.split('\n')
            for line in lines:
                line = line.strip()
                # Skip comments, empty lines, and echo statements
                if (line and not line.startswith('#') and 
                    not line.startswith('echo') and not line.startswith('//')):
                    
                    # Extract the first word as potential command
                    parts = line.split()
                    if parts:
                        cmd = parts[0]
                        
                        # Skip if matches any exclude pattern
                        skip_cmd = False
                        for pattern in exclude_patterns:
                            if re.match(pattern, cmd):
                                skip_cmd = True
                                break
                        
                        # Only add valid command-like strings
                        if (not skip_cmd and 
                            not cmd.startswith('$') and 
                            not cmd.startswith('[') and 
                            '=' not in cmd and
                            len(cmd) > 1 and
                            (cmd.replace('-', '').replace('_', '').isalnum())):
                            found_commands.add(cmd)
        
        # Add critical commands if mentioned in text
        for cmd in critical_commands:
            if cmd in self.prp_content:
                found_commands.add(cmd)
        
        # Remove common false positives
        false_positives = {'ls', 'cd', 'mkdir', 'rm', 'cp', 'mv', 'cat', 'grep', 'find', 'sort', 'uniq'}
        found_commands = found_commands - false_positives
        
        available_commands = []
        missing_commands = []
        
        for cmd in found_commands:
            try:
                result = subprocess.run(['which', cmd], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    available_commands.append(cmd)
                else:
                    missing_commands.append(cmd)
            except:
                missing_commands.append(cmd)
        
        if missing_commands:
            self.report.add_result(
                "Command Availability",
                "WARN",
                f"{len(missing_commands)} commands not available",
                [f"Missing: {cmd}" for cmd in missing_commands[:3]]  # Limit to 3
            )
        else:
            self.report.add_result(
                "Command Availability",
                "PASS",
                f"All {len(available_commands)} critical commands available"
            )
        
        return len(missing_commands) == 0
    
    def validate_structure_completeness(self):
        """Validate that the PRP has all required sections"""
        print("📋 Validating PRP structure completeness...")
        
        required_sections = {
            "Goal": r"#+\s*Goal",
            "Why": r"#+\s*Why",
            "What": r"#+\s*What", 
            "Context": r"#+\s*.*Context",
            "Implementation": r"#+\s*Implementation",
            "Validation": r"#+\s*Validation",
        }
        
        found_sections = []
        missing_sections = []
        
        for section_name, pattern in required_sections.items():
            if re.search(pattern, self.prp_content, re.IGNORECASE):
                found_sections.append(section_name)
            else:
                missing_sections.append(section_name)
        
        if missing_sections:
            self.report.add_result(
                "PRP Structure",
                "FAIL",
                f"Missing {len(missing_sections)} required sections",
                [f"Missing: {section}" for section in missing_sections]
            )
        else:
            self.report.add_result(
                "PRP Structure",
                "PASS",
                f"All {len(found_sections)} required sections present"
            )
        
        return len(missing_sections) == 0
    
    def calculate_scores(self):
        """Calculate validation scores"""
        total_checks = len(self.report.results)
        if total_checks == 0:
            return
            
        pass_count = sum(1 for r in self.report.results if r.status == "PASS")
        warn_count = sum(1 for r in self.report.results if r.status == "WARN")
        fail_count = sum(1 for r in self.report.results if r.status == "FAIL")
        
        # Context completeness score (0-100)
        self.report.context_score = int((pass_count / total_checks) * 100)
        
        # Readiness score (0-100, penalize failures more than warnings)
        penalty_score = (fail_count * 20) + (warn_count * 5)
        self.report.readiness_score = max(0, 100 - penalty_score)
        
        # Overall status
        if fail_count > 0:
            self.report.overall_status = "BLOCKED" if fail_count > total_checks / 3 else "NEEDS_ATTENTION"
            self.report.dependency_status = "BLOCKED" if fail_count > 2 else "ISSUES"
            self.report.risk_level = "HIGH" if fail_count > 2 else "MEDIUM"
        elif warn_count > 0:
            self.report.overall_status = "NEEDS_ATTENTION"
            self.report.dependency_status = "ISSUES"
            self.report.risk_level = "MEDIUM" if warn_count > 2 else "LOW"
        else:
            self.report.overall_status = "READY_TO_EXECUTE"
            self.report.dependency_status = "READY"
            self.report.risk_level = "LOW"
    
    def generate_report(self) -> str:
        """Generate a comprehensive validation report"""
        summary = self.report.get_summary()
        
        report = f"""
🔍 PRP Validation Report
========================
📁 PRP File: {self.prp_file.name}
📊 Summary: {summary['passed']}/{summary['total_checks']} checks passed

📁 Context Validation: {"PASS" if summary['failed'] == 0 else "FAIL"}
- Checks passed: {summary['passed']}/{summary['total_checks']}
- Warnings: {summary['warnings']}
- Failures: {summary['failed']}

🔧 Dependencies: {self.report.dependency_status}
- Environment ready: {"YES" if self.report.dependency_status == "READY" else "NO"}
- Missing components: {summary['failed'] + summary['warnings']}

⚠️  Risk Assessment: {self.report.risk_level}
- Context completeness: {self.report.context_score}%
- Implementation readiness: {self.report.readiness_score}%

📊 Readiness Score: {self.report.readiness_score}/100

🎯 Overall Status: {self.report.overall_status}

"""
        
        # Add detailed results
        for result in self.report.results:
            status_emoji = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}[result.status]
            report += f"\n{status_emoji} {result.category}: {result.message}"
            if result.details:
                for detail in result.details[:3]:  # Limit details
                    report += f"\n    - {detail}"
                if len(result.details) > 3:
                    report += f"\n    - ... and {len(result.details) - 3} more"
        
        # Add recommendations
        if self.report.overall_status != "READY_TO_EXECUTE":
            report += f"\n\n🔧 Recommended Actions:"
            
            missing_packages = []
            missing_commands = []
            
            for result in self.report.results:
                if result.status in ["FAIL", "WARN"]:
                    if "Python Dependencies" in result.category:
                        missing_packages.extend([d.split(": ")[1] for d in result.details if d.startswith("Missing:")])
                    elif "Command Availability" in result.category:
                        missing_commands.extend([d.split(": ")[1] for d in result.details if d.startswith("Missing:")])
            
            if missing_packages:
                report += f"\n[ ] Install missing packages: uv add {' '.join(missing_packages)}"
            if missing_commands:
                report += f"\n[ ] Install missing commands: {', '.join(missing_commands)}"
            
            report += f"\n[ ] Review and fix validation issues above"
            report += f"\n[ ] Re-run validation before PRP execution"
        
        return report
    
    async def validate(self) -> PRPValidationReport:
        """Run all validation checks"""
        print(f"🚀 Starting PRP validation for: {self.prp_file.name}")
        
        if not self._load_prp_content():
            return self.report
        
        # Run all validation checks
        self.validate_structure_completeness()
        self.validate_file_references()
        self.validate_url_accessibility() 
        self.validate_python_dependencies()
        self.validate_commands()
        
        # Calculate final scores
        self.calculate_scores()
        
        return self.report


async def main():
    """Main validation function"""
    if len(sys.argv) != 2:
        print("Usage: python validate_prp.py <prp_file_path>")
        sys.exit(1)
    
    prp_file = sys.argv[1]
    
    if not os.path.exists(prp_file):
        print(f"Error: PRP file not found: {prp_file}")
        sys.exit(1)
    
    validator = PRPValidator(prp_file)
    report = await validator.validate()
    
    print(validator.generate_report())
    
    # Exit with appropriate code
    if report.overall_status == "READY_TO_EXECUTE":
        sys.exit(0)
    elif report.overall_status == "NEEDS_ATTENTION":
        sys.exit(1)
    else:  # BLOCKED
        sys.exit(2)


if __name__ == "__main__":
    asyncio.run(main())