from dotenv import load_dotenv
import asyncio
import aiohttp
import json
import time
import os


class Translate():
    def __init__(self):
        self.api_key = os.getenv("API_KEY_TR")
        self.url = "https://api.mymemory.translated.net/get"
        self.session: aiohttp.ClientSession | None = None

    async def setup(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close(self):
        if self.session is not None:
            await self.session.close()
            self.session = None

    # To start the translation
    async def start_translate(self, data: list | tuple, source_lang: str, target_lang: str) -> None:
        tasks = [self.translate_text(line["LineText"], source_lang, target_lang)
                 for line in data
                 if line["LineText"].strip() and len(line["LineText"]) > 1]

        results = await asyncio.gather(*tasks)
        for result in results:
            print(result)

    # To translate a single text
    async def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        params = {
            "q": text,
            "langpair": f"{source_lang}|{target_lang}",
            "key": self.api_key
        }

        async with self.session.get(url=self.url, params=params) as r:
            response = await r.json()
            return response["responseData"]["translatedText"]


async def main():
    load_dotenv()
    with open("translate\\result.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    print(data)
    tr = Translate()
    await tr.setup()
    print("\nStarting translation...\n")

    try:
        await tr.start_translate(data, "en", "id")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await tr.close()


if __name__ == "__main__":
    asyncio.run(main())
