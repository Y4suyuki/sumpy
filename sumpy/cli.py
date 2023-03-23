import os
import fire

from sumpy.core import Sumpy


OPENAI_API_KEY = os.environ["OPENAI_API_KEY"] if "OPENAI_API_KEY" in os.environ else ""


def cli(file: str):
    with open(file, "r") as f:
        text = f.read()
    sp = Sumpy(api_key=OPENAI_API_KEY)
    result = sp.summarize(text)
    for r in result:
        print(r)


def main():
    fire.Fire(cli)


if __name__ == "__main__":
    main()
