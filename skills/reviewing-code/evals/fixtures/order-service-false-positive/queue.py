from parser import parse_payload
from producer import build_payload


def enqueue(queue, event):
    queue.push(build_payload(event))


def consume(queue):
    raw = queue.pop()
    return parse_payload(raw)
