import os
from pathlib import Path
from typing import List
from git import Repo, exc

def get_repo_files(root_path: Path) -> List[Path]:
    """
    Returns a list of files in the repository, respecting gitignore.
    Falls back to simple walk if not a git repo.
    """
    try:
        repo = Repo(root_path, search_parent_directories=True)
        # ls-files gives us tracked files
        # We might also want untracked files that are not ignored.
        # repo.untracked_files gives untracked files
        
        git_root = Path(repo.working_dir)
        files = [git_root / f for f in repo.git.ls_files().split('\n') if f]
        
        # Add untracked files (newly created)
        for f in repo.untracked_files:
             files.append(git_root / f)
             
        # Filter to ensure they are within strict root_path if root_path is a subdir of git root
        # (Though usually we run from root)
        return sorted([f for f in files if root_path in f.parents or f == root_path])
        
    except (exc.InvalidGitRepositoryError, exc.NoSuchPathError):
        # Fallback: naive walk (skipping hidden)
        file_list = []
        for root, dirs, files in os.walk(root_path):
            # approximate gitignore by skipping . dirs
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if not file.startswith('.'):
                    file_list.append(Path(root) / file)
        return sorted(file_list)

def generate_context_map(root_path: Path) -> str:
    """
    Generates a markdown tree or list of the project structure.
    """
    files = get_repo_files(root_path)
    
    # Simple list format for now, optimized for token usage
    # We can group by directory
    
    output = ["# Context Map", ""]
    output.append(f"Total Files: {len(files)}")
    output.append("## File List")
    
    # Group by stored relative path
    rel_files = [f.relative_to(root_path) for f in files]
    
    for f in rel_files:
        output.append(f"- {f}")
        
    return "\n".join(output)

def is_repo_dirty(root_path: Path) -> bool:
    try:
        repo = Repo(root_path, search_parent_directories=True)
        return repo.is_dirty() or len(repo.untracked_files) > 0
    except (exc.InvalidGitRepositoryError, exc.NoSuchPathError):
        return False
