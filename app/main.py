import asyncio
from fastapi import FastAPI
from app.router.WeatherRouter import router as weather_router
from cli.CLI import Cli


app = FastAPI()
app.include_router(weather_router)

async def main():
    cli = Cli()
    await cli.Start()

if __name__ == "__main__":
    asyncio.run(main())
