import argparse
import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from .agent import DeepSeekAgent


def setup_logging(log_dir: str = "logs"):
    """配置日志"""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_path / f"crawl_{timestamp}.log"

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)


async def run_single_query(agent: DeepSeekAgent, query: str, logger) -> bool:
    """运行单个 query"""
    logger.info(f"Starting query: {query}")
    try:
        result = await agent.run(query)
        if result["success"]:
            logger.info(f"Query completed successfully: {query}")
            logger.info(f"Result: {result['result']}")
            return True
        else:
            logger.error(f"Query failed: {query}")
            return False
    except Exception as e:
        logger.exception(f"Error running query: {e}")
        return False
    finally:
        await agent.close()


async def run_batch(agent: DeepSeekAgent, queries: list[str], logger) -> dict:
    """批量运行 queries"""
    results = {"total": len(queries), "success": 0, "failed": 0}

    for i, query in enumerate(queries, 1):
        logger.info(f"Processing {i}/{len(queries)}: {query}")
        success = await run_single_query(agent, query, logger)
        if success:
            results["success"] += 1
        else:
            results["failed"] += 1

    logger.info(f"Batch complete: {results}")
    return results


async def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="DeepSeek Auto Crawl")
    parser.add_argument("-q", "--query", type=str, help="Single query to run")
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="JSON file containing queries",
        default="tests/test_queries.json",
    )
    parser.add_argument(
        "-p",
        "--profile",
        type=str,
        help="Chrome profile directory for login",
        default=None,
    )
    args = parser.parse_args()

    logger = setup_logging()

    agent = DeepSeekAgent(profile_dir=args.profile)

    if args.query:
        await run_single_query(agent, args.query, logger)
    elif args.file and Path(args.file).exists():
        with open(args.file, encoding="utf-8") as f:
            data = json.load(f)
            queries = [item["query"] for item in data]
        await run_batch(agent, queries, logger)
    else:
        logger.error("Please provide either -q or -f argument")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
