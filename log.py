import streamlit as st
import subprocess

class LogDisplay:
    def __init__(self, log_height=350, log_width=700):
        # Inicializar o estado de sessão do Streamlit para os logs
        if 'log_content' not in st.session_state:
            st.session_state.log_content = []
        if 'progress_content' not in st.session_state:
            st.session_state.progress_content = ''
        
        # Definir estilo visual
        self.log_height = log_height
        self.log_width = log_width
        
        # Elemento de exibição do log
        self.log_display = st.empty()
    
    def add_log_session(self, header):
        """Adiciona um cabeçalho para uma nova sessão de log"""
        st.session_state.log_content.append(f"<span style='color:#ffffff;'>=== {header} ===</span>")
        self.display_logs()

    def update_log(self, message, message_type="INFO", is_progress=False):
        """Atualiza o log com uma nova mensagem, colorida por tipo de mensagem"""
        colors = {
            "INFO": "#14d931",   # Verde
            "OK": "#14d931",     # Verde
            "ERRO": "#d93a3a",   # Vermelho
            "AVISO": "#e5b800"   # Amarelo
        }
        color = colors.get(message_type, "#14d931")
        formatted_message = f"<span style='color:{color};'>[{message_type}] {message}</span>"
        
        if is_progress:
            st.session_state.progress_content = formatted_message
        else:
            st.session_state.log_content.append(formatted_message)
        
        self.display_logs()

    def display_logs(self):
        """Exibe o conteúdo de log no estilo de terminal com rolagem automática"""
        log_content = "<br>".join(st.session_state.log_content)
        full_log_content = log_content + "<br>" + st.session_state.progress_content
        self.log_display.markdown(
            f"""
            <div id="log-container" style="background-color: #121212; color: #14d931; font-family: monospace; 
                         padding: 10px; border-radius: 5px; height: {self.log_height}px; 
                         width: {self.log_width}px; overflow-y: auto; margin-top: 20px;">
                {full_log_content}
            </div>
            <script>
            const logContainer = document.getElementById('log-container');
            logContainer.scrollTop = logContainer.scrollHeight;
            </script>
            """,
            unsafe_allow_html=True
        )

    def run_command(self, command):
        """Executa um comando de shell e atualiza o log conforme o output"""
        self.update_log(f"Iniciando: {command}...", message_type="INFO")
        try:
            with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
                for stdout_line in iter(process.stdout.readline, ""):
                    if stdout_line:
                        # Atualiza o log em tempo real para cada linha de saída
                        self.update_log(stdout_line.strip(), is_progress=False)
                    # Verifica e exibe possíveis erros em stderr
                for stderr_line in iter(process.stderr.readline, ""):
                    if stderr_line:
                        self.update_log(stderr_line.strip(), message_type="ERRO", is_progress=False)
                process.stdout.close()
                process.stderr.close()
                return_code = process.wait()
                if return_code:
                    self.update_log(f"Erro: Código de saída {return_code}", message_type="ERRO")
                else:
                    self.update_log("Finalizado com sucesso.", message_type="OK")
        except Exception as e:
            self.update_log(f"Erro ao executar comando: {e}", message_type="ERRO")
