import httpx
from typing import Dict, Any, Optional
from rich.console import Console

console = Console()

# Placeholder URL
API_BASE_URL = "https://api.vibepm.ai/v1"

async def fetch_prompts(api_key: Optional[str]) -> Dict[str, str]:
    """
    Fetches system prompts from the VibePM Intelligence Service.
    """
    # TODO: Implement actual API call
    # async with httpx.AsyncClient() as client:
    #     resp = await client.get(...)
    
    # Mock Response
    return {
        "scout_system_prompt": (
            "You are a VDoc Scout Agent. Your job is to analyze the codebase context "
            "and create a detailed plan for documentation. "
            "The user will provide a 'Context Map' of the project. "
            "You must output a plan in a specific format."
        ),
        "writer_system_prompt": (
            "You are a VDoc Technical Writer. Your job is to read the code and write "
            "perfect documentation based on the user's plan."
        )
    }

def get_prompts_sync(api_key: Optional[str]) -> Dict[str, str]:
    """Sync wrapper for fetch_prompts"""
    import asyncio
    return asyncio.run(fetch_prompts(api_key))
