import re
import json

END_OF_WORD = "</w>"

class BPETokenizer:
    def __init__(self, rules_path: str):
        """
        Инициализирует токенизатор, загружая правила BPE из файла JSON.
        """
        with open(rules_path, "r", encoding="utf-8") as f:
            loaded_rules = json.load(f)
            # JSON сохраняет кортежи как списки, переводим обратно в tuple для надежности
            self.rules = [tuple(rule) for rule in loaded_rules]
            
    def tokenize_word(self, word: str) -> list[str]:
        """Применяет выученные правила к одному слову."""
        tokens = list(word) + [END_OF_WORD]
        
        for rule in self.rules:
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i < len(tokens) - 1 and tokens[i] == rule[0] and tokens[i+1] == rule[1]:
                    new_tokens.append(rule[0] + rule[1])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens
            
        return tokens

    def tokenize_sentence(self, sentence: str) -> list[str]:
        """Токенизирует целое предложение."""
        words = re.findall(r'[а-яё]+(?:-[а-яё]+)?', sentence.lower())
        
        sentence_tokens = []
        for word in words:
            sentence_tokens.extend(self.tokenize_word(word))
            
        return sentence_tokens

if __name__ == "__main__":
    # Демонстрация использования
    # Предполагается, что файлы bpe_rules_1000.json и bpe_rules_3000.json уже созданы
    
    tokenizer_1000 = BPETokenizer("bpe_rules_1000.json")
    tokenizer_3000 = BPETokenizer("bpe_rules_3000.json")
    
    test_sentence = input("Введите предложение для токенизации: ")
    
    tokens_1000 = tokenizer_1000.tokenize_sentence(test_sentence)
    print(f"Токенизация для 1000 правил, количество получившихся токенов: {len(tokens_1000)}):")
    print(tokens_1000)
    
    tokens_3000 = tokenizer_3000.tokenize_sentence(test_sentence)
    print(f"Токенизация для 3000 правил, количество получившихся токенов: {len(tokens_3000)}):")
    print(tokens_3000)