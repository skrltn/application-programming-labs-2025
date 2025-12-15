"""
Главный модуль программы для обработки аудиоданных.
"""

import pandas as pd
from typing import NoReturn
from utils import load_annotation, rename_columns
from audio_processor import add_min_amplitude_column
from data_processor import sort_by_amplitude, filter_by_amplitude, create_amplitude_plot, save_dataframe


def main() -> None:
    """
    Главная функция программы.
    """
    try:
        # 1. Загрузка аннотации
        df = load_annotation("sound_annotation.csv")
        
        # 2. Переименование колонок
        df = rename_columns(df)
        
        # 3. Добавление колонки с минимальной амплитудой
        df = add_min_amplitude_column(df)
        
        # Удаляем строки с None (ошибки чтения файлов)
        df = df.dropna(subset=['Минимальная амплитуда'])
        
        # 4. Сортировка данных
        sorted_df = sort_by_amplitude(df)
        print("Первые 5 строк отсортированного DataFrame:")
        print(sorted_df[['Абсолютный путь к файлу', 'Минимальная амплитуда']].head())
        
        # 5. Фильтрация данных
        min_val = 0.01
        max_val = 0.1
        filtered_df = filter_by_amplitude(sorted_df, min_val, max_val)
        print(f"Найдено {len(filtered_df)} файлов с амплитудой от {min_val} до {max_val}")
        
        # 6. Построение графика
        create_amplitude_plot(sorted_df, 'audio_amplitudes.png')
        
        # 7. Сохранение данных
        save_dataframe(sorted_df, 'processed_audio_data.csv')
        
        print("Обработка завершена.")
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()