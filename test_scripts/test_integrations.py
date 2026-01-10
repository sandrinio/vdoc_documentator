import shutil
import pytest
from typer.testing import CliRunner
from vdoc.main import app
from pathlib import Path

runner = CliRunner()

def test_integration_injection(tmp_path):
    """
    Test that vdoc init correctly injects Cursor rules.
    """
    # Change workspace to temp
    import os
    os.chdir(tmp_path)
    
    # 1. Run Init
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    
    # 2. Check Directories
    rules_dir = tmp_path / ".cursor" / "rules"
    assert rules_dir.exists()
    assert rules_dir.is_dir()
    
    # 3. Check Files
    plan_rule = rules_dir / "vdoc-plan.mdc"
    exec_rule = rules_dir / "vdoc-exec.mdc"
    
    assert plan_rule.exists()
    assert exec_rule.exists()
    
    # 4. Check Cursor Rule Content
    assert "/vdoc-plan" in plan_rule.read_text()
    assert "/vdoc-exec" in exec_rule.read_text()

    # 5. Check Antigravity Workflows
    workflow_dir = tmp_path / ".agent" / "workflows"
    assert workflow_dir.exists()
    
    plan_workflow = workflow_dir / "vdoc-plan.md"
    exec_workflow = workflow_dir / "vdoc-exec.md"
    
    assert plan_workflow.exists()
    assert exec_workflow.exists()
    assert "Run the VDoc Planning workflow" in plan_workflow.read_text()
