from datetime import datetime
from json import dump, load

import httpx


async def history():
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            tracks = load(f)
    except FileNotFoundError:
        print(
            "Cant find history.json. Download and extract yandex history archive first."
        )
        return 0, 0
    errors = []
    tracks_lb = []
    async with httpx.AsyncClient() as client:
        for track in tracks:
            id = track["id"]
            r = await client.get(f"https://api.music.yandex.net/tracks/{id}")
            d = r.json()
            d = d["result"][0]
            error = None
            try:
                t = d["title"]
            except Exception as e:
                t = "None"
                error = e
                print(f"ERROR: {e}; ID: {id}")
            try:
                a = d["artists"][0]["name"]
            except Exception as e:
                a = "None"
                error = e
                print(f"ERROR: {e}; ID: {id}")
            try:
                al = d["albums"][0]["title"]
            except Exception as e:
                al = "None"
                error = e
                print(f"ERROR: {e}; ID: {id}")
            if not error:
                print(f"Title: {t}; Artist: {a}; Album: {al}; ID: {id}")
                time = track["timestamp"]
                dt = datetime.fromisoformat(time.replace("Z", "+03:00"))
                time = int(dt.timestamp())
                track_lb = {"title": t, "artist": a, "album": al, "time": time}
                tracks_lb.append(track_lb)
            else:
                errors.append(id)
            del d, r, id, t, a, al, error
        if errors:
            with open("errors_.json", "w", encoding="utf-8") as f:
                dump(errors, f, ensure_ascii=False, indent=4)
            print(f"Saved {len(errors)} errors to errors.json")
        if tracks_lb:
            with open("history_for_lb.json", "w", encoding="utf-8") as f:
                dump(tracks_lb, f, ensure_ascii=False, indent=4)
            print(f"Saved {len(tracks_lb)} history to history_for_lb.json")
    return len(errors), len(tracks_lb)
