#!/usr/bin/env python3
"""Зеркалит state.js в страницу дашборда и держит сервер живым.

Вызывается одной строкой после каждой правки состояния:

    python3 .designpilot/sync.py

Делает ровно три вещи, в этом порядке:

  1. Проверяет, что state.js разбирается. Битый файл дальше не идёт: снимок
     на странице остаётся прежним, а не затирается мусором.
  2. Вписывает состояние внутрь dashboard.html между маркерами — атомарно,
     через временный файл рядом. Оборвётся на середине — на месте останется
     целая прежняя страница. Отсюда дашборд показывает данные, даже если его
     открыли файлом, с мёртвым сервером или через месяц после прогона.
  3. Смотрит, жив ли статический сервер этого прогона, и поднимает на прежнем
     порту, если нет. Прежний порт — чтобы уже скопированная ссылка работала.

state.js — это JSON в обёртке `window.STATE = {...}`. Никаких выражений
внутри: `new Date()` в файле означает, что дашборд не обновится, а сообщение
об ошибке придёт сюда, а не в браузер.
"""
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.request

A = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(A, "state.js")
PAGE = os.path.join(A, "dashboard.html")
PORTFILE = os.path.join(A, ".port")
BEGIN, END = "/*STATE-BEGIN*/", "/*STATE-END*/"


def fail(msg):
    print(msg)
    sys.exit(1)


def read_state():
    try:
        raw = open(STATE, encoding="utf-8").read()
    except FileNotFoundError:
        fail("state.js ещё нет — снимок не вписан, сервер не тронут")
    body = raw.split("=", 1)[1] if "=" in raw.split("\n", 1)[0] else raw
    try:
        return json.loads(body.strip().rstrip(";"))
    except json.JSONDecodeError as e:
        fail("state.js не разбирается (строка %d: %s) — снимок оставлен прежним" % (e.lineno, e.msg))


def write_snapshot(state):
    try:
        page = open(PAGE, encoding="utf-8").read()
    except FileNotFoundError:
        return "страницы нет — перекопируй dashboard.html из навыка"
    i, j = page.find(BEGIN), page.find(END)
    if i < 0 or j < 0:
        return "страница без маркеров снимка — перекопируй dashboard.html из навыка"
    # `</` внутри <script> закрыл бы тег и порвал страницу; `<` в JSON безопасен
    payload = "window.STATE=" + json.dumps(state, ensure_ascii=False).replace("</", "<\\/") + ";"
    new = page[: i + len(BEGIN)] + payload + page[j:]
    tmp = PAGE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(new)
    os.replace(tmp, PAGE)
    return "снимок вписан"


def port():
    if os.path.exists(PORTFILE):
        try:
            return int(open(PORTFILE).read().strip())
        except ValueError:
            pass
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    open(PORTFILE, "w").write(str(p))
    return p


def alive(p):
    try:
        urllib.request.urlopen("http://127.0.0.1:%d/" % p, timeout=0.5).read(1)
        return True
    except Exception:
        return False


def serve(p):
    if alive(p):
        return "сервер жив"
    subprocess.Popen(
        [sys.executable, "-m", "http.server", str(p), "--bind", "127.0.0.1", "--directory", A],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True,
    )
    for _ in range(20):
        time.sleep(0.1)
        if alive(p):
            return "сервер поднят"
    return "сервер не поднялся — дашборд открывается файлом: " + PAGE


def main():
    state = read_state()
    snap = write_snapshot(state)
    p = port()
    print("%s · %s · http://127.0.0.1:%d/" % (snap, serve(p), p))


if __name__ == "__main__":
    main()
