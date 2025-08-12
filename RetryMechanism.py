import logging
import time
import asyncio  


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("weather.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RetryMechanism:
    """Provides retry logic for synchronous and asynchronous functions."""

    async def retry_async(func, *args, retries=3, delay=2, **kwargs):
        """Retries an asynchronous function on failure.

        Args:
            func (Callable): The async function to retry.
            *args: Positional arguments to pass to the function.
            retries (int, optional): Number of retry attempts. Defaults to 3.
            delay (int, optional): Delay in seconds between retries. Defaults to 2.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            Any: The result of the function if successful.

        Raises:
            Exception: The last exception raised after all retries fail.
        """
        for attempt in range(1, retries + 1):
            try:
                logger.info(f"Attempt {attempt} for {func.__name__}")
                result = await func(*args, **kwargs)
                logger.info(f"Success on attempt {attempt}")
                return result
            except Exception as e:
                logger.error(f"Error on attempt {attempt}: {e}")
                if attempt < retries:
                    logger.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    logger.critical(f"All {retries} attempts failed.")
                    raise

    def retry_sync(func, *args, retries=3, delay=2, **kwargs):
        """Retries a synchronous function on failure.

        Args:
            func (Callable): The function to retry.
            *args: Positional arguments to pass to the function.
            retries (int, optional): Number of retry attempts. Defaults to 3.
            delay (int, optional): Delay in seconds between retries. Defaults to 2.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            Any: The result of the function if successful.

        Raises:
            Exception: The last exception raised after all retries fail.
        """
        for attempt in range(1, retries + 1):
            try:
                logger.info(f"Attempt {attempt} for {func.__name__}")
                result = func(*args, **kwargs)
                logger.info(f"Success on attempt {attempt}")
                return result
            except Exception as e:
                logger.error(f"Error on attempt {attempt}: {e}")
                if attempt < retries:
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.critical(f"All {retries} attempts failed.")
                    raise
