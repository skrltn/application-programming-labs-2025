"""
Модуль для загрузки, обработки и сохранения аудиофайлов.
"""

import numpy as np
import soundfile as sf
from typing import Tuple, Optional


class AudioProcessor:
    """Класс для обработки аудиофайлов."""
    
    def __init__(self, file_path: str) -> None:
        """
        Инициализация AudioProcessor.
        
        Args:
            file_path: Путь к аудиофайлу
        """
        self.file_path = file_path
        self.data: Optional[np.ndarray] = None
        self.samplerate: Optional[int] = None
        
    def load_audio(self) -> Tuple[np.ndarray, int]:
        """
        Загружает аудиофайл.
        
        Returns:
            Кортеж (аудиоданные, частота дискретизации)
            
        Raises:
            FileNotFoundError: Если файл не найден
            Exception: При других ошибках загрузки
        """
        try:
            self.data, self.samplerate = sf.read(self.file_path)
            return self.data, self.samplerate
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Файл не найден: {self.file_path}") from e
        except Exception as e:
            raise Exception(f"Ошибка загрузки файла: {e}") from e
    
    def crop_audio(self, start_time: float, end_time: float) -> np.ndarray:
        """
        Обрезает аудио в заданном временном диапазоне.
        
        Args:
            start_time: Начало обрезки в секундах
            end_time: Конец обрезки в секундах
            
        Returns:
            Обрезанные аудиоданные
            
        Raises:
            ValueError: Если аудио не загружено или диапазон некорректен
        """
        if self.data is None or self.samplerate is None:
            raise ValueError("Аудио не загружено")
        
        start_sample = int(start_time * self.samplerate)
        end_sample = int(end_time * self.samplerate)
        
        start_sample = max(0, start_sample)
        end_sample = min(len(self.data), end_sample)
        
        if start_sample >= end_sample:
            raise ValueError("Некорректный диапазон")
        
        return self.data[start_sample:end_sample]
    
    def save_audio(self, output_path: str, data: np.ndarray) -> None:
        """
        Сохраняет аудиоданные в файл.
        
        Args:
            output_path: Путь для сохранения файла
            data: Аудиоданные для сохранения
            
        Raises:
            Exception: При ошибке сохранения
        """
        try:
            sf.write(output_path, data, self.samplerate)
        except Exception as e:
            raise Exception(f"Ошибка сохранения файла: {e}") from e
