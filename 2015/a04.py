from pathlib import Path
import hashlib


def main_a():
    data = "ckczppom"
    i = 0
    while True:
        m = hashlib.md5()
        m.update(f"{data}{i}".encode())
        if m.hexdigest().startswith("000000"):
            break
        i += 1
    print(i)


if __name__ == "__main__":
    main_a()
