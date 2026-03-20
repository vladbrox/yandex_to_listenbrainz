from json import load

import httpx

URL = "https://api.listenbrainz.org/"


# history
async def get_payload_listens(tracks):
    payload_temp = []
    for track in tracks:
        try:
            temp = {
                "listened_at": track["time"],
                "track_metadata": {
                    "artist_name": track["artist"],
                    "track_name": track["title"],
                    "release_name": track["album"],
                },
            }
            payload_temp.append(temp)
        except Exception as e:
            print(f"Getting {track} error: {e}")
    payload = {"listen_type": "import", "payload": payload_temp}
    return payload


async def submit_listens(client, payload, tuinput):
    token = tuinput
    try:
        headers = {"Authorization": f"Token {token}"}
        r = await client.post(URL + "1/submit-listens", json=payload, headers=headers)
        if r.status_code == 200:
            print("Successfully submitted history!")
        else:
            print(f"{r.status_code} error: {r.text}")
    except Exception as e:
        print(f"Request error: {e}")


async def history(t):
    try:
        with open("history_for_lb.json", "r", encoding="utf-8") as f:
            tracks = load(f)
            le = len(tracks)
    except FileNotFoundError:
        print(
            "FileNotFoundError: 'history_for_lb.json' not found. Try run main.py first."
        )
        return
    if le < 1000:
        payload = await get_payload_listens(tracks)
        async with httpx.AsyncClient() as client:
            await submit_listens(client, payload, t)
    else:
        async with httpx.AsyncClient() as client:
            print(f"Starting upload history({le})")
            while tracks:
                target = tracks[:1000]
                payload = await get_payload_listens(target)
                await submit_listens(client, payload, t)
                tracks = tracks[1000:]
