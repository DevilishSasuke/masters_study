import os
import re
import json
from collections import Counter, defaultdict
from tqdm import tqdm

DATA_DIR = "data"
END_OF_WORD = "</w>"

def load_texts(data_dir: str) -> str:
    """Считывает все .txt файлы из указанной директории и объединяет в одну строку."""
    full_text = []
    files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]
    for file_name in files:
        with open(os.path.join(data_dir, file_name), "r", encoding="utf-8") as f:
            full_text.append(f.read())
    return " ".join(full_text)


def build_word_frequency(text: str) -> dict[tuple[str, ...], int]:
    """
    Разбивает текст на слова, приводит к нижнему регистру
    и строит частотный словарь вида:
    """
    # отсекаем лишние знаки (препинания и т.д.)
    words = re.findall(r'[а-яё]+(?:-[а-яё]+)?', text.lower())
    
    raw_counts = Counter(words)
    print(f"total words: {len(words)}")
    print(f"unique words: {len(raw_counts)}")
    
    # Преобразуем каждое слово в кортеж отдельных символов с маркером конца слова
    vocab = {}
    for word, count in raw_counts.items():
        char_tuple = tuple(list(word) + [END_OF_WORD])
        vocab[char_tuple] = count
        
    return vocab

def get_stats(vocab: dict[tuple[str, ...], int]) -> dict[tuple[str, str], int]:
    pairs = defaultdict(int)
    for word, frequency in vocab.items():
        for i in range(len(word) - 1):
            pairs[(word[i], word[i + 1])] += frequency
    return pairs

def merge_vocab(pair: tuple[str, str], v_in: dict[tuple[str, ...], int]) -> dict[tuple[str, ...], int]:
    v_out = {}
    pair_str = "".join(pair)
    for word, frequency in v_in.items():
        new_word = []
        i = 0
        while i < len(word):
            if i < len(word) - 1 and word[i] == pair[0] and word[i+1] == pair[1]:
                new_word.append(pair_str)
                i += 2
            else:
                new_word.append(word[i])
                i += 1
        v_out[tuple(new_word)] = frequency
    return v_out

def train_bpe_checkpoints(vocab: dict[tuple[str, ...], int], checkpoints: list[int]) -> dict:
    bpe_rules = []
    results = {}
    max_merges = max(checkpoints)
    
    print(f"Начинаем обучение BPE (до {max_merges} итераций)...")
    for i in tqdm(range(1, max_merges + 1)):
        pairs = get_stats(vocab)
        if not pairs:
            break
            
        best_pair = max(pairs, key=pairs.get)
        bpe_rules.append(best_pair)
        vocab = merge_vocab(best_pair, vocab)
        
        if i in checkpoints:
            results[i] = {
                "rules": list(bpe_rules), 
                "vocab": vocab.copy()
            }
            
    return results

if __name__ == "__main__":
    text_corpus = load_texts(DATA_DIR)
    word_freq = build_word_frequency(text_corpus)
    
    checkpoints = [1000, 3000]
    models = train_bpe_checkpoints(word_freq, checkpoints)
    
    for size, data in models.items():
        filename = f"bpe_rules_{size}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data["rules"], f, ensure_ascii=False, indent=2)
        print(f"Правила сохранены в {filename}")