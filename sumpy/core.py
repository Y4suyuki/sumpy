from collections.abc import Iterable
import tiktoken
import openai

DAVINC_MAX_TOKEN_SIZE = 2048


class Sumpy:
    def __init__(self, api_key: str):
        self.__openai = openai
        self.__openai.api_key = api_key

    def summarize(self, s: str) -> list[str]:

        sentences = split_into_sentences_by_token_size(s)
        lsentences = list(sentences)
        print(lsentences)
        print(f"len of sentences: {len(lsentences)}")

        res = [self.__summarize(_s) for _s in lsentences]

        return res

    def __summarize(self, s: str) -> str:
        print("trying to summarize")
        print(s)
        order_header = "以下の文章を要約してください\n---\n"
        end = "\n要約: \n"
        res = self.__openai.Completion.create(
            engine="text-davinci-003",
            prompt=order_header + s + end,
            max_tokens=800,
            temperature=0.7,
            timeout=(30, 60),  # 30s to connection timeout and 60s to total timeout
        )
        return res.choices[0].text


def get_tokens(s: str):
    encoding_model = "r50k_base"
    enc = tiktoken.get_encoding(encoding_model)
    tokens = enc.encode(s)
    return tokens


def split_into_sentences(s: str) -> Iterable[str]:
    stop_words = "。\n"
    x = ""
    for c in s:
        if c in stop_words:
            if x != "" or x not in stop_words:
                yield x
            x = ""
        else:
            x += c

    if x != "":
        yield x


def split_into_sentences_by_token_size(
    s: str, token_limit: int = DAVINC_MAX_TOKEN_SIZE, summarize_ratio=0.15
) -> Iterable[str]:
    _token_limit = int(token_limit * (1 - summarize_ratio))
    sentences = split_into_sentences(s)
    result = ""
    for sentence in sentences:
        tmp = result + sentence if result.strip() == "" else result + "。" + sentence
        if len(get_tokens(tmp)) > _token_limit:
            yield result + "。"
            result = sentence
        else:
            result = tmp

    if result.strip() != "":
        yield result + "。"
