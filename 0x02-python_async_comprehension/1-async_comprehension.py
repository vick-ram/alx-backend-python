#!/usr/bin/env python3
"""1-async_comprehension.py module"""
import asyncio
from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    Coroutine that collects 10 random numbers using an async comprehensing
    over async_generator, then returns the 10 random numbers.
    """
    return [i async for i in async_generator()]
