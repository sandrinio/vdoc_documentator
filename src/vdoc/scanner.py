import os
import json
import toml
from pathlib import Path
from typing import List, Dict, Set
from git import Repo, exc
from collections import Counter

def get_repo_files(root_path: Path) -> List[Path]:
    """
    Returns a list of files in the repository, respecting gitignore.
    Falls back to simple walk if not a git repo.
    """
    try:
        repo = Repo(root_path, search_parent_directories=True)
        git_root = Path(repo.working_dir)
        files = [git_root / f for f in repo.git.ls_files().split('\n') if f]
        
        # Add untracked files (newly created)
        for f in repo.untracked_files:
             files.append(git_root / f)
             
        # Filter to ensure they are within strict root_path
        return sorted([f for f in files if root_path in f.parents or f == root_path])
        
    except (exc.InvalidGitRepositoryError, exc.NoSuchPathError):
        # Fallback: naive walk (skipping hidden)
        file_list = []
        for root, dirs, files in os.walk(root_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if not file.startswith('.'):
                    file_list.append(Path(root) / file)
        return sorted(file_list)

def analyze_project_root(root_path: Path, files: List[Path]) -> Dict:
    """
    Analyzes the project to detect languages and frameworks.
    """
    stats = {
        "languages": Counter(),
        "frameworks": set(),
        "config_files": []
    }
    
    # 1. Language Detection by Extension
    ext_map = {
        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.tsx': 'TypeScript (React)',
        '.jsx': 'JavaScript (React)', '.go': 'Go', '.rs': 'Rust', '.java': 'Java',
        '.cpp': 'C++', '.c': 'C', '.html': 'HTML', '.css': 'CSS', '.md': 'Markdown'
    }
    
    for f in files:
        if f.suffix in ext_map:
            stats["languages"][ext_map[f.suffix]] += 1
            
    # 2. Framework Detection (Configs)
    # Python (pyproject.toml)
    pyproject = root_path / "pyproject.toml"
    if pyproject.exists():
        stats["config_files"].append("pyproject.toml")
        try:
            data = toml.load(pyproject)
            deps = str(data).lower() # Naive search
            
            frameworks = {
                "django": "Django", "fastapi": "FastAPI", "flask": "Flask",
                "tornado": "Tornado", "pyramid": "Pyramid", "bottle": "Bottle",
                "falcon": "Falcon", "sanic": "Sanic", "starlette": "Starlette",
                "litestar": "Litestar"
            }
            for k, v in frameworks.items():
                if k in deps: stats["frameworks"].add(v)
        except Exception:
            pass

    # Node (package.json)
    package_json = root_path / "package.json"
    if package_json.exists():
        stats["config_files"].append("package.json")
        try:
            with open(package_json) as f:
                data = json.load(f)
                all_deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                keys = " ".join(all_deps.keys()).lower()
                
                frameworks = {
                    "react": "React", "vue": "Vue", "angular": "Angular",
                    "next": "Next.js", "nuxt": "Nuxt", "svelte": "Svelte",
                    "express": "Express", "nest": "NestJS", "koa": "Koa",
                    "fastify": "Fastify", "hapi": "Hapi", "meteor": "Meteor",
                    "sails": "Sails", "adonis": "AdonisJS"
                }
                for k, v in frameworks.items():
                    if k in keys: stats["frameworks"].add(v)
                
                # Special check for Angular core
                if "@angular/core" in keys: stats["frameworks"].add("Angular")

        except Exception:
            pass

    # Go (go.mod)
    go_mod = root_path / "go.mod"
    if go_mod.exists():
        stats["config_files"].append("go.mod")
        try:
            content = go_mod.read_text().lower()
            frameworks = {
                "github.com/gin-gonic/gin": "Gin",
                "github.com/gofiber/fiber": "Fiber",
                "github.com/labstack/echo": "Echo",
                "github.com/go-chi/chi": "Chi",
                "github.com/beego/beego": "Beego"
            }
            for k, v in frameworks.items():
                if k in content: stats["frameworks"].add(v)
        except Exception:
            pass

    # Java (pom.xml - Maven)
    pom_xml = root_path / "pom.xml"
    if pom_xml.exists():
        stats["config_files"].append("pom.xml")
        try:
            content = pom_xml.read_text().lower()
            if "org.springframework.boot" in content: stats["frameworks"].add("Spring Boot")
            if "io.micronaut" in content: stats["frameworks"].add("Micronaut")
            if "io.quarkus" in content: stats["frameworks"].add("Quarkus")
            if "jakarta" in content: stats["frameworks"].add("Jakarta EE")
        except Exception:
            pass

    # Ruby (Gemfile)
    gemfile = root_path / "Gemfile"
    if gemfile.exists():
        stats["config_files"].append("Gemfile")
        try:
            content = gemfile.read_text().lower()
            if "rails" in content: stats["frameworks"].add("Ruby on Rails")
            if "sinatra" in content: stats["frameworks"].add("Sinatra")
            if "hanami" in content: stats["frameworks"].add("Hanami")
        except Exception:
            pass
            
    # PHP (composer.json)
    composer_json = root_path / "composer.json"
    if composer_json.exists():
        stats["config_files"].append("composer.json")
        try:
            content = composer_json.read_text().lower()
            if "laravel/framework" in content: stats["frameworks"].add("Laravel")
            if "symfony/framework-bundle" in content: stats["frameworks"].add("Symfony")
            if "codeigniter/framework" in content: stats["frameworks"].add("CodeIgniter")
            if "cakephp/cakephp" in content: stats["frameworks"].add("CakePHP")
        except Exception:
            pass
            
    return stats

def generate_context_map(root_path: Path) -> str:
    """
    Generates a structured, smart markdown map of the project.
    """
    files = get_repo_files(root_path)
    stats = analyze_project_root(root_path, files)
    
    # Calculate top languages
    total_code_files = sum(stats["languages"].values())
    top_langs = [f"{lang} ({count})" for lang, count in stats["languages"].most_common(3)]
    
    output = ["# Context Map", ""]
    
    # Section 1: Overview
    output.append("## Project Overview")
    if top_langs:
        output.append(f"- **Languages:** {', '.join(top_langs)}")
    if stats["frameworks"]:
        output.append(f"- **Frameworks:** {', '.join(sorted(stats['frameworks']))}")
    if stats["config_files"]:
        output.append(f"- **Config Files:** {', '.join(stats['config_files'])}")
    output.append(f"- **Total Files:** {len(files)}")
    output.append("")

    # Section 2: Structure (Grouped)
    output.append("## Project Structure")
    
    # Group files by top-level directory
    structure = {}
    root_files = []
    
    for f in files:
        rel = f.relative_to(root_path)
        parts = rel.parts
        if len(parts) == 1:
            root_files.append(str(rel))
        else:
            top_dir = parts[0]
            if top_dir not in structure:
                structure[top_dir] = []
            structure[top_dir].append(str(Path(*parts[1:])))
            
    # Print Root Files first
    if root_files:
        output.append("### Root")
        for f in sorted(root_files):
            output.append(f"- {f}")
        output.append("")
            
    # Print Directories
    for d in sorted(structure.keys()):
        offset = len(structure[d])
        output.append(f"### {d}/ ({offset} files)")
        # If too many files, truncate? For now, list all.
        # Ideally we'd show a tree, but a list is token-efficient.
        # Let's show up to 20 files per dir, then truncate.
        items = sorted(structure[d])
        for item in items[:50]: # Increased cap slightly
            output.append(f"- {item}")
        if len(items) > 50:
            output.append(f"- ... ({len(items) - 50} more)")
        output.append("")

    return "\n".join(output)

def is_repo_dirty(root_path: Path) -> bool:
    try:
        repo = Repo(root_path, search_parent_directories=True)
        return repo.is_dirty() or len(repo.untracked_files) > 0
    except (exc.InvalidGitRepositoryError, exc.NoSuchPathError):
        return False
