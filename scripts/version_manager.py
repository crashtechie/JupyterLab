#!/usr/bin/env python3
"""
Semantic Version Manager for JupyterLab Project

This script manages semantic versioning following the Semantic Versioning 2.0.0 specification.
It updates version numbers across multiple files and generates changelog entries.

Usage:
    python scripts/version_manager.py --bump major|minor|patch [--dry-run]
    python scripts/version_manager.py --set 1.2.3
    python scripts/version_manager.py --current

Examples:
    python scripts/version_manager.py --bump patch
    python scripts/version_manager.py --bump minor --dry-run
    python scripts/version_manager.py --set 2.0.0
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional


class VersionManager:
    """Manages semantic versioning for the project."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.version_file = project_root / "version.txt"
        self.readme_file = project_root / "README.md"
        self.changelog_file = project_root / "CHANGELOG.md"
        
    def get_current_version(self) -> str:
        """Read the current version from version.txt"""
        if not self.version_file.exists():
            return "0.1.0"
        return self.version_file.read_text().strip()
    
    def parse_version(self, version: str) -> Tuple[int, int, int]:
        """Parse version string into major, minor, patch tuple."""
        match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version)
        if not match:
            raise ValueError(f"Invalid version format: {version}")
        major, minor, patch = match.groups()
        return (int(major), int(minor), int(patch))
    
    def bump_version(self, bump_type: str) -> str:
        """Bump version based on type (major, minor, patch)."""
        current = self.get_current_version()
        major, minor, patch = self.parse_version(current)
        
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "patch":
            patch += 1
        else:
            raise ValueError(f"Invalid bump type: {bump_type}. Use major, minor, or patch.")
        
        return f"{major}.{minor}.{patch}"
    
    def update_version_file(self, new_version: str, dry_run: bool = False) -> None:
        """Update version.txt with new version."""
        if dry_run:
            print(f"[DRY RUN] Would update {self.version_file} to {new_version}")
            return
        
        self.version_file.write_text(new_version)
        print(f"✅ Updated {self.version_file} to {new_version}")
    
    def update_readme(self, new_version: str, dry_run: bool = False) -> None:
        """Update version badge in README.md"""
        if not self.readme_file.exists():
            print(f"⚠️  {self.readme_file} not found, skipping")
            return
        
        content = self.readme_file.read_text(encoding='utf-8')
        
        # Update version badge
        pattern = r'(!\[Version\]\(https://img\.shields\.io/badge/Version-v)[\d\.]+(-blue\.svg\))'
        replacement = rf'\g<1>{new_version}\g<2>'
        new_content = re.sub(pattern, replacement, content)
        
        if content == new_content:
            print(f"⚠️  No version badge found in {self.readme_file}")
            return
        
        if dry_run:
            print(f"[DRY RUN] Would update version badge in {self.readme_file} to v{new_version}")
            return
        
        self.readme_file.write_text(new_content, encoding='utf-8')
        print(f"✅ Updated version badge in {self.readme_file} to v{new_version}")
    
    def add_changelog_entry(self, new_version: str, dry_run: bool = False) -> None:
        """Add new version entry to CHANGELOG.md"""
        if not self.changelog_file.exists():
            print(f"⚠️  {self.changelog_file} not found, skipping")
            return
        
        content = self.changelog_file.read_text(encoding='utf-8')
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Find the position after the header
        header_pattern = r'(# Changelog.*?## \[)'
        
        new_entry = f"""## [v{new_version}] - {today}

### Added
- 

### Changed
- 

### Fixed
- 

### Security
- 

## ["""
        
        new_content = re.sub(header_pattern, rf'\g<1>{new_version}] - {today}\n\n### Added\n- \n\n### Changed\n- \n\n### Fixed\n- \n\n### Security\n- \n\n## [', content, count=1)
        
        if content == new_content:
            # Try alternate pattern if standard doesn't work
            lines = content.split('\n')
            insert_pos = None
            for i, line in enumerate(lines):
                if line.startswith('## [v'):
                    insert_pos = i
                    break
            
            if insert_pos is not None:
                entry_lines = [
                    f"## [v{new_version}] - {today}",
                    "",
                    "### Added",
                    "- ",
                    "",
                    "### Changed", 
                    "- ",
                    "",
                    "### Fixed",
                    "- ",
                    "",
                    "### Security",
                    "- ",
                    ""
                ]
                lines = lines[:insert_pos] + entry_lines + lines[insert_pos:]
                new_content = '\n'.join(lines)
        
        if dry_run:
            print(f"[DRY RUN] Would add new version entry to {self.changelog_file}")
            return
        
        self.changelog_file.write_text(new_content, encoding='utf-8')
        print(f"✅ Added v{new_version} entry to {self.changelog_file}")
        print(f"📝 Please edit {self.changelog_file} to add release notes")
    
    def update_all(self, new_version: str, dry_run: bool = False) -> None:
        """Update all files with new version."""
        current = self.get_current_version()
        
        print(f"\n{'=' * 60}")
        print(f"Version Update: v{current} → v{new_version}")
        print(f"{'=' * 60}\n")
        
        self.update_version_file(new_version, dry_run)
        self.update_readme(new_version, dry_run)
        self.add_changelog_entry(new_version, dry_run)
        
        if not dry_run:
            print(f"\n{'=' * 60}")
            print(f"✅ Version successfully updated to v{new_version}")
            print(f"{'=' * 60}\n")
            print("Next steps:")
            print(f"1. Edit {self.changelog_file} to add release notes")
            print("2. Review changes: git diff")
            print("3. Commit: git add . && git commit -m \"chore: bump version to v{new_version}\"")
            print("4. Tag: git tag -a v{new_version} -m \"Release v{new_version}\"")
            print("5. Push: git push origin develop && git push origin v{new_version}")


def main():
    parser = argparse.ArgumentParser(
        description="Manage semantic versioning for JupyterLab project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/version_manager.py --current
  python scripts/version_manager.py --bump patch
  python scripts/version_manager.py --bump minor --dry-run
  python scripts/version_manager.py --set 2.0.0

Semantic Versioning Guide:
  major: Breaking changes (1.0.0 → 2.0.0)
  minor: New features, backwards compatible (1.0.0 → 1.1.0)
  patch: Bug fixes, backwards compatible (1.0.0 → 1.0.1)
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--bump',
        choices=['major', 'minor', 'patch'],
        help='Bump version (major, minor, or patch)'
    )
    group.add_argument(
        '--set',
        metavar='VERSION',
        help='Set specific version (e.g., 1.2.3)'
    )
    group.add_argument(
        '--current',
        action='store_true',
        help='Show current version'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without making changes'
    )
    
    args = parser.parse_args()
    
    # Determine project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    manager = VersionManager(project_root)
    
    try:
        if args.current:
            version = manager.get_current_version()
            print(f"Current version: v{version}")
            sys.exit(0)
        
        if args.bump:
            new_version = manager.bump_version(args.bump)
        elif args.set:
            # Validate version format
            manager.parse_version(args.set)
            new_version = args.set
        else:
            parser.error("Must specify --bump, --set, or --current")
        
        manager.update_all(new_version, args.dry_run)
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
