"""FitCoach entry point."""

import asyncio
import logging
from fitcoach.agent import FitCoachAgent
from fitcoach.config import load_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("fitcoach")


async def main():
    """Run the FitCoach agent."""
    config = load_config()
    agent = FitCoachAgent(config)
    logger.info("Starting FitCoach agent...")
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
