import json
from math import floor
import os
from time import sleep, time
from typing import Any, TypedDict
import requests
from websocket import create_connection, WebSocket
import websocket
import rel

from solver_lib import Score, Solver

HEADERS = {
    "origin": "https://squabble.me",
    "referer": "https://squabble.me/",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
}

WORDLE_ANSWERS_WORDLIST: list[str] = json.load(open("ott_answer_words.json"))
WORDLE_GUESS_WORDLIST: list[str] = json.load(open("ott_guess_words.json"))

WORDLE_WORDLIST = list(set(WORDLE_ANSWERS_WORDLIST + WORDLE_GUESS_WORDLIST))


class SquabbleBot:
    def __init__(self, token: str):
        self.started = False
        self.first = True
        self.scores = [[Score.UNKNOWN for _ in range(5)] for _ in range(6)]
        self.ready = False

        ws_headers = {
            "Sec-WebSocket-Protocol": "squbbl, " + token,
            "Sec-WebSocket-Version": "13",
        }

        r = requests.get(
            f"https://api.squabble.me/lobby/join/{input('Enter shortcode for the lobby: ')}",
            headers=HEADERS | {"authorization": "Bearer " + token},
        )

        if r.status_code == 200:
            if not r.json():
                print("No lobbies found :(")
                exit()

            print(r.json())
            id: str = r.json()["data"]["id"]
        else:
            print("Uh-oh looks I did an oopsy-woopsy")
            print(r.text)
            print(r.status_code)
            exit()

        # websocket.enableTrace(True)

        self.ws = create_connection(
            f"wss://api.squabble.me/game/{id}/ws", header=HEADERS | ws_headers
        )

        self.solver = Solver(
            lambda word: self.write(word, 0),
            lambda: self.get_scores(),
            WORDLE_ANSWERS_WORDLIST,
            WORDLE_WORDLIST,
            "slate",
        )

        while not self.wait_for_start():
            pass

        try:
            self.solver.solve_forever(lambda: True)
        except json.JSONDecodeError:
            print("I hope the game is over, because it would be really embarrasing if it wasn't")
            self.ws.close()
            print(f"Replay link: https://squabble.me/game/{id}/replay")
            exit()

    def get_scores(self) -> list[list[Score]]:
        message = self.ws.recv()
        data = json.loads(message)
        while not (data["type"] == "state" and "player" in data["data"]):
            message = self.ws.recv()
            data = json.loads(message)
        return [
            [Score(y) for y in x]
            for x in list(data["data"]["public"]["playerStates"].values())[0]["history"]
        ]

    def wait_for_start(self) -> bool:
        message = self.ws.recv()
        data = json.loads(message)
        if (
            # data["type"] == "event"
            # and data["eventData"]["id"] == "GvwDhmLtfVdEup1aLWNpSOAtup33"
            not self.ready
        ):
            self.ws.send(json.dumps({"type": "ready", "data": True}))
            self.ready = True
            self.started = False
            return False
        elif data["type"] == "state":
            self.started = data["data"]["public"]["gameStatus"] == 1
            return self.started
        else:
            return self.started

    # def on_message(self, ws: WebSocketApp, message: str):
    #     data: dict[str, Any] = json.loads(message)
    #     if (
    #         data["type"] == "event"
    #         and data["eventData"]["id"] == "GvwDhmLtfVdEup1aLWNpSOAtup33"
    #     ):
    #         ws.send(json.dumps({"type": "ready", "data": True}))
    #     if data["type"] == "state":
    #         self.started = data["data"]["public"]["gameStatus"] == 1
    #     if self.started:
    #         if self.first:
    #             self.first = False
    #             self.write("irate", 200)
    #         elif data["type"] == "state" and "player" in data["data"]:
    #             self.scores = [
    #                 [Score(y) for y in x]
    #                 for x in list(data["data"]["public"]["playerStates"].values())[0][
    #                     "history"
    #                 ]
    #             ]
    #             print(self.scores)
    #     print(self.started)

    def write(self, word: str, time: int):
        sleep(time / 1000)
        self.ws.send(
            json.dumps(
                {
                    "type": "word",
                    "data": {
                        "word": word,
                        "typing": self.fake_typing(word, time),
                    },
                }
            )
        )

    def fake_typing(self, word: str, time: int) -> list[list[int | str]]:
        typing = []
        currtime = -time
        for i in range(1, 5 + 1):
            typing.append([currtime, word[:i]])
            currtime += time // 6
        return typing


def get_token(something: str, refresh_token: str) -> str:
    with open("token.json", "a+") as token_file:
        empty = False
        try:
            token = json.load(token_file)
        except:
            token = None
            empty = True
        if empty or token["expiry"] >= floor(time()):
            r = requests.post(
                "https://securetoken.googleapis.com/v1/token",
                params={"key": something},
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                },
            )
            response = r.json()
            json.dump(
                {
                    "access_token": response["access_token"],
                    "expiry": floor(time()) + int(response["expires_in"]),
                },
                token_file,
            )
            return response["access_token"]
        return token["access_token"]


SquabbleBot(
    get_token(
        "AIzaSyA_6U-ZrtypmA7qacuQ2L_GD8NrUTORftI",
        "AIwUaOmXtfL69zooVmvi-_51oCq0mJcybmexy9dnJZuDMKpZGoFBMNgmwbykfxjF0lqvjNnWy1dH-DV6Mrjim7SAW-lYxr7TszPo1Um08l5TpGFmQvjEr6Rw_En0-7_lNHbpmNVDRDByi28kyvneVNVDHvojak7Y7Xz4-8_NjDjcbrebN4jWzWg",
    )
)

# SquabbleBot("eyJhbGciOiJSUzI1NiIsImtpZCI6ImYyNGYzMTQ4MTk3ZWNlYTUyOTE3YzNmMTgzOGFiNWQ0ODg3ZWEwNzYiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9vdHRvLXNxdWFiYmxlIiwiYXVkIjoib3R0by1zcXVhYmJsZSIsImF1dGhfdGltZSI6MTY0NDg0OTMwMywidXNlcl9pZCI6IlliN3FjRG81c1lQc3BLTzdmemoweEpZa0dxbzIiLCJzdWIiOiJZYjdxY0RvNXNZUHNwS083ZnpqMHhKWWtHcW8yIiwiaWF0IjoxNjQ0ODQ5MzAzLCJleHAiOjE2NDQ4NTI5MDMsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnt9LCJzaWduX2luX3Byb3ZpZGVyIjoiYW5vbnltb3VzIn19.QpbwNmIpmC70K5dBrpIIogngNVz403HNoJHuELiUG6yxpBSpFz6jz-HUdIEdB-7IQ4ApH2KSmBQiFhlXJnRA2fWKZbz3ja1I0-uopsZSDp-stdLWtDzXaqVdNsz8aYE-JQkHGXKMPD0WSIIOj7D063g0sWmZPL5CfbfV_eMmPq8zBmK2Cg8Hwa6NgRAoAqrHge0MRyfmcKH5vFlPNjxx8fjUUXT9JBZX6geUxsT1W4LifWPKwqtYiAFhhTeuaqUuFrXru8SzBvzljdjSJUIROVN3qcGQTy6Tk43Taq9cgQxSHFf_QN44Il_Sjn_ZIRdIDIrqLFJrmGIqwuVpiaajzg")

# https://squabble.me/game/861fa54f9849b56bd8eb9638a652b5a4a0dc8f32f133209907828ccb7bf037b3/replay