import requests
import re
from collections import Counter
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

# 1. Завантажуємо текст із заданої URL-адреси
def fetch_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# 2. Токенізація тексту (очищення та розбиття на слова)
def tokenize(text):
    text = text.lower()  # Приводимо до нижнього регістру
    words = re.findall(r'\b\w+\b', text)  # Знаходимо всі слова
    return words

# 3. Обчислення частоти слів за допомогою MapReduce
def map_reduce(text, num_threads=4):
    # Поділяємо текст на частини для багатопотокового оброблення
    chunk_size = len(text) // num_threads
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Мапінг: виконуємо токенізацію для кожного блоку тексту
        results = executor.map(tokenize, chunks)
    
    # Редюс: підрахунок частоти кожного слова
    word_count = Counter()
    for result in results:
        word_count.update(result)
    
    return word_count

# 4. Функція для візуалізації топ-10 слів
def visualize_top_words(word_count):
    top_words = word_count.most_common(10)  # Топ-10 слів
    words, counts = zip(*top_words)
    
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top 10 Most Frequent Words')
    plt.xticks(rotation=45)
    plt.show()

# 5. Основний блок коду
if __name__ == '__main__':
    url = 'https://www.gutenberg.org/files/11/11-0.txt'  # URL з текстом
    text = fetch_text(url)
    
    if text:
        word_count = map_reduce(text)
        visualize_top_words(word_count)
    else:
        print("Не вдалося завантажити текст.")
