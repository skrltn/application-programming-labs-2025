"""
Модуль с вспомогательными функциями для работы с данными.
"""

from typing import Optional, Tuple
import pandas as pd


def load_annotation(file_path: str) -> pd.DataFrame:
    """
    Загружает аннотацию из CSV файла.

    Args:
        file_path (str): Путь к CSV файлу с аннотацией

    Returns:
        pd.DataFrame: DataFrame с загруженными данными
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Аннотация успешно загружена. Записей: {len(df)}")
        return df
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
        raise
    except Exception as e:
        print(f"Ошибка при загрузке аннотации: {e}")
        raise


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Переименовывает колонки DataFrame.

    Args:
        df (pd.DataFrame): Исходный DataFrame

    Returns:
        pd.DataFrame: DataFrame с переименованными колонками
    """
    column_mapping = {
        'absolute_path': 'Абсолютный путь к файлу',
        'relative_path': 'Относительный путь к файлу'
    }
    return df.rename(columns=column_mapping)