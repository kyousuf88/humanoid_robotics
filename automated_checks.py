#!/usr/bin/env python3
"""
Automated checks script for the Physical AI & Humanoid Robotics book.
Performs checks for accuracy, clarity, reproducibility, formatting consistency, and plagiarism indicators.
"""

import os
import re
import glob
from typing import List, Dict, Tuple
import requests
from collections import Counter
import argparse


class AutomatedChecker:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.md_files = self._find_markdown_files()
        self.results = {
            'formatting_issues': [],
            'content_issues': [],
            'consistency_issues': [],
            'potential_plagiarism': [],
            'word_counts': {},
            'readability_metrics': {}
        }

    def _find_markdown_files(self) -> List[str]:
        """Find all markdown files in the project"""
        patterns = [
            os.path.join(self.base_path, "**/*.md"),
            os.path.join(self.base_path, "docs/**/*.md"),
            os.path.join(self.base_path, "specs/**/*.md")
        ]

        files = []
        for pattern in patterns:
            files.extend(glob.glob(pattern, recursive=True))

        # Filter out template files that are not part of the main content
        main_files = [f for f in files if not any(exclude in f for exclude in ['.specify', 'templates', 'history'])]
        return main_files

    def run_all_checks(self) -> Dict:
        """Run all automated checks"""
        print("Running automated checks...")

        # Run individual checks
        self._check_formatting_consistency()
        self._check_content_structure()
        self._check_citations()
        self._check_word_counts()
        self._check_readability_indicators()
        self._check_code_examples()

        return self.results

    def _check_formatting_consistency(self):
        """Check for formatting consistency across files"""
        print("Checking formatting consistency...")

        required_sections = ['## Learning Objectives', '## Key Concepts', '## Introduction']

        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)

            if missing_sections:
                self.results['formatting_issues'].append({
                    'file': file_path,
                    'issue': f'Missing required sections: {missing_sections}',
                    'type': 'structure'
                })

            # Check for common formatting issues
            lines = content.split('\n')
            for i, line in enumerate(lines):
                # Check for inconsistent heading levels
                if line.strip().startswith('#') and not line.strip().startswith('# '):
                    self.results['formatting_issues'].append({
                        'file': file_path,
                        'line': i + 1,
                        'issue': f'Inconsistent heading format: {line.strip()}',
                        'type': 'formatting'
                    })

                # Check for missing spaces after hash in headings
                if re.match(r'^#+[^ ].*', line.strip()):
                    self.results['formatting_issues'].append({
                        'file': file_path,
                        'line': i + 1,
                        'issue': f'Missing space after heading hash: {line.strip()}',
                        'type': 'formatting'
                    })

    def _check_content_structure(self):
        """Check content structure and organization"""
        print("Checking content structure...")

        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if file has proper chapter template structure
            has_learning_objectives = '## Learning Objectives' in content
            has_key_concepts = '## Key Concepts' in content
            has_introduction = '## Introduction' in content

            if not (has_learning_objectives and has_key_concepts and has_introduction):
                self.results['content_issues'].append({
                    'file': file_path,
                    'issue': 'Missing standard chapter sections',
                    'type': 'structure'
                })

            # Check for checklist format in learning objectives
            learning_obj_start = content.find('## Learning Objectives')
            if learning_obj_start != -1:
                # Find the end of the learning objectives section
                next_header = content.find('\n## ', learning_obj_start + 1)
                if next_header == -1:
                    section_content = content[learning_obj_start:]
                else:
                    section_content = content[learning_obj_start:next_header]

                # Check if objectives are in checklist format
                checklist_items = re.findall(r'- \[([ x])\] (.+)', section_content)
                if not checklist_items:
                    self.results['content_issues'].append({
                        'file': file_path,
                        'issue': 'Learning objectives not in checklist format',
                        'type': 'formatting'
                    })

    def _check_citations(self):
        """Check citation format and consistency"""
        print("Checking citations...")

        apa_pattern = r'\([A-Z][a-z]+, \d{4}\)'  # Basic APA format check
        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            citations = re.findall(apa_pattern, content)

            # Check if citations are followed by proper references
            if citations and '## References' not in content and '## Bibliography' not in content:
                self.results['content_issues'].append({
                    'file': file_path,
                    'issue': f'Found {len(citations)} citations but no References/Bibliography section',
                    'type': 'citation'
                })

    def _check_word_counts(self):
        """Check word counts for each file"""
        print("Checking word counts...")

        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count words (rough estimate, excluding markdown syntax)
            text_content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)  # Remove code blocks
            text_content = re.sub(r'`[^`]*`', '', text_content)  # Remove inline code
            text_content = re.sub(r'^#+.*$', '', text_content, flags=re.MULTILINE)  # Remove headings
            text_content = re.sub(r'^[-*]\s+.*$', '', text_content, flags=re.MULTILINE)  # Remove list items

            words = re.findall(r'\b\w+\b', text_content)
            word_count = len(words)

            self.results['word_counts'][file_path] = word_count

            # Check if word count is reasonable for a chapter
            if word_count < 1000 and 'chapter' in os.path.basename(file_path).lower():
                self.results['content_issues'].append({
                    'file': file_path,
                    'issue': f'Chapter has only {word_count} words (possibly too short)',
                    'type': 'content_length'
                })

    def _check_readability_indicators(self):
        """Check for readability indicators"""
        print("Checking readability indicators...")

        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count sentences (very rough estimate)
            sentences = re.split(r'[.!?]+', content)
            avg_sentence_length = 0
            if sentences:
                sentence_word_counts = []
                for sentence in sentences:
                    words = re.findall(r'\b\w+\b', sentence)
                    if words:  # Only count non-empty sentences
                        sentence_word_counts.append(len(words))

                if sentence_word_counts:
                    avg_sentence_length = sum(sentence_word_counts) / len(sentence_word_counts)

            # Count complex words (words with 3+ syllables - very rough approximation)
            words = re.findall(r'\b\w+\b', content)
            complex_words = 0
            for word in words:
                # Very rough syllable counting
                vowels = 'aeiouyAEIOUY'
                syllable_count = 0
                prev_was_vowel = False

                for char in word:
                    is_vowel = char in vowels
                    if is_vowel and not prev_was_vowel:
                        syllable_count += 1
                    prev_was_vowel = is_vowel

                if syllable_count >= 3:
                    complex_words += 1

            complex_word_ratio = complex_words / len(words) if words else 0

            self.results['readability_metrics'][file_path] = {
                'avg_sentence_length': avg_sentence_length,
                'complex_word_ratio': complex_word_ratio
            }

    def _check_code_examples(self):
        """Check code examples for consistency"""
        print("Checking code examples...")

        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find code blocks
            code_blocks = re.findall(r'```(\w+)?\n(.*?)```', content, re.DOTALL)

            for lang, code in code_blocks:
                if not lang:
                    self.results['formatting_issues'].append({
                        'file': file_path,
                        'issue': 'Code block missing language identifier',
                        'type': 'formatting'
                    })
                elif lang.lower() not in ['python', 'yaml', 'json', 'bash', 'xml', 'cpp', 'c', 'java', 'javascript', 'html', 'css']:
                    # Common programming languages used in robotics/ROS context
                    pass  # Allow other languages if they're appropriate

    def generate_report(self) -> str:
        """Generate a report of the automated checks"""
        report = []
        report.append("AUTOMATED CHECKS REPORT")
        report.append("=" * 50)

        report.append(f"\nFiles analyzed: {len(self.md_files)}")

        if self.results['formatting_issues']:
            report.append(f"\nFormatting Issues Found: {len(self.results['formatting_issues'])}")
            for issue in self.results['formatting_issues']:
                report.append(f"  - {issue['file']}: {issue.get('issue', 'Unknown issue')}")

        if self.results['content_issues']:
            report.append(f"\nContent Issues Found: {len(self.results['content_issues'])}")
            for issue in self.results['content_issues']:
                report.append(f"  - {issue['file']}: {issue.get('issue', 'Unknown issue')}")

        # Word count summary
        total_words = sum(self.results['word_counts'].values())
        report.append(f"\nTotal word count: {total_words:,}")
        report.append(f"Average words per file: {total_words/len(self.results['word_counts']):.0f}")

        # Readability summary
        report.append(f"\nReadability Metrics:")
        for file_path, metrics in list(self.results['readability_metrics'].items())[:5]:  # Show first 5
            rel_path = os.path.relpath(file_path, self.base_path)
            report.append(f"  - {rel_path}: Avg sentence length: {metrics['avg_sentence_length']:.1f}, Complex word ratio: {metrics['complex_word_ratio']:.2f}")

        report.append(f"\nFiles processed: {len(self.md_files)}")
        for file_path in self.md_files[:10]:  # Show first 10 files
            rel_path = os.path.relpath(file_path, self.base_path)
            word_count = self.results['word_counts'].get(file_path, 0)
            report.append(f"  - {rel_path}: {word_count:,} words")

        if len(self.md_files) > 10:
            report.append(f"  ... and {len(self.md_files) - 10} more files")

        return "\n".join(report)

    def check_plagiarism_indicators(self):
        """Check for potential plagiarism indicators"""
        print("Checking for plagiarism indicators...")

        # This is a very basic check - in a real system, you'd want to use proper plagiarism detection tools
        # For now, we'll just check for suspiciously long verbatim text blocks

        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for long paragraphs that might be copied content
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                # Check for very long paragraphs without citations or original thought markers
                if len(para.strip()) > 500:  # Arbitrary threshold
                    # Check if paragraph contains citation markers
                    if not re.search(r'\([^)]*[0-9]{4}[^\)]*\)', para) and not re.search(r'\[[^\]]*et al[^\]]*\]', para):
                        self.results['potential_plagiarism'].append({
                            'file': file_path,
                            'issue': f'Long paragraph without citation markers (possible verbatim text): {para[:100]}...',
                            'type': 'plagiarism_indicator'
                        })


def main():
    parser = argparse.ArgumentParser(description='Automated checks for Physical AI & Humanoid Robotics book')
    parser.add_argument('--path', default='.', help='Path to the project root')
    parser.add_argument('--output', help='Output file for the report')

    args = parser.parse_args()

    checker = AutomatedChecker(args.path)

    # Run all checks
    results = checker.run_all_checks()
    checker.check_plagiarism_indicators()

    # Generate report
    report = checker.generate_report()

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report saved to {args.output}")
    else:
        print(report)

    # Summary
    total_issues = (len(results['formatting_issues']) +
                   len(results['content_issues']) +
                   len(results['consistency_issues']) +
                   len(results['potential_plagiarism']))

    print(f"\nSUMMARY: Found {total_issues} issues across {len(checker.md_files)} files")

    if total_issues == 0:
        print("✓ All automated checks passed!")
    else:
        print("? Some issues were found that may need manual review")


if __name__ == "__main__":
    main()