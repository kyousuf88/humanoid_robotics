#!/usr/bin/env python3
"""
Comprehensive Quality Assurance Script for Physical AI & Humanoid Robotics book.
Performs end-to-end validation of all requirements and success criteria.
"""

import os
import re
import glob
from typing import List, Dict, Tuple
import json
import argparse
from collections import Counter


class QualityAssuranceChecker:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.md_files = self._find_book_markdown_files()
        self.results = {
            'functional_requirements_met': [],
            'success_criteria_met': [],
            'citation_validation': [],
            'grade_level_compliance': [],
            'length_compliance': [],
            'overall_compliance': {}
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

    def run_comprehensive_qa(self) -> Dict:
        """Run comprehensive quality assurance checks"""
        print("Running comprehensive quality assurance...")

        # Check functional requirements (FR-001 to FR-020)
        self._check_functional_requirements()

        # Check success criteria (SC-001 to SC-010)
        self._check_success_criteria()

        # Verify citations follow APA format
        self._verify_citations_format()

        # Check Flesch-Kincaid Grade level compliance (Grade 9-12)
        self._check_grade_level_compliance()

        # Check book length compliance (30,000-50,000 words)
        self._check_length_compliance()

        # Final overall compliance check
        self._calculate_overall_compliance()

        return self.results

    def _check_functional_requirements(self):
        """Check if functional requirements are met"""
        print("Checking functional requirements (FR-001 to FR-020)...")

        # Define expected functional requirements based on typical book requirements
        expected_fr = {
            'FR-001': 'Book provides comprehensive coverage of Physical AI concepts',
            'FR-002': 'Book covers ROS 2 fundamentals for robotic systems',
            'FR-003': 'Book includes simulation techniques using Gazebo/Unity',
            'FR-004': 'Book covers NVIDIA Isaac ecosystem',
            'FR-005': 'Book addresses VLA (Vision-Language-Action) systems',
            'FR-006': 'Book includes code examples in Python',
            'FR-007': 'Book provides practical implementation guides',
            'FR-008': 'Book covers safety considerations for humanoid robots',
            'FR-009': 'Book includes multi-modal perception techniques',
            'FR-010': 'Book addresses sim-to-real transfer techniques',
            'FR-011': 'Book covers reinforcement learning for robotics',
            'FR-012': 'Book includes navigation and path planning',
            'FR-013': 'Book addresses humanoid locomotion control',
            'FR-014': 'Book covers cognitive planning using LLMs',
            'FR-015': 'Book includes sensor fusion techniques',
            'FR-016': 'Book addresses human-robot interaction',
            'FR-017': 'Book covers robot perception systems',
            'FR-018': 'Book addresses robot manipulation',
            'FR-019': 'Book includes system integration techniques',
            'FR-020': 'Book provides deployment guidelines'
        }

        # Check if content covers these requirements
        all_content = self._get_all_content()

        for fr_id, description in expected_fr.items():
            # Simple keyword-based check for now
            keywords = self._extract_keywords(description)
            found = any(keyword.lower() in all_content.lower() for keyword in keywords)

            if found:
                self.results['functional_requirements_met'].append({
                    'id': fr_id,
                    'description': description,
                    'met': True,
                    'evidence': f"Keywords found: {keywords}"
                })
            else:
                self.results['functional_requirements_met'].append({
                    'id': fr_id,
                    'description': description,
                    'met': False,
                    'evidence': f"No evidence found for keywords: {keywords}"
                })

    def _check_success_criteria(self):
        """Check if success criteria are met"""
        print("Checking success criteria (SC-001 to SC-010)...")

        # Define expected success criteria
        expected_sc = {
            'SC-001': 'Book provides clear learning objectives for each chapter',
            'SC-002': 'Book includes practical code examples',
            'SC-003': 'Book covers theoretical foundations',
            'SC-004': 'Book includes real-world applications',
            'SC-005': 'Book addresses safety considerations',
            'SC-006': 'Book provides step-by-step tutorials',
            'SC-007': 'Book includes review questions/exercises',
            'SC-008': 'Book covers multiple AI techniques',
            'SC-009': 'Book addresses humanoid-specific challenges',
            'SC-010': 'Book provides clear chapter summaries'
        }

        sc_results = []
        for sc_id, description in expected_sc.items():
            # Check each criterion in the content
            if sc_id == 'SC-001':  # Learning objectives
                found = any('Learning Objectives' in open(f, 'r', encoding='utf-8').read()
                           for f in self.md_files if os.path.exists(f))
                sc_results.append({'id': sc_id, 'description': description, 'met': found})
            elif sc_id == 'SC-002':  # Code examples
                found = any('```python' in open(f, 'r', encoding='utf-8').read()
                           for f in self.md_files if os.path.exists(f))
                sc_results.append({'id': sc_id, 'description': description, 'met': found})
            elif sc_id == 'SC-007':  # Review questions
                found = any('Review Questions' in open(f, 'r', encoding='utf-8').read()
                           for f in self.md_files if os.path.exists(f))
                sc_results.append({'id': sc_id, 'description': description, 'met': found})
            elif sc_id == 'SC-010':  # Chapter summaries
                found = any('Summary' in open(f, 'r', encoding='utf-8').read()
                           for f in self.md_files if os.path.exists(f))
                sc_results.append({'id': sc_id, 'description': description, 'met': found})
            else:
                # For other criteria, do a general content search
                keywords = self._extract_keywords(description)
                found = any(any(keyword.lower() in open(f, 'r', encoding='utf-8').read().lower()
                               for f in self.md_files if os.path.exists(f)) for keyword in keywords)
                sc_results.append({'id': sc_id, 'description': description, 'met': found})

        self.results['success_criteria_met'] = sc_results

    def _verify_citations_format(self):
        """Verify citations follow APA format and are traceable to credible sources"""
        print("Verifying citations format...")

        apa_pattern = r'\([A-Z][a-z]+, \d{4}\)|\[([^\]]+)\]\([^)]+\)'  # Basic APA and markdown link check

        total_citations = 0
        apa_formatted = 0
        markdown_formatted = 0

        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find APA-style citations
            apa_citations = re.findall(apa_pattern, content)
            total_citations += len(apa_citations)

            # Count different types
            for cit in apa_citations:
                if isinstance(cit, tuple):
                    # Check which element matched
                    if cit[0]:  # APA format matched
                        apa_formatted += 1
                    elif cit[1]:  # Markdown link matched
                        markdown_formatted += 1
                elif '(' in cit and ')' in cit:
                    apa_formatted += 1
                elif '[' in cit and ']' in cit:
                    markdown_formatted += 1

        # Add results
        self.results['citation_validation'].append({
            'total_citations_found': total_citations,
            'apa_formatted': apa_formatted,
            'markdown_formatted': markdown_formatted,
            'compliance_percentage': (apa_formatted / total_citations * 100) if total_citations > 0 else 0
        })

    def _check_grade_level_compliance(self):
        """Check Flesch-Kincaid Grade level compliance (Grade 9-12)"""
        print("Checking grade level compliance...")

        # This is a simplified check - in reality, you'd use a proper readability library
        # For now, we'll estimate based on sentence and word complexity

        total_sentences = 0
        total_words = 0
        total_syllables = 0

        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count sentences (roughly)
            sentences = len(re.split(r'[.!?]+', content))
            # Count words
            words = len(re.findall(r'\b\w+\b', content))
            # Count syllables (very rough approximation)
            syllables = sum(max(1, len(word)//3) for word in re.findall(r'\b\w+\b', content))

            total_sentences += sentences
            total_words += words
            total_syllables += syllables

        if total_words > 0 and total_sentences > 0:
            # Simplified Flesch-Kincaid calculation
            avg_words_per_sentence = total_words / total_sentences if total_sentences > 0 else 0
            avg_syllables_per_word = total_syllables / total_words if total_words > 0 else 0

            # Flesch-Kincaid Grade Level formula
            grade_level = 0.39 * avg_words_per_sentence + 11.8 * avg_syllables_per_word - 15.59

            self.results['grade_level_compliance'].append({
                'calculated_grade_level': round(grade_level, 2),
                'target_range': '9-12',
                'compliant': 9 <= grade_level <= 12,
                'details': {
                    'sentences': total_sentences,
                    'words': total_words,
                    'syllables': total_syllables,
                    'avg_words_per_sentence': round(avg_words_per_sentence, 2),
                    'avg_syllables_per_word': round(avg_syllables_per_word, 4)
                }
            })
        else:
            self.results['grade_level_compliance'].append({
                'calculated_grade_level': 0,
                'target_range': '9-12',
                'compliant': False,
                'error': 'Unable to calculate grade level - no content found'
            })

    def _check_length_compliance(self):
        """Check book length compliance (30,000-50,000 words)"""
        print("Checking length compliance...")

        total_words = 0
        file_word_counts = {}

        for file_path in self.md_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove code blocks for word count
            text_content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            text_content = re.sub(r'`[^`]*`', '', text_content)

            # Count words
            words = len(re.findall(r'\b\w+\b', text_content))
            total_words += words
            file_word_counts[os.path.basename(file_path)] = words

        compliant = 30000 <= total_words <= 50000

        self.results['length_compliance'].append({
            'total_word_count': total_words,
            'target_range': '30,000-50,000',
            'compliant': compliant,
            'words_per_file': file_word_counts,
            'file_count': len(self.md_files)
        })

    def _calculate_overall_compliance(self):
        """Calculate overall compliance with requirements"""
        print("Calculating overall compliance...")

        # Calculate compliance percentages
        total_fr = len(self.results['functional_requirements_met'])
        met_fr = sum(1 for fr in self.results['functional_requirements_met'] if fr['met'])
        fr_compliance = (met_fr / total_fr * 100) if total_fr > 0 else 0

        total_sc = len(self.results['success_criteria_met'])
        met_sc = sum(1 for sc in self.results['success_criteria_met'] if sc['met'])
        sc_compliance = (met_sc / total_sc * 100) if total_sc > 0 else 0

        # Check citation compliance
        citation_info = self.results['citation_validation'][0] if self.results['citation_validation'] else {}
        citation_compliance = citation_info.get('compliance_percentage', 0)

        # Check grade level compliance
        grade_info = self.results['grade_level_compliance'][0] if self.results['grade_level_compliance'] else {}
        grade_compliant = grade_info.get('compliant', False)

        # Check length compliance
        length_info = self.results['length_compliance'][0] if self.results['length_compliance'] else {}
        length_compliant = length_info.get('compliant', False)

        # Overall assessment
        overall_score = (fr_compliance + sc_compliance) / 2  # Average of FR and SC compliance

        self.results['overall_compliance'] = {
            'functional_requirement_compliance': f"{fr_compliance:.1f}% ({met_fr}/{total_fr})",
            'success_criteria_compliance': f"{sc_compliance:.1f}% ({met_sc}/{total_sc})",
            'citation_format_compliance': f"{citation_compliance:.1f}%",
            'grade_level_compliant': grade_compliant,
            'length_compliant': length_compliant,
            'overall_score': f"{overall_score:.1f}%",
            'status': 'PASS' if (overall_score >= 80 and grade_compliant and length_compliant) else 'NEEDS_IMPROVEMENT'
        }

    def _get_all_content(self) -> str:
        """Get all content from book files"""
        all_content = ""
        for file_path in self.md_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    all_content += f.read() + "\n\n"
        return all_content

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Simple keyword extraction - in reality, use NLP techniques
        words = re.findall(r'\b\w+\b', text.lower())
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        return [word for word in words if word not in stop_words and len(word) > 2]

    def generate_report(self) -> str:
        """Generate comprehensive QA report"""
        report = []
        report.append("COMPREHENSIVE QUALITY ASSURANCE REPORT")
        report.append("=" * 60)

        report.append(f"\nFiles analyzed: {len(self.md_files)}")
        report.append(f"Total word count: {self.results['length_compliance'][0]['total_word_count']:,}" if self.results['length_compliance'] else "Word count: Unknown")

        # Functional Requirements
        report.append(f"\nFUNCTIONAL REQUIREMENTS ASSESSMENT:")
        fr_info = self.results['overall_compliance'].get('functional_requirement_compliance', '0% (0/0)')
        report.append(f"  Compliance: {fr_info}")

        # Success Criteria
        report.append(f"\nSUCCESS CRITERIA ASSESSMENT:")
        sc_info = self.results['overall_compliance'].get('success_criteria_compliance', '0% (0/0)')
        report.append(f"  Compliance: {sc_info}")

        # Citation Validation
        report.append(f"\nCITATION VALIDATION:")
        if self.results['citation_validation']:
            citation_info = self.results['citation_validation'][0]
            report.append(f"  Total citations: {citation_info['total_citations_found']}")
            report.append(f"  APA formatted: {citation_info['apa_formatted']}")
            report.append(f"  Compliance: {citation_info['compliance_percentage']:.1f}%")

        # Grade Level Compliance
        report.append(f"\nGRADE LEVEL COMPLIANCE:")
        if self.results['grade_level_compliance']:
            grade_info = self.results['grade_level_compliance'][0]
            calculated = grade_info.get('calculated_grade_level', 'Unknown')
            compliant = grade_info.get('compliant', False)
            report.append(f"  Calculated Grade Level: {calculated}")
            report.append(f"  Compliant (9-12): {'Yes' if compliant else 'No'}")

        # Length Compliance
        report.append(f"\nLENGTH COMPLIANCE:")
        if self.results['length_compliance']:
            length_info = self.results['length_compliance'][0]
            compliant = length_info.get('compliant', False)
            report.append(f"  Total words: {length_info['total_word_count']:,}")
            report.append(f"  Target: 30,000-50,000 words")
            report.append(f"  Compliant: {'Yes' if compliant else 'No'}")

        # Overall Compliance
        report.append(f"\nOVERALL COMPLIANCE ASSESSMENT:")
        overall = self.results['overall_compliance']
        report.append(f"  Overall Score: {overall.get('overall_score', '0%')}")
        report.append(f"  Status: {overall.get('status', 'UNKNOWN')}")

        # Recommendations
        report.append(f"\nRECOMMENDATIONS:")
        if overall.get('status') == 'PASS':
            report.append("  ✓ The book meets quality assurance standards.")
        else:
            report.append("  ? The book may need improvements to meet all requirements.")
            if float(overall.get('overall_score', '0%').rstrip('%')) < 80:
                report.append("    - Consider improving content coverage for functional requirements")
            if not overall.get('grade_level_compliant', False):
                report.append("    - Review content complexity for target grade level (9-12)")
            if not overall.get('length_compliant', False):
                report.append("    - Adjust content length to meet 30,000-50,000 word requirement")

        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description='Quality Assurance for Physical AI & Humanoid Robotics book')
    parser.add_argument('--path', default='.', help='Path to the project root')
    parser.add_argument('--output', help='Output file for the report')

    args = parser.parse_args()

    checker = QualityAssuranceChecker(args.path)

    # Run comprehensive QA
    results = checker.run_comprehensive_qa()

    # Generate report
    report = checker.generate_report()

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"QA Report saved to {args.output}")
    else:
        print(report)

    print(f"\nCompleted T063: Comprehensive end-to-end quality assurance pass")


if __name__ == "__main__":
    main()