"""
BPE-токенизатор: применяет к новому тексту слияния, выученные train_bpe.py.

Использование:
    from tokenizer import BPETokenizer

    tok = BPETokenizer("../artifacts/vocab_1000.json", "../artifacts/merges_1000.txt")
    tokens = tok.encode("Привет, как дела?")
    print(tokens)
    ids = tok.encode_ids("Привет, как дела?")
"""

import re
import json
from typing import List

END_OF_WORD = "</w>"
WORD_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)

UNK_TOKEN = "<unk>"
PAD_TOKEN = "<pad>"
BOS_TOKEN = "<bos>"
EOS_TOKEN = "<eos>"


class BPETokenizer:
    def __init__(self, vocab_path: str, merges_path: str):
        with open(vocab_path, "r", encoding="utf-8") as f:
            self.token_to_id = json.load(f)
        self.id_to_token = {i: t for t, i in self.token_to_id.items()}

        self.merges = self._load_merges(merges_path)
        # ранг слияния = порядок обучения (меньше -> применяется раньше)
        self.merge_ranks = {pair: i for i, pair in enumerate(self.merges)}

    @staticmethod
    def _load_merges(merges_path: str):
        merges = []
        with open(merges_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line or line.startswith("#"):
                    continue
                a, b = line.split(" ")
                merges.append((a, b))
        return merges

    def _get_pairs(self, symbols):
        return {(symbols[i], symbols[i + 1]) for i in range(len(symbols) - 1)}

    def _bpe_word(self, word: str) -> List[str]:
        """Применить выученные BPE-слияния к одному слову."""
        symbols = list(word) + [END_OF_WORD]
        if len(symbols) == 1:
            return symbols

        pairs = self._get_pairs(symbols)
        while pairs:
            # выбрать пару с наименьшим рангом (выучена раньше всех остальных)
            candidate = min(
                pairs, key=lambda p: self.merge_ranks.get(p, float("inf"))
            )
            if candidate not in self.merge_ranks:
                break  # ни одна из оставшихся пар не была выучена

            a, b = candidate
            new_symbols = []
            i = 0
            while i < len(symbols):
                if (
                    i < len(symbols) - 1
                    and symbols[i] == a
                    and symbols[i + 1] == b
                ):
                    new_symbols.append(a + b)
                    i += 2
                else:
                    new_symbols.append(symbols[i])
                    i += 1
            symbols = new_symbols
            if len(symbols) == 1:
                break
            pairs = self._get_pairs(symbols)

        return symbols

    def encode(self, text: str) -> List[str]:
        """Строка -> список токенов (строк)."""
        text = text.lower()
        words = WORD_RE.findall(text)
        tokens: List[str] = []
        for word in words:
            for piece in self._bpe_word(word):
                if piece == END_OF_WORD:
                    continue  # маркер конца слова не выводим отдельным токеном
                tokens.append(self._resolve_unknown(piece))
        return tokens

    def _resolve_unknown(self, piece: str) -> str:
        """Если куска нет в словаре целиком - разбить на известные символы
        или заменить на <unk>."""
        if piece in self.token_to_id:
            return piece
        # fallback: попробовать разложить неизвестный кусок посимвольно
        # (на случай встречи символа, которого не было в обучающем корпусе)
        chars = [c for c in piece if c in self.token_to_id]
        if chars:
            return "".join(chars) if "".join(chars) in self.token_to_id else UNK_TOKEN
        return UNK_TOKEN

    def encode_ids(self, text: str) -> List[int]:
        tokens = self.encode(text)
        unk_id = self.token_to_id[UNK_TOKEN]
        return [self.token_to_id.get(t, unk_id) for t in tokens]

    def decode(self, tokens: List[str]) -> str:
        """Собрать токены обратно в текст (для проверки)."""
        text = "".join(tokens)
        text = text.replace(END_OF_WORD, " ")
        return text.strip()

    def vocab_size(self) -> int:
        return len(self.token_to_id)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Токенизация предложения с помощью обученного BPE")
    parser.add_argument("--vocab", default="../artifacts/vocab_1000.json")
    parser.add_argument("--merges", default="../artifacts/merges_1000.txt")
    parser.add_argument("sentence", nargs="?", help="предложение для токенизации")
    args = parser.parse_args()

    tok = BPETokenizer(args.vocab, args.merges)

    if args.sentence:
        sentence = args.sentence
    else:
        sentence = input("Введите предложение: ")

    tokens = tok.encode(sentence)
    print("Токены:", tokens)
    print("Кол-во токенов:", len(tokens))
    print("ID токенов:", tok.encode_ids(sentence))
