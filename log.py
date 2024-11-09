import logging
import datetime
import json
import os
from dataclasses import dataclass
from typing import Optional, List, Dict
from enum import Enum
import streamlit as st

class LogLevel(Enum):
    """Níveis de log disponíveis no sistema."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    PROGRESS = "PROGRESS"

@dataclass
class LogEntry:
    """Estrutura de dados para uma entrada de log."""
    message: str
    level: LogLevel
    timestamp: datetime.datetime
    details: Optional[Dict] = None
    progress: Optional[float] = None

    def to_dict(self) -> Dict:
        """Converte a entrada de log para dicionário."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.value,
            "message": self.message,
            "details": self.details,
            "progress": self.progress
        }

class StreamlitLogger:
    def __init__(self, log_file_path: Optional[str] = None):
        self._setup_attributes(log_file_path)
        self._ensure_log_directory()
        self._setup_logging()

    def _setup_attributes(self, log_file_path: Optional[str]) -> None:
        """Configura os atributos básicos do logger."""
        self.log_entries: List[LogEntry] = []
        self.log_container = st.empty()
        self.progress_bar = st.empty()
        self.log_file_path = (
            log_file_path or 
            f"logs/install_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

    def _setup_logging(self) -> None:
        """Configura o logger do Python."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger()

    def _ensure_log_directory(self) -> None:
        """Garante que o diretório de logs existe."""
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)

    def log(self, message: str, level: LogLevel, details: Optional[Dict] = None, 
            progress: Optional[float] = None) -> None:
        """
        Método principal para logging. Todos os outros métodos de log utilizam este.
        
        Args:
            message: Mensagem a ser logada
            level: Nível do log
            details: Detalhes adicionais opcional
            progress: Valor de progresso opcional
        """
        entry = LogEntry(
            message=message,
            level=level,
            timestamp=datetime.datetime.now(),
            details=details,
            progress=progress
        )
        
        self.log_entries.append(entry)
        self._update_display()
        self._save_to_file(entry)
        self._log_to_console(entry)

    def _update_display(self) -> None:
        """Atualiza a interface do Streamlit com as entradas de log."""
        display_text = "\n".join(
            f"[{entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {entry.level.value}: {entry.message}"
            for entry in self.log_entries
            if entry.level != LogLevel.PROGRESS
        )
        self.log_container.text_area("Log de Instalação", display_text, height=400)

    def _save_to_file(self, entry: LogEntry) -> None:
        """Salva a entrada de log em arquivo JSON."""
        try:
            with open(self.log_file_path, 'a', encoding='utf-8') as f:
                json.dump(entry.to_dict(), f, ensure_ascii=False)
                f.write('\n')
        except Exception as e:
            self.logger.error(f"Erro ao salvar log: {str(e)}")

    def _log_to_console(self, entry: LogEntry) -> None:
        """Envia o log para o console usando o logger do Python."""
        log_funcs = {
            LogLevel.INFO: self.logger.info,
            LogLevel.WARNING: self.logger.warning,
            LogLevel.ERROR: self.logger.error,
            LogLevel.SUCCESS: lambda msg: self.logger.info(f"SUCCESS: {msg}"),
            LogLevel.PROGRESS: self.logger.info
        }
        log_funcs[entry.level](entry.message)

    # Métodos públicos para diferentes tipos de log
    def info(self, message: str, details: Optional[Dict] = None) -> None:
        """Registra uma mensagem informativa."""
        self.log(message, LogLevel.INFO, details)

    def warning(self, message: str, details: Optional[Dict] = None) -> None:
        """Registra um aviso."""
        self.log(message, LogLevel.WARNING, details)

    def error(self, message: str, details: Optional[Dict] = None) -> None:
        """Registra um erro."""
        self.log(message, LogLevel.ERROR, details)

    def success(self, message: str, details: Optional[Dict] = None) -> None:
        """Registra uma mensagem de sucesso."""
        self.log(message, LogLevel.SUCCESS, details)

    def progress(self, message: str, progress_value: float) -> None:
        """Atualiza a barra de progresso."""
        self.log(message, LogLevel.PROGRESS, progress=progress_value)
        self.progress_bar.progress(progress_value)

    def get_logs(self) -> List[LogEntry]:
        """Retorna todas as entradas de log."""
        return self.log_entries

    def export_logs(self, format: str = 'json') -> str:
        """
        Exporta os logs no formato especificado.
        
        Args:
            format: Formato de exportação ('json' por enquanto)
            
        Returns:
            String com os logs no formato especificado
        """
        if format == 'json':
            return json.dumps([entry.to_dict() for entry in self.log_entries], indent=2)
        return ""

def create_logger(log_file_path: Optional[str] = None) -> StreamlitLogger:
    """
    Função de fábrica para criar uma nova instância do logger.
    
    Args:
        log_file_path: Caminho opcional para o arquivo de log
        
    Returns:
        Nova instância de StreamlitLogger
    """
    return StreamlitLogger(log_file_path)

def create_log_wrapper(logger: StreamlitLogger):
    """
    Cria um wrapper para funções de log existentes.
    
    Args:
        logger: Instância do StreamlitLogger
        
    Returns:
        Função wrapper para logging
    """
    def log_wrapper(message: str, is_progress: bool = False):
        if is_progress:
            try:
                progress_value = float(message.strip('%')) / 100
                logger.progress(message, progress_value)
            except ValueError:
                logger.warning(f"Valor de progresso inválido: {message}")
        else:
            logger.info(message)
    return log_wrapper
