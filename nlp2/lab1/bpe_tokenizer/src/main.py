"""
Точка входа: токенизация предложения обученным BPE-словарём.

Примеры запуска:
    python3 main.py "Мой дядя самых честных правил"
    python3 main.py --vocab-size 3000 "Привет, как дела?"
    python3 main.py                      # интерактивный режим (спросит предложение)
"""

import argparse
from tokenizer import BPETokenizer


def main():
    parser = argparse.ArgumentParser(description="Токенизировать предложение с помощью обученного BPE")
    parser.add_argument("sentence", nargs="?", default=None, help="предложение для токенизации")
    parser.add_argument("--vocab-size", type=int, default=1000, choices=[1000, 3000],
                         help="какой обученный словарь использовать: 1000 или 3000 токенов")
    parser.add_argument("--artifacts-dir", default="../artifacts", help="папка с vocab_*.json и merges_*.txt")
    args = parser.parse_args()

    vocab_path = f"{args.artifacts_dir}/vocab_{args.vocab_size}.json"
    merges_path = f"{args.artifacts_dir}/merges_{args.vocab_size}.txt"

    tokenizer = BPETokenizer(vocab_path, merges_path)

    sentence = args.sentence
    if sentence is None:
        sentence = input("Введите предложение: ")

    tokens = tokenizer.encode(sentence)
    ids = tokenizer.encode_ids(sentence)

    print(f"Словарь: {args.vocab_size} токенов (реально {tokenizer.vocab_size()} с учётом спецтокенов)")
    print(f"Входное предложение: {sentence}")
    print(f"Токены ({len(tokens)}): {tokens}")
    print(f"ID токенов: {ids}")
    print(f"Восстановленный текст: {tokenizer.decode(tokens)}")


if __name__ == "__main__":
    main()
