"""
Основной модуль программы для обрезки аудио.
Использование: python main.py <input> <output> <start> <end>
"""

import argparse
import sys
from audio_processor import AudioProcessor
from audio_visualizer import AudioVisualizer


def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.
    
    Returns:
        Объект с аргументами
    """
    parser = argparse.ArgumentParser(description='Обрезка длины аудио в заданном диапазоне')
    
    parser.add_argument('input', type=str, help='Путь к исходному аудиофайлу')
    parser.add_argument('output', type=str, help='Путь для сохранения результата')
    parser.add_argument('start', type=float, help='Начало диапазона (секунды)')
    parser.add_argument('end', type=float, help='Конец диапазона (секунды)')
    
    parser.add_argument('--no-plot', action='store_true', help='Не показывать график')
    
    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> bool:
    """
    Проверяет корректность аргументов.
    
    Args:
        args: Аргументы командной строки
        
    Returns:
        True если аргументы корректны, иначе False
    """
    if args.start < 0:
        print("Ошибка: время начала не может быть отрицательным")
        return False
    
    if args.end <= args.start:
        print("Ошибка: время конца должно быть больше времени начала")
        return False
    
    return True


def main() -> None:
    """
    Основная функция программы.
    Выполняет загрузку, обрезку, визуализацию и сохранение аудио.
    """
    args = parse_arguments()
    
    if not validate_arguments(args):
        sys.exit(1)
    
    processor = AudioProcessor(args.input)
    visualizer = AudioVisualizer()
    
    try:
        # Загрузка аудио
        original_data, samplerate = processor.load_audio()
        
        # Вывод информации об исходном файле
        print(f"Размер аудио: {original_data.shape}")
        duration = len(original_data) / samplerate
        print(f"Длительность: {duration:.2f} секунд")
        
        # Обрезка аудио
        print(f"Диапазон обрезки: {args.start} - {args.end} секунд")
        cropped_data = processor.crop_audio(args.start, args.end)
        
        # Вывод информации о результате
        cropped_duration = len(cropped_data) / samplerate
        print(f"Длительность после обрезки: {cropped_duration:.2f} секунд")
        
        # Визуализация
        visualizer.plot_audio_comparison(
            original_data=original_data,
            cropped_data=cropped_data,
            samplerate=samplerate,
            start_time=args.start,
            end_time=args.end,
            show_plot=not args.no_plot
        )
        
        visualizer.save_plot('audio_comparison.png')
        print(f"График сохранен в: audio_comparison.png")
        
        # Сохранение результата
        processor.save_audio(args.output, cropped_data)
        print(f"Результат сохранен в: {args.output}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

#pip install -r requirements.txt
#python main.py animal_sound_37.mp3 cropped_audio.mp3 5.0 10.0