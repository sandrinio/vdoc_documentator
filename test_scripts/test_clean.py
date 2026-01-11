import os
from pathlib import Path
import shutil
import vdoc.commands.clean as clean

def test_clean_command():
    test_dir = Path("temp_clean_test")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()
    
    # Setup mock environment
    (test_dir / ".vdoc").mkdir()
    (test_dir / ".vdoc" / "context.md").touch()
    
    (test_dir / ".cursor" / "rules").mkdir(parents=True)
    (test_dir / ".cursor" / "rules" / "vdoc-plan.mdc").touch()
    (test_dir / ".cursor" / "rules" / "vdoc-exec.mdc").touch()
    (test_dir / ".cursor" / "rules" / "other.mdc").touch() # Should stay
    
    (test_dir / "product_documentation").mkdir()
    (test_dir / "product_documentation" / "doc.md").touch() # Should stay
    
    # Change cwd to test_dir to simulate running inside a project
    os.chdir(test_dir)
    
    print("Running clean command...")
    try:
        clean.run_clean()
    finally:
        # Reset cwd
        os.chdir("..")
        
    # Verify
    assert not (test_dir / ".vdoc").exists(), ".vdoc should be removed"
    assert not (test_dir / ".cursor" / "rules" / "vdoc-plan.mdc").exists(), "vdoc-plan.mdc should be removed"
    assert not (test_dir / ".cursor" / "rules" / "vdoc-exec.mdc").exists(), "vdoc-exec.mdc should be removed"
    
    assert (test_dir / ".cursor" / "rules" / "other.mdc").exists(), "other.mdc should be preserved"
    assert (test_dir / "product_documentation" / "doc.md").exists(), "product_documentation should be preserved"
    
    print("[SUCCESS] vdoc clean verification passed!")
    
    # Cleanup
    if test_dir.exists():
        shutil.rmtree(test_dir)

if __name__ == "__main__":
    test_clean_command()
