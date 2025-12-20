"""
Главное окно приложения для просмотра аудиофайлов с звуками животных.
Вариант 19.
"""

import sys
import os
from typing import Optional
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QProgressBar
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QIcon

from iterator import SoundFileIterator


class AudioPlayer(QObject):
    """Класс для управления воспроизведением аудио."""
    
    duration_changed = pyqtSignal(int)
    position_changed = pyqtSignal(int)
    state_changed = pyqtSignal(QMediaPlayer.State)
    
    def __init__(self, parent: Optional[QObject] = None) -> None:
        """
        Инициализация аудиоплеера.
        
        Args:
            parent: Родительский объект
        """
        super().__init__(parent)
        self._player = QMediaPlayer()
        self._setup_connections()
        
    def _setup_connections(self) -> None:
        """Настройка сигналов медиаплеера."""
        self._player.durationChanged.connect(self._on_duration_changed)
        self._player.positionChanged.connect(self._on_position_changed)
        self._player.stateChanged.connect(self._on_state_changed)
    
    def _on_duration_changed(self, duration: int) -> None:
        """Обработчик изменения длительности трека."""
        self.duration_changed.emit(duration)
    
    def _on_position_changed(self, position: int) -> None:
        """Обработчик изменения позиции воспроизведения."""
        self.position_changed.emit(position)
    
    def _on_state_changed(self, state: QMediaPlayer.State) -> None:
        """Обработчик изменения состояния плеера."""
        self.state_changed.emit(state)
    
    def load_file(self, file_path: str) -> None:
        """
        Загрузка аудиофайла.
        
        Args:
            file_path: Путь к аудиофайлу
        """
        url = QUrl.fromLocalFile(file_path)
        content = QMediaContent(url)
        self._player.setMedia(content)
    
    def play(self) -> None:
        """Начать воспроизведение."""
        self._player.play()
    
    def pause(self) -> None:
        """Приостановить воспроизведение."""
        self._player.pause()
    
    def stop(self) -> None:
        """Остановить воспроизведение."""
        self._player.stop()
    
    def set_position(self, position: int) -> None:
        """
        Установить позицию воспроизведения.
        
        Args:
            position: Позиция в миллисекундах
        """
        self._player.setPosition(position)
    
    def state(self) -> QMediaPlayer.State:
        """
        Получить текущее состояние плеера.
        
        Returns:
            Состояние плеера
        """
        return self._player.state()
    
    def duration(self) -> int:
        """
        Получить длительность текущего трека.
        
        Returns:
            Длительность в миллисекундах
        """
        return self._player.duration()


class MainWindow(QMainWindow):
    """Главное окно приложения."""
    
    def __init__(self) -> None:
        """Инициализация главного окна."""
        super().__init__()
        self._iterator: Optional[SoundFileIterator] = None
        self._current_index: int = 0
        self._total_files: int = 0
        self._audio_player = AudioPlayer()
        
        self._setup_ui()
        self._setup_connections()
        
    def _setup_ui(self) -> None:
        """Настройка пользовательского интерфейса."""
        self.setWindowTitle("Просмотр звуков животных")
        self.setGeometry(100, 100, 600, 400)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Панель управления файлами
        file_panel = QHBoxLayout()
        
        self._select_file_btn = QPushButton("Выбрать файл аннотации")
        self._select_file_btn.setFixedHeight(40)
        file_panel.addWidget(self._select_file_btn)
        
        self._file_label = QLabel("Файл не выбран")
        self._file_label.setFixedHeight(40)
        file_panel.addWidget(self._file_label)
        
        main_layout.addLayout(file_panel)
        
        # Информация о текущем файле
        info_layout = QVBoxLayout()
        
        self._title_label = QLabel("Название: -")
        self._title_label.setFixedHeight(30)
        info_layout.addWidget(self._title_label)
        
        self._duration_label = QLabel("Длительность: -")
        self._duration_label.setFixedHeight(30)
        info_layout.addWidget(self._duration_label)
        
        main_layout.addLayout(info_layout)
        
        # Прогресс воспроизведения
        self._progress_bar = QProgressBar()
        self._progress_bar.setFixedHeight(20)
        main_layout.addWidget(self._progress_bar)
        
        # Панель управления воспроизведением
        control_panel = QHBoxLayout()
        
        self._prev_btn = QPushButton("Предыдущий")
        self._prev_btn.setFixedHeight(40)
        self._prev_btn.setEnabled(False)
        control_panel.addWidget(self._prev_btn)
        
        self._play_btn = QPushButton("▶ Воспроизвести")
        self._play_btn.setFixedHeight(40)
        self._play_btn.setEnabled(False)
        control_panel.addWidget(self._play_btn)
        
        self._stop_btn = QPushButton("⏹ Остановить")
        self._stop_btn.setFixedHeight(40)
        self._stop_btn.setEnabled(False)
        control_panel.addWidget(self._stop_btn)
        
        self._next_btn = QPushButton("Следующий")
        self._next_btn.setFixedHeight(40)
        self._next_btn.setEnabled(False)
        control_panel.addWidget(self._next_btn)
        
        main_layout.addLayout(control_panel)
        
        # Статус
        self._status_label = QLabel("Готов к работе")
        self._status_label.setFixedHeight(30)
        main_layout.addWidget(self._status_label)
        
    def _setup_connections(self) -> None:
        """Настройка сигналов и слотов."""
        # Кнопки файлов
        self._select_file_btn.clicked.connect(self._select_annotation_file)
        
        # Кнопки управления
        self._prev_btn.clicked.connect(self._play_previous)
        self._play_btn.clicked.connect(self._toggle_playback)
        self._stop_btn.clicked.connect(self._audio_player.stop)
        self._next_btn.clicked.connect(self._play_next)
        
        # Сигналы аудиоплеера
        self._audio_player.duration_changed.connect(self._update_duration)
        self._audio_player.position_changed.connect(self._update_position)
        self._audio_player.state_changed.connect(self._update_playback_state)
        
    def _select_annotation_file(self) -> None:
        """Выбор файла аннотации."""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Выберите файл аннотации",
                "",
                "CSV файлы (*.csv);;Все файлы (*)"
            )
            
            if file_path:
                self._load_annotation_file(file_path)
                
        except Exception as e:
            self._show_error(f"Ошибка при выборе файла: {str(e)}")
    
    def _load_annotation_file(self, file_path: str) -> None:
        """
        Загрузка файла аннотации и инициализация итератора.
        
        Args:
            file_path: Путь к файлу аннотации
        """
        try:
            self._iterator = SoundFileIterator(file_path)
            self._total_files = len(self._iterator)
            self._current_index = 0
            
            self._file_label.setText(f"Файл: {Path(file_path).name}")
            self._status_label.setText(f"Загружено файлов: {self._total_files}")
            
            # Активируем кнопки управления
            self._prev_btn.setEnabled(self._total_files > 1)
            self._next_btn.setEnabled(self._total_files > 1)
            self._play_btn.setEnabled(self._total_files > 0)
            
            if self._total_files > 0:
                self._load_current_file()
            else:
                self._show_warning("В файле аннотации нет данных")
                
        except Exception as e:
            self._show_error(f"Ошибка при загрузке аннотации: {str(e)}")
    
    def _load_current_file(self) -> None:
        """Загрузка текущего аудиофайла."""
        if not self._iterator or self._total_files == 0:
            return
        
        try:
            # Останавливаем предыдущее воспроизведение
            self._audio_player.stop()
            
            # Получаем текущий файл
            files = list(self._iterator)
            if 0 <= self._current_index < len(files):
                absolute_path, relative_path = files[self._current_index]
                
                # Проверяем существование файла
                if not os.path.exists(absolute_path):
                    self._show_error(f"Файл не найден: {absolute_path}")
                    return
                
                # Загружаем файл в плеер
                self._audio_player.load_file(absolute_path)
                
                # Обновляем интерфейс
                file_name = Path(absolute_path).name
                self._title_label.setText(f"Название: {file_name}")
                self._status_label.setText(
                    f"Файл {self._current_index + 1} из {self._total_files}"
                )
                
        except StopIteration:
            self._current_index = 0
            if self._total_files > 0:
                self._iterator = iter(self._iterator)
                self._load_current_file()
        except Exception as e:
            self._show_error(f"Ошибка при загрузке файла: {str(e)}")
    
    def _play_previous(self) -> None:
        """Воспроизведение предыдущего файла."""
        if self._total_files <= 1:
            return
        
        self._current_index = (self._current_index - 1) % self._total_files
        self._load_current_file()
    
    def _play_next(self) -> None:
        """Воспроизведение следующего файла."""
        if self._total_files <= 1:
            return
        
        self._current_index = (self._current_index + 1) % self._total_files
        self._load_current_file()
    
    def _toggle_playback(self) -> None:
        """Переключение между воспроизведением и паузой."""
        current_state = self._audio_player.state()
        
        if current_state == QMediaPlayer.PlayingState:
            self._audio_player.pause()
        else:
            self._audio_player.play()
    
    def _update_duration(self, duration: int) -> None:
        """
        Обновление информации о длительности трека.
        
        Args:
            duration: Длительность в миллисекундах
        """
        if duration > 0:
            minutes = duration // 60000
            seconds = (duration % 60000) // 1000
            self._duration_label.setText(f"Длительность: {minutes}:{seconds:02d}")
            self._progress_bar.setMaximum(duration)
        else:
            self._duration_label.setText("Длительность: -")
            self._progress_bar.setMaximum(100)
    
    def _update_position(self, position: int) -> None:
        """
        Обновление позиции прогресс-бара.
        
        Args:
            position: Текущая позиция в миллисекундах
        """
        self._progress_bar.setValue(position)
    
    def _update_playback_state(self, state: QMediaPlayer.State) -> None:
        """
        Обновление состояния кнопок управления воспроизведением.
        
        Args:
            state: Состояние медиаплеера
        """
        if state == QMediaPlayer.PlayingState:
            self._play_btn.setText("⏸ Пауза")
            self._stop_btn.setEnabled(True)
        else:
            self._play_btn.setText("▶ Воспроизвести")
            self._stop_btn.setEnabled(state != QMediaPlayer.StoppedState)
    
    def _show_error(self, message: str) -> None:
        """
        Показать сообщение об ошибке.
        
        Args:
            message: Текст сообщения
        """
        QMessageBox.critical(self, "Ошибка", message)
        self._status_label.setText(f"Ошибка: {message[:50]}...")
    
    def _show_warning(self, message: str) -> None:
        """
        Показать предупреждение.
        
        Args:
            message: Текст сообщения
        """
        QMessageBox.warning(self, "Предупреждение", message)
        self._status_label.setText(f"Предупреждение: {message[:50]}...")
    
    def closeEvent(self, event) -> None:
        """Обработчик закрытия окна."""
        self._audio_player.stop()
        event.accept()


def main() -> None:
    """
    Основная функция приложения.
    Создает и запускает главное окно.
    """
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')  # Современный стиль
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()