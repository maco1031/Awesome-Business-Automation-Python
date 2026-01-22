"""
Skill Loader Utility
====================
Copies skills from a Master Skills Collection to the current project's local agent skills directory.

Usage:
    python utils/skill_loader.py --source <path_to_master> --list
    python utils/skill_loader.py --source <path_to_master> --install <SkillName>

Default Master Path: Can be set in execution or defaults to user's home directory pattern if configured.
"""

import os
import shutil
import argparse
import sys

# Default Local Skills Directory (Agentic Mode Standard)
LOCAL_SKILLS_DIR = os.path.join(".agent", "skills")

def list_skills(source_dir):
    """List available skills in the source directory."""
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    print(f"--- Available Skills in {source_dir} ---")
    found = False
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "SKILL.md")):
            print(f"- {item}")
            found = True
    
    if not found:
        print("(No valid skills found. A valid skill must have a SKILL.md file.)")
    print("------------------------------------------")

def install_skill(source_dir, skill_name, update=False):
    """Copy a skill from source to local skills directory."""
    source_path = os.path.join(source_dir, skill_name)
    target_path = os.path.join(LOCAL_SKILLS_DIR, skill_name)

    if not os.path.exists(source_path):
        print(f"Error: Skill '{skill_name}' not found in {source_dir}.")
        return

    if not os.path.exists(os.path.join(source_path, "SKILL.md")):
        print(f"Error: '{skill_name}' is not a valid skill (missing SKILL.md).")
        return

    if os.path.exists(target_path):
        if not update:
            print(f"Warning: Skill '{skill_name}' already exists locally.")
            confirm = input("Overwrite? (y/n): ").lower()
            if confirm != 'y':
                print("Aborted.")
                return
        print(f"Updating '{skill_name}'...")
        shutil.rmtree(target_path)
    else:
        print(f"Installing '{skill_name}'...")

    try:
        shutil.copytree(source_path, target_path)
        print(f"Success! Skill '{skill_name}' installed to '{target_path}'.")
    except Exception as e:
        print(f"Error installing skill: {e}")

def export_skill(source_dir, skill_name, update=False):
    """Copy a skill from local skills directory to the master source directory."""
    local_path = os.path.join(LOCAL_SKILLS_DIR, skill_name)
    target_path = os.path.join(source_dir, skill_name)

    if not os.path.exists(local_path):
        print(f"Error: Local skill '{skill_name}' not found in {LOCAL_SKILLS_DIR}.")
        return

    if not os.path.exists(os.path.join(local_path, "SKILL.md")):
        print(f"Error: '{skill_name}' is not a valid skill (missing SKILL.md).")
        return

    if os.path.exists(target_path):
        if not update:
            print(f"Warning: Skill '{skill_name}' already exists in master collection: {source_dir}")
            confirm = input("Overwrite in master? (y/n): ").lower()
            if confirm != 'y':
                print("Aborted.")
                return
        print(f"Updating '{skill_name}' in master...")
        shutil.rmtree(target_path)
    else:
        print(f"Exporting '{skill_name}' to master...")

    try:
        shutil.copytree(local_path, target_path)
        print(f"Success! Skill '{skill_name}' exported to '{target_path}'.")
    except Exception as e:
        print(f"Error exporting skill: {e}")

def main():
    parser = argparse.ArgumentParser(description="Skill Loader for Agentic Workflow")
    parser.add_argument("--source", required=True, help="Path to the Master Skills Collection directory")
    parser.add_argument("--list", action="store_true", help="List available skills")
    parser.add_argument("--install", help="Name of the skill to install")
    parser.add_argument("--export", help="Name of the skill to export from local to master")
    parser.add_argument("--update", action="store_true", help="Force update if skill exists")

    args = parser.parse_args()

    if args.list:
        list_skills(args.source)
    elif args.install:
        install_skill(args.source, args.install, args.update)
    elif args.export:
        export_skill(args.source, args.export, args.update)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
