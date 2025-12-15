"""
Модуль для обработки DataFrame и построения графиков.
"""

import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple, List


def sort_by_amplitude(df: pd.DataFrame, ascending: bool = True) -> pd.DataFrame:
    """
    Сортирует DataFrame по колонке минимальной амплитуды.

    Args:
        df (pd.DataFrame): Исходный DataFrame
        ascending (bool): Порядок сортировки (True - по возрастанию)

    Returns:
        pd.DataFrame: Отсортированный DataFrame
    """
    return df.sort_values(by='Минимальная амплитуда', ascending=ascending)


def filter_by_amplitude(df: pd.DataFrame, min_value: float, max_value: float) -> pd.DataFrame:
    """
    Фильтрует DataFrame по диапазону минимальной амплитуды.

    Args:
        df (pd.DataFrame): Исходный DataFrame
        min_value (float): Минимальное значение амплитуды
        max_value (float): Максимальное значение амплитуды

    Returns:
        pd.DataFrame: Отфильтрованный DataFrame
    """
    mask = (df['Минимальная амплитуда'] >= min_value) & (df['Минимальная амплитуда'] <= max_value)
    return df[mask]


def create_amplitude_plot(df: pd.DataFrame, output_path: str = 'amplitude_plot.png') -> None:
    """
    Создает график минимальных амплитуд.

    Args:
        df (pd.DataFrame): DataFrame с данными
        output_path (str): Путь для сохранения графика
    """
    # Сортируем данные для графика
    sorted_df = sort_by_amplitude(df)
    
    # Создаем график
    plt.figure(figsize=(12, 6))
    
    # По оси X - номер аудиофайла в отсортированном списке
    x_values = range(1, len(sorted_df) + 1)
    y_values = sorted_df['Минимальная амплитуда'].values
    
    plt.plot(x_values, y_values, 'b-', linewidth=2, marker='o', markersize=4)
    plt.xlabel('Номер аудиофайла в отсортированном списке', fontsize=12)
    plt.ylabel('Минимальная амплитуда (по модулю)', fontsize=12)
    plt.title('Минимальные амплитуды аудиофайлов', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Сохраняем график
    plt.savefig(output_path, dpi=300)
    print(f"График сохранен в файл: {output_path}")
    
    # Показываем график
    plt.show()


def save_dataframe(df: pd.DataFrame, output_path: str = 'processed_data.csv') -> None:
    """
    Сохраняет DataFrame в CSV файл.

    Args:
        df (pd.DataFrame): DataFrame для сохранения
        output_path (str): Путь для сохранения файла
    """
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"DataFrame сохранен в файл: {output_path}")