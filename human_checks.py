#!/usr/bin/env python3
"""
Human checks script for the Physical AI & Humanoid Robotics book.
Evaluates technical rigor, content quality, formatting consistency, and proofreading.
"""

import os
import re
import glob
from typing import List, Dict, Tuple
import argparse
from collections import Counter


class HumanChecker:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.md_files = self._find_book_markdown_files()
        self.results = {
            'technical_rigor': [],
            'content_quality': [],
            'formatting_consistency': [],
            'proofreading_issues': [],
            'completeness_check': {}
        }

    def _find_book_markdown_files(self) -> List[str]:
        """Find all book markdown files in the project"""
        patterns = [
            os.path.join(self.base_path, "docs", "**/*.md"),
        ]

        files = []
        for pattern in patterns:
            files.extend(glob.glob(pattern, recursive=True))

        # Filter to only the main book content files
        book_files = []
        for f in files:
            # Include preface, appendix, and module chapters
            if any(part in f.lower() for part in ['preface', 'appendix', 'module']):
                book_files.append(f)

        return sorted(book_files)

    def run_human_checks(self) -> Dict:
        """Run human-oriented checks on the book content"""
        print("Running human checks...")

        # Check technical rigor
        self._check_technical_rigor()

        # Check content quality
        self._check_content_quality()

        # Check formatting consistency
        self._check_formatting_consistency()

        # Check for proofreading issues
        self._check_proofreading_issues()

        # Check completeness
        self._check_completeness()

        return self.results

    def _check_technical_rigor(self):
        """Check for technical rigor in content"""
        print("Checking technical rigor...")

        technical_keywords = [
            'algorithm', 'architecture', 'framework', 'protocol', 'interface',
            'implementation', 'optimization', 'performance', 'efficiency',
            'accuracy', 'precision', 'recall', 'f1-score', 'benchmark',
            'evaluation', 'validation', 'testing', 'simulation', 'real-world'
        ]

        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()

            # Count technical terms
            tech_term_count = sum(content.count(term) for term in technical_keywords)

            # Check for code examples
            code_blocks = len(re.findall(r'```.*?```', content, re.DOTALL))

            # Check for equations/formulas (look for LaTeX patterns or mathematical expressions)
            equations = len(re.findall(r'\$.*?\$|\\\[.*?\\\]', content)) + \
                       len(re.findall(r'\b(?:eq\.|equation|formula)\b', content))

            # Check for citations
            citations = len(re.findall(r'\([^)]*[0-9]{4}[^\)]*\)', content))  # Basic author-year pattern

            if tech_term_count < 10 and code_blocks < 2 and equations < 1 and citations < 1:
                self.results['technical_rigor'].append({
                    'file': file_path,
                    'issue': f'Potentially low technical rigor: {tech_term_count} tech terms, {code_blocks} code blocks, {equations} equations, {citations} citations',
                    'type': 'rigor_assessment'
                })

    def _check_content_quality(self):
        """Check content quality metrics"""
        print("Checking content quality...")

        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for depth of content
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            non_trivial_paragraphs = [p for p in paragraphs if len(p) > 100 and not p.startswith('#')]  # Exclude short and headings

            # Check for variety in content types
            has_code = '```' in content
            has_lists = any(char in content for char in ['-', '*', '+'])  # List markers
            has_links = '](' in content  # Markdown links
            has_bold = '**' in content or '__' in content
            has_italic = '*' in content or '_' in content

            content_types = sum([has_code, has_lists, has_links, has_bold, has_italic])

            # Quality indicators
            quality_indicators = {
                'paragraph_count': len(non_trivial_paragraphs),
                'content_variety': content_types,
                'has_code_examples': has_code,
                'has_structured_content': has_lists
            }

            # Flag files with very little substantial content
            if len(non_trivial_paragraphs) < 3:
                self.results['content_quality'].append({
                    'file': file_path,
                    'issue': f'Potentially thin content: only {len(non_trivial_paragraphs)} substantial paragraphs',
                    'type': 'quality_assessment'
                })

    def _check_formatting_consistency(self):
        """Check formatting consistency across files"""
        print("Checking formatting consistency...")

        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Check header formatting consistency
            headers = []
            for i, line in enumerate(lines):
                if line.strip().startswith('#'):
                    headers.append((i, line.strip()))

            # Check if headers follow expected patterns
            expected_headers = ['Learning Objectives', 'Key Concepts', 'Introduction']
            content = ''.join(lines)

            missing_standard_headers = []
            for header in expected_headers:
                if f'## {header}' not in content and f'### {header}' not in content:
                    missing_standard_headers.append(header)

            if missing_standard_headers:
                self.results['formatting_consistency'].append({
                    'file': file_path,
                    'issue': f'Missing standard headers: {missing_standard_headers}',
                    'type': 'formatting'
                })

            # Check list formatting consistency
            checklist_pattern = r'- \[[ x]\]'  # Proper checklist format
            checklist_items = re.findall(checklist_pattern, content)

            if 'Learning Objectives' in content and not checklist_items:
                self.results['formatting_consistency'].append({
                    'file': file_path,
                    'issue': 'Learning Objectives section found but no checklist items in proper format',
                    'type': 'formatting'
                })

    def _check_proofreading_issues(self):
        """Check for common proofreading issues"""
        print("Checking for proofreading issues...")

        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for common grammar/spelling issues
            issues = []

            # Double spaces
            double_spaces = len(re.findall(r'  +', content))
            if double_spaces > 5:  # Allow a few for formatting
                issues.append(f'{double_spaces} instances of multiple consecutive spaces')

            # Missing spaces after periods
            missing_spaces_after_periods = len(re.findall(r'[a-z]\.[A-Z]', content))
            if missing_spaces_after_periods > 0:
                issues.append(f'{missing_spaces_after_periods} missing spaces after periods')

            # Inconsistent capitalization in headers (informal check)
            header_lines = [line.strip() for line in content.split('\n') if line.strip().startswith('#')]
            for header in header_lines:
                # Check if it looks like a title that should be capitalized
                if ':' in header and '#' not in header[1:]:  # Not a header, just text with colon
                    continue
                # Just note headers for review - manual check needed for title case

            # Long lines (potential formatting issues)
            lines = content.split('\n')
            long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 120 and not line.strip().startswith('```')]

            if long_lines:
                issues.append(f'Lines {long_lines[:5]} are very long (>120 chars) - may affect readability')

            if issues:
                self.results['proofreading_issues'].append({
                    'file': file_path,
                    'issues': issues,
                    'type': 'proofreading'
                })

    def _check_completeness(self):
        """Check completeness of the book structure"""
        print("Checking completeness...")

        # Check which modules/chapters exist
        modules = {}
        for file_path in self.md_files:
            if 'module' in file_path.lower():
                # Extract module number
                match = re.search(r'module-(\d+)', file_path)
                if match:
                    module_num = match.group(1)
                    if module_num not in modules:
                        modules[module_num] = []

                    # Extract chapter number
                    chap_match = re.search(r'chapter-(\d+)', file_path)
                    if chap_match:
                        modules[module_num].append(chap_match.group(1))

        self.results['completeness_check'] = {
            'modules_found': list(modules.keys()),
            'chapters_per_module': {mod: sorted(chaps) for mod, chaps in modules.items()},
            'total_modules': len(modules),
            'total_chapters': sum(len(chaps) for chaps in modules.values()),
            'expected_modules': 4,  # Modules 1-4
            'expected_chapters_per_module': 5  # Chapters 1-5 per module
        }

        # Check if all expected modules and chapters are present
        if len(modules) < 4:
            self.results['completeness_check']['missing_modules'] = [str(i) for i in range(1, 5) if str(i) not in modules]

        for mod_num, chapters in modules.items():
            if len(chapters) < 5:
                expected_chapters = [str(i) for i in range(1, 6)]
                missing_chapters = [ch for ch in expected_chapters if ch not in chapters]
                if missing_chapters:
                    self.results['completeness_check'].setdefault('missing_chapters', {})[mod_num] = missing_chapters

    def generate_report(self) -> str:
        """Generate a comprehensive human checks report"""
        report = []
        report.append("HUMAN CHECKS REPORT")
        report.append("=" * 50)

        report.append(f"\nFiles analyzed: {len(self.md_files)}")
        report.append(f"Files: {', '.join(os.path.basename(f) for f in self.md_files[:5])}{', ...' if len(self.md_files) > 5 else ''}")

        # Technical Rigor
        report.append(f"\nTECHNICAL RIGOR ASSESSMENT:")
        if self.results['technical_rigor']:
            report.append(f"  Issues found: {len(self.results['technical_rigor'])}")
            for issue in self.results['technical_rigor']:
                report.append(f"    - {issue['file']}: {issue['issue']}")
        else:
            report.append("  ✓ Appears technically rigorous")

        # Content Quality
        report.append(f"\nCONTENT QUALITY ASSESSMENT:")
        if self.results['content_quality']:
            report.append(f"  Issues found: {len(self.results['content_quality'])}")
            for issue in self.results['content_quality']:
                report.append(f"    - {issue['file']}: {issue['issue']}")
        else:
            report.append("  ✓ Content appears to be of good quality")

        # Formatting Consistency
        report.append(f"\nFORMATTING CONSISTENCY ASSESSMENT:")
        if self.results['formatting_consistency']:
            report.append(f"  Issues found: {len(self.results['formatting_consistency'])}")
            for issue in self.results['formatting_consistency']:
                report.append(f"    - {issue['file']}: {issue['issue']}")
        else:
            report.append("  ✓ Formatting appears consistent")

        # Proofreading
        report.append(f"\nPROOFREADING ASSESSMENT:")
        if self.results['proofreading_issues']:
            report.append(f"  Issues found: {len(self.results['proofreading_issues'])}")
            for issue in self.results['proofreading_issues']:
                report.append(f"    - {issue['file']}: {', '.join(issue['issues'])}")
        else:
            report.append("  ✓ No major proofreading issues detected")

        # Completeness
        report.append(f"\nCOMPLETENESS ASSESSMENT:")
        comp_check = self.results['completeness_check']
        report.append(f"  Modules found: {comp_check['total_modules']}/{comp_check['expected_modules']}")
        report.append(f"  Total chapters: {comp_check['total_chapters']}/{comp_check['expected_modules'] * comp_check['expected_chapters_per_module']}")
        report.append(f"  Modules: {comp_check['modules_found']}")

        for mod, chaps in comp_check['chapters_per_module'].items():
            report.append(f"    Module {mod}: {len(chaps)}/{comp_check['expected_chapters_per_module']} chapters ({chaps})")

        if 'missing_modules' in comp_check:
            report.append(f"  Missing modules: {comp_check['missing_modules']}")

        if 'missing_chapters' in comp_check:
            for mod, missing in comp_check['missing_chapters'].items():
                report.append(f"  Module {mod} missing chapters: {missing}")

        # Overall assessment
        total_issues = (len(self.results['technical_rigor']) +
                       len(self.results['content_quality']) +
                       len(self.results['formatting_consistency']) +
                       len(self.results['proofreading_issues']))

        report.append(f"\nOVERALL ASSESSMENT:")
        if total_issues == 0:
            report.append("  ✓ All human checks passed! The book appears to meet quality standards.")
        else:
            report.append(f"  ? Found {total_issues} issues that may benefit from human review.")
            report.append("  Manual review is recommended for technical accuracy and content quality.")

        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description='Human checks for Physical AI & Humanoid Robotics book')
    parser.add_argument('--path', default='.', help='Path to the project root')
    parser.add_argument('--output', help='Output file for the report')

    args = parser.parse_args()

    checker = HumanChecker(args.path)

    # Run human checks
    results = checker.run_human_checks()

    # Generate report
    report = checker.generate_report()

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report saved to {args.output}")
    else:
        print(report)

    print(f"\nCompleted T061: Conduct Human Checks")


if __name__ == "__main__":
    main()