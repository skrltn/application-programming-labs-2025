import os
import re
import time
from typing import List, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from utils import create_annotation_file, ensure_directory


class SoundDownloader:
    """
    Класс для скачивания звуковых файлов с сайта mixkit.co
    """

    def __init__(self, base_url: str = "https://mixkit.co") -> None:
        """
        Инициализация загрузчика

        Args:
            base_url: Базовый URL сайта
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })

    def get_animal_sounds_links(self, max_count: int = 50) -> List[str]:
        """
        Получает ссылки на звуки животных

        Args:
            max_count: Максимальное количество звуков для скачивания

        Returns:
            Список URL звуковых файлов
        """
        sound_links = []
        page = 1

        try:
            while len(sound_links) < max_count:
                url = f"{self.base_url}/free-sound-effects/animals/?page={page}"
                print(f"Парсинг страницы: {url}")

                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                # Проверяем, что получили HTML
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    print(f"Получен не HTML контент: {response.headers.get('Content-Type')}")
                    break

                soup = BeautifulSoup(response.content, 'html.parser')

                # Способ 1: Ищем ссылки в кнопках скачивания
                download_buttons = soup.find_all('a', {'class': re.compile(r'.*download-button.*', re.I)})
                
                # Способ 2: Ищем элементы с атрибутами данных, содержащими ссылки
                if not download_buttons:
                    # Ищем все элементы с атрибутами data-src или data-url
                    for element in soup.find_all(attrs={"data-src": True}):
                        data_src = element['data-src']
                        if '.mp3' in data_src or 'sound' in data_src.lower():
                            sound_url = urljoin(self.base_url, data_src)
                            sound_links.append(sound_url)
                            
                            if len(sound_links) >= max_count:
                                break
                
                # Способ 3: Ищем ссылки в скриптах
                if not download_buttons and len(sound_links) == 0:
                    script_tags = soup.find_all('script')
                    for script in script_tags:
                        if script.string:
                            # Ищем URL в формате JSON или JavaScript
                            urls = re.findall(r'["\'](https?://[^"\']+\.mp3)["\']', script.string)
                            for url_match in urls:
                                if 'animal' in url_match.lower() or 'sound' in url_match.lower():
                                    sound_links.append(url_match)
                                    
                                    if len(sound_links) >= max_count:
                                        break
                
                # Способ 4: Пробуем альтернативный селектор для ссылок
                if not download_buttons and len(sound_links) == 0:
                    # Ищем все ссылки на странице
                    all_links = soup.find_all('a', href=True)
                    for link in all_links:
                        href = link['href']
                        if '.mp3' in href or 'sound' in href.lower():
                            sound_url = urljoin(self.base_url, href)
                            if sound_url not in sound_links:
                                sound_links.append(sound_url)
                                
                                if len(sound_links) >= max_count:
                                    break

                print(f"Найдено ссылок на текущей странице: {len(sound_links)}")
                
                # Проверяем, есть ли следующая страница
                next_button = soup.find('a', string=re.compile(r'next|›|»', re.I))
                if not next_button:
                    print("Следующая страница не найдена")
                    break

                page += 1
                time.sleep(2)  # Увеличиваем задержку

        except requests.RequestException as e:
            print(f"Ошибка сети при парсинге: {e}")
        except Exception as e:
            print(f"Ошибка при парсинге страниц: {e}")

        return sound_links[:max_count]

    def download_sounds(self, download_dir: str, annotation_file: str, max_count: int = 50) -> None:
        """
        Скачивает звуковые файлы и создает аннотацию

        Args:
            download_dir: Директория для сохранения
            annotation_file: Путь к файлу аннотации
            max_count: Максимальное количество файлов для скачивания
        """
        try:
            ensure_directory(download_dir)

            print("Поиск ссылок на звуки животных...")
            sound_links = self.get_animal_sounds_links(max_count)

            if not sound_links:
                print("Не удалось найти звуки для скачивания")
                print("Попробуйте альтернативный подход:")
                
                # Предлагаем альтернативу - использовать заранее подготовленные ссылки
                alternative_links = [
                    "https://assets.mixkit.co/sfx/preview/mixkit-dog-barking-twice-1.mp3",
                    "https://assets.mixkit.co/sfx/preview/mixkit-cat-meow-109.mp3",
                    "https://assets.mixkit.co/sfx/preview/mixkit-rooster-crowing-in-the-morning-246.mp3",
                    "https://assets.mixkit.co/sfx/preview/mixkit-cow-moo-1740.mp3",
                    "https://assets.mixkit.co/sfx/preview/mixkit-bird-chirping-124.mp3",
                ]
                
                print("Использую тестовые звуки для демонстрации...")
                sound_links = alternative_links[:min(max_count, 5)]

            print(f"Найдено {len(sound_links)} звуков. Начинаю загрузку...")

            annotation_data = []

            for i, sound_url in enumerate(sound_links, 1):
                try:
                    # Получаем имя файла из URL
                    filename = os.path.basename(sound_url.split('?')[0])
                    if not filename.endswith('.mp3'):
                        filename = f"animal_sound_{i}.mp3"

                    file_path = os.path.join(download_dir, filename)

                    print(f"Скачивание {i}/{len(sound_links)}: {filename}")

                    response = self.session.get(sound_url, timeout=30)
                    response.raise_for_status()

                    # Сохраняем файл
                    with open(file_path, 'wb') as f:
                        f.write(response.content)

                    # Добавляем в аннотацию
                    absolute_path = os.path.abspath(file_path)
                    relative_path = os.path.relpath(file_path)
                    annotation_data.append((absolute_path, relative_path))

                    print(f"✓ Успешно скачан: {filename}")
                    time.sleep(1)  # Увеличиваем задержку

                except Exception as e:
                    print(f"✗ Ошибка при скачивании {sound_url}: {e}")
                    continue

            # Создаем файл аннотации
            if annotation_data:
                create_annotation_file(annotation_file, annotation_data)
                print(f"\nУспешно скачано {len(annotation_data)} звуков")
                print(f"Файлы сохранены в: {download_dir}")
                print(f"Аннотация создана: {annotation_file}")
            else:
                print("Не удалось скачать ни одного звука")

        except Exception as e:
            print(f"Общая ошибка при скачивании: {e}")

