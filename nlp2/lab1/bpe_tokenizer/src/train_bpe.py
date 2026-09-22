"""
Обучение символьного BPE (Byte-Pair Encoding) токенизатора
на текстах русской классики.

Алгоритм (классический, Sennrich et al., 2016):
1. Каждое слово корпуса представляется как последовательность символов
   (+ спецсимвол конца слова </w>).
2. Считается частота слов -> частота смежных пар символов.
3. На каждом шаге самая частая пара символов "склеивается" в новый токен,
   который добавляется в словарь. Повторяем, пока словарь не достигнет
   нужного размера.
"""

import re
import os
import sys
import json
import glob
import argparse
from collections import Counter, defaultdict

END_OF_WORD = "</w>"          # маркер конца слова
WORD_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)   # слово ИЛИ один знак пунктуации


def read_corpus(data_dir: str) -> str:
    """Считать и склеить все .txt файлы из папки с текстами."""
    texts = []
    for path in sorted(glob.glob(os.path.join(data_dir, "*.txt"))):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            texts.append(f.read())
    if not texts:
        raise FileNotFoundError(f"В папке {data_dir} не найдено .txt файлов")
    return "\n".join(texts)


def get_word_freqs(text: str) -> Counter:
    """Разбить текст на слова/знаки препинания и посчитать частоты."""
    text = text.lower()
    words = WORD_RE.findall(text)
    return Counter(words)


def word_to_symbols(word: str):
    """'привет' -> ('п','р','и','в','е','т','</w>')"""
    return tuple(list(word) + [END_OF_WORD])


def get_pair_stats(word_freqs: dict):
    """Посчитать частоты всех смежных пар символов + индекс пара->слова (для инкрементальных обновлений)."""
    pairs = Counter()
    where = defaultdict(set)  # pair -> множество слов (кортежей символов), где она встречается
    for symbols, freq in word_freqs.items():
        for i in range(len(symbols) - 1):
            p = (symbols[i], symbols[i + 1])
            pairs[p] += freq
            where[p].add(symbols)
    return pairs, where


def apply_merge_to_word(symbols, bigram, merged_symbol):
    new_symbols = []
    i = 0
    n = len(symbols)
    changed = False
    while i < n:
        if i < n - 1 and (symbols[i], symbols[i + 1]) == bigram:
            new_symbols.append(merged_symbol)
            i += 2
            changed = True
        else:
            new_symbols.append(symbols[i])
            i += 1
    return tuple(new_symbols), changed


def train_bpe(text: str, vocab_size: int, min_freq: int = 1, verbose: bool = True):
    """
    Обучить BPE. Возвращает:
      vocab   - список токенов (символьный алфавит + выученные слияния)
      merges  - список пар (a, b) в порядке их обучения (нужен для энкодинга)

    Оптимизация: после первого полного подсчёта пар мы обновляем счётчик
    инкрементально, пересчитывая только слова, задействованные в последнем
    слиянии, а не весь корпус на каждом шаге.
    """
    word_freqs_raw = get_word_freqs(text)
    word_freqs = {}
    for word, freq in word_freqs_raw.items():
        word_freqs[word_to_symbols(word)] = freq

    alphabet = set()
    for symbols in word_freqs:
        alphabet.update(symbols)
    vocab = sorted(alphabet)

    merges = []

    if verbose:
        print(f"[train_bpe] Уникальных слов: {len(word_freqs)}")
        print(f"[train_bpe] Начальный алфавит: {len(vocab)} символов")
        print(f"[train_bpe] Целевой размер словаря: {vocab_size}")

    pair_stats, where = get_pair_stats(word_freqs)

    step = 0
    while len(vocab) < vocab_size:
        if not pair_stats:
            break
        best_pair, best_freq = pair_stats.most_common(1)[0]
        if best_freq < min_freq:
            break

        merged_symbol = best_pair[0] + best_pair[1]
        affected_words = where.pop(best_pair, set())

        for old_symbols in affected_words:
            freq = word_freqs.pop(old_symbols, None)
            if freq is None:
                continue
            new_symbols, changed = apply_merge_to_word(old_symbols, best_pair, merged_symbol)
            if not changed:
                continue

            # убрать вклад старого слова из статистики пар
            for i in range(len(old_symbols) - 1):
                p = (old_symbols[i], old_symbols[i + 1])
                pair_stats[p] -= freq
                if pair_stats[p] <= 0:
                    del pair_stats[p]
                where[p].discard(old_symbols)

            # добавить вклад нового слова
            word_freqs[new_symbols] = word_freqs.get(new_symbols, 0) + freq
            for i in range(len(new_symbols) - 1):
                p = (new_symbols[i], new_symbols[i + 1])
                pair_stats[p] += freq
                where[p].add(new_symbols)

        vocab.append(merged_symbol)
        merges.append(best_pair)
        step += 1
        if verbose and step % 200 == 0:
            print(f"[train_bpe] шаг {step}: слияние {best_pair} -> '{merged_symbol}' "
                  f"(частота={best_freq}), размер словаря={len(vocab)}")

    if verbose:
        print(f"[train_bpe] Готово. Итоговый размер словаря: {len(vocab)}, "
              f"слияний: {len(merges)}")

    return vocab, merges


def save_artifacts(vocab, merges, out_dir: str, vocab_size: int):
    os.makedirs(out_dir, exist_ok=True)

    # id -> токен, специальные токены в начале
    special_tokens = ["<pad>", "<unk>", "<bos>", "<eos>"]
    full_vocab = special_tokens + vocab
    token_to_id = {tok: i for i, tok in enumerate(full_vocab)}

    vocab_path = os.path.join(out_dir, f"vocab_{vocab_size}.json")
    with open(vocab_path, "w", encoding="utf-8") as f:
        json.dump(token_to_id, f, ensure_ascii=False, indent=1)

    merges_path = os.path.join(out_dir, f"merges_{vocab_size}.txt")
    with open(merges_path, "w", encoding="utf-8") as f:
        f.write("#version: 0.1 - BPE merges (порядок важен)\n")
        for a, b in merges:
            f.write(f"{a} {b}\n")

    print(f"[save_artifacts] Словарь сохранён: {vocab_path} ({len(full_vocab)} токенов)")
    print(f"[save_artifacts] Слияния сохранены: {merges_path} ({len(merges)} правил)")
    return vocab_path, merges_path


def main():
    parser = argparse.ArgumentParser(description="Обучение BPE-токенизатора на русских романах")
    parser.add_argument("--data-dir", default="../data", help="папка с .txt файлами")
    parser.add_argument("--out-dir", default="../artifacts", help="куда сохранить словарь и слияния")
    parser.add_argument("--vocab-size", type=int, default=1000, help="размер словаря (1000 или 3000)")
    args = parser.parse_args()

    text = read_corpus(args.data_dir)
    print(f"[main] Длина корпуса: {len(text)} символов")

    vocab, merges = train_bpe(text, args.vocab_size)
    save_artifacts(vocab, merges, args.out_dir, args.vocab_size)


if __name__ == "__main__":
    main()
