from pathlib import Path
import os
import shutil
import vdoc.scanner as scanner

def test_smart_scanner():
    test_dir = Path("temp_smart_scanner_test")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()
    
    # 1. Create a mock Python project
    (test_dir / "src").mkdir()
    (test_dir / "src" / "main.py").touch()
    
    # Mock pyproject.toml with FastAPI
    with open(test_dir / "pyproject.toml", "w") as f:
        f.write("[tool.poetry.dependencies]\npython = '^3.9'\nfastapi = '^0.68.0'\n")
        
    # 2. Create a mock Node project
    (test_dir / "frontend").mkdir()
    (test_dir / "frontend" / "App.tsx").touch()
    
    # Mock package.json with React, Next.js, and Express
    with open(test_dir / "package.json", "w") as f:
        f.write('{"dependencies": {"react": "^17.0.2", "next": "^11.0.0", "express": "^4.17.1"}}')

    # 3. Create a mock Go project
    with open(test_dir / "go.mod", "w") as f:
        f.write("module example.com/hello\n\ngo 1.16\n\nrequire github.com/gin-gonic/gin v1.7.4")

    # 4. Create a mock Java project
    with open(test_dir / "pom.xml", "w") as f:
        f.write("<project><dependencies><dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency></dependencies></project>")

    print("Running Smart Scanner on temporary directory...")
    
    files = [
        test_dir / "src" / "main.py",
        test_dir / "pyproject.toml",
        test_dir / "frontend" / "App.tsx",
        test_dir / "package.json",
        test_dir / "go.mod",
        test_dir / "pom.xml"
    ]
    
    stats = scanner.analyze_project_root(test_dir, files)
    
    print("\n--- Detection Results ---")
    print(f"Languages: {stats['languages']}")
    print(f"Frameworks: {stats['frameworks']}")
    print(f"Config Files: {stats['config_files']}")
    
    assert "FastAPI" in stats['frameworks']
    assert "React" in stats['frameworks']
    assert "Next.js" in stats['frameworks']
    assert "Express" in stats['frameworks']
    assert "Gin" in stats['frameworks']
    assert "Spring Boot" in stats['frameworks']
    
    print("\n[SUCCESS] Smart Scanner correctly detected expanded stack!")
    
    # Clean up
    if test_dir.exists():
        shutil.rmtree(test_dir)

if __name__ == "__main__":
    test_smart_scanner()
