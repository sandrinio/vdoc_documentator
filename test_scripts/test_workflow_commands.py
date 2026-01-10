import os
import shutil
from pathlib import Path
from typer.testing import CliRunner
from vdoc.main import app

runner = CliRunner()

def test_full_workflow(tmp_path):
    """
    Test the full Init -> Plan -> Exec -> Update workflow in a temp directory.
    """
    # Change into tmp_path so cwd is correct
    os.chdir(tmp_path)
    
    # Create a dummy file to scan
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hello')")
    
    # 1. Test INIT
    print("\n--- Testing INIT ---")
    result = runner.invoke(app, ["init"])
    print(result.stdout)
    assert result.exit_code == 0
    assert (tmp_path / ".vdoc").exists()
    assert (tmp_path / ".vdoc" / "context_map.md").exists()
    assert (tmp_path / ".vdoc" / "spec.md").exists()
    assert (tmp_path / "product_documentation" / "INIT_PROMPT.md").exists()

    # 2. Test PLAN
    print("\n--- Testing PLAN ---")
    result = runner.invoke(app, ["plan"])
    print(result.stdout)
    assert result.exit_code == 0
    assert (tmp_path / "product_documentation" / "PLANNING_PROMPT.md").exists()
    
    # Mock the Agent creating the doc_plan.md
    (tmp_path / ".vdoc" / "doc_plan.md").write_text("# Plan\nCreate API.md")

    # 3. Test EXEC
    print("\n--- Testing EXEC ---")
    result = runner.invoke(app, ["exec"])
    print(result.stdout)
    assert result.exit_code == 0
    assert (tmp_path / "product_documentation" / "EXECUTION_PROMPT.md").exists()

    # 4. Test UPDATE
    print("\n--- Testing UPDATE ---")
    # Add a new file to simulate drift
    (tmp_path / "src" / "new.py").write_text("print('new')")
    
    result = runner.invoke(app, ["update"])
    print(result.stdout)
    assert result.exit_code == 0
    assert (tmp_path / "product_documentation" / "UPDATE_PROMPT.md").exists()

    print("\n--- Workflow Verification Successful ---")
