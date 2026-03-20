import asyncio
from os import name, system

import prepare
import upload

TOKEN = ""


def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")


async def main():
    while True:
        clear()
        print("1. Prepare history for ListenBrainz")
        print("2. Upload history to ListenBrainz")
        print("3. Prepare and Upload history")
        print("4. Exit")
        match input(">>> "):
            case "1":
                await prepare.history()
            case "2":
                if not TOKEN:
                    t = input("Please enter your ListenBrainz User Token: ").strip()
                else:
                    t = TOKEN
                await upload.history(t)
                input("Press Enter...")
            case "3":
                if not TOKEN:
                    t = input("Please enter your ListenBrainz User Token: ").strip()
                else:
                    t = TOKEN
                print("Preparing history...")
                he, ht = await prepare.history()
                print(f"Prepared history(tracks: {ht}; errors: {he});")
                await upload.history(t)
                input("Press Enter...")
            case "4":
                return
            case _:
                print("Incorrect")


asyncio.run(main())
