"""Test script to verify Runner import and usage"""
import asyncio
from agents import Runner, Agent

async def test_runner():
    """Test basic Runner usage"""
    agent = Agent(
        name="Test",
        instructions="You are a helpful assistant"
    )

    result = await Runner.run(agent, "Hello")
    print(f"Success! Result: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(test_runner())
