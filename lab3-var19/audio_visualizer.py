"""
Модуль для визуализации аудиоданных.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional


class AudioVisualizer:
    """Класс для создания графиков аудиоданных."""
    
    def __init__(self) -> None:
        """Инициализация AudioVisualizer."""
        self.fig = None
        
    def plot_audio_comparison(
        self,
        original_data: np.ndarray,
        cropped_data: np.ndarray,
        samplerate: int,
        start_time: float,
        end_time: float,
        show_plot: bool = True
    ) -> Optional[plt.Figure]:
        """
        Создает график сравнения исходного и обрезанного аудио.
        
        Args:
            original_data: Исходные аудиоданные
            cropped_data: Обрезанные аудиоданные
            samplerate: Частота дискретизации
            start_time: Начало диапазона обрезки
            end_time: Конец диапазона обрезки
            show_plot: Показывать график
            
        Returns:
            Объект фигуры matplotlib или None
        """
        time_original = np.arange(len(original_data)) / samplerate
        time_cropped = np.arange(len(cropped_data)) / samplerate
        
        self.fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Исходное аудио
        if len(original_data.shape) == 1:
            ax1.plot(time_original, original_data, 'b', alpha=0.7, linewidth=0.5)
        else:
            ax1.plot(time_original, original_data[:, 0], 'b', alpha=0.7, linewidth=0.5, label='Левый')
            ax1.plot(time_original, original_data[:, 1], 'r', alpha=0.5, linewidth=0.5, label='Правый')
            ax1.legend()
        
        ax1.axvspan(start_time, end_time, alpha=0.3, color='green')
        ax1.set_title('Исходное аудио')
        ax1.set_xlabel('Время (с)')
        ax1.set_ylabel('Амплитуда')
        ax1.grid(True, alpha=0.3)
        
        # Обрезанное аудио
        if len(cropped_data.shape) == 1:
            ax2.plot(time_cropped, cropped_data, 'g', linewidth=0.5)
        else:
            ax2.plot(time_cropped, cropped_data[:, 0], 'darkgreen', linewidth=0.5, label='Левый')
            ax2.plot(time_cropped, cropped_data[:, 1], 'lime', linewidth=0.5, label='Правый')
            ax2.legend()
        
        ax2.set_title('Обрезанное аудио')
        ax2.set_xlabel('Время (с)')
        ax2.set_ylabel('Амплитуда')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        
        return self.fig
    
    def save_plot(self, filename: str) -> None:
        """
        Сохраняет график в файл.
        
        Args:
            filename: Имя файла для сохранения
        """
        if self.fig is not None:
            self.fig.savefig(filename, dpi=100, bbox_inches='tight')