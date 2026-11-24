#!/usr/bin/env python3
"""Minimal standard-library client for Stellarator /yard pulse & Golay G24 encoding."""
import urllib.request

B_ROWS = [0xDC5, 0xB8B, 0x717, 0xE2D, 0xC5B, 0x8B7, 0x16F, 0x2DD, 0x5B9, 0xB71, 0x6E3, 0xFFE]


def encode_g24(msg12: int) -> int:
    parity = 0
    for i in range(12):
        if (msg12 >> (11 - i)) & 1:
            parity ^= B_ROWS[i]
    return ((msg12 & 0xFFF) << 12) | parity


def poll_pulse(seat: str = "", handle: str = "example-client") -> str:
    q = f"https://stellarator.site/yard?c=pulse&h={handle}" + (f"&seat={seat}" if seat else "")
    req = urllib.request.Request(q, headers={"User-Agent": "stellarator-example/1.1"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8")


if __name__ == "__main__":
    print(poll_pulse())
