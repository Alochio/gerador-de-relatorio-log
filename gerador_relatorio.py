import os
import pandas as pd
from datetime import datetime
from tkinter import Tk, Button, Label, filedialog, messagebox, StringVar
from tkinter.ttk import Progressbar, Style, Frame

# Função para ler arquivos .log da pasta especificada
def read_log_files(folder_path, progress_var):
    logs = []
    try:
        filenames = [f for f in os.listdir(folder_path) if f.endswith('.log')]
        total_files = len(filenames)
        for i, filename in enumerate(filenames):
            with open(os.path.join(folder_path, filename), 'r') as file:
                logs.extend([(line.strip(), filename) for line in file.readlines()])
            progress_var.set((i + 1) / total_files * 100)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler arquivos de log: {e}")
    return logs

# Função para processar os logs e extrair as informações desejadas
def process_logs(logs, progress_var):
    data = []
    try:
        total_logs = len(logs)
        for i, (line, filename) in enumerate(logs):
            parts = line.split(', ')
            if len(parts) >= 14:
                ip, _, date, time, _, _, _, _, _, _, _, _, method, url, _ = parts
                if url.startswith('/') and url.endswith('.html'):
                    datetime_str = f'{date} {time}'
                    datetime_obj = datetime.strptime(datetime_str, '%m/%d/%Y %H:%M:%S')
                    data.append((datetime_obj, url, filename))
            progress_var.set((i + 1) / total_logs * 100)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar logs: {e}")
    return pd.DataFrame(data, columns=['datetime', 'url', 'filename'])

# Função para gerar o relatório de acesso para cada página por dia e contar acessos por tela
def generate_access_report(df, save_path, progress_var):
    try:
        df['date'] = df['datetime'].dt.date
        report = df.groupby(['date', 'url']).size().unstack(fill_value=0)
        
        # Salvar o relatório em um arquivo Excel com nome 'Relatório_Mensal_De_Logs.xlsx'
        report_file = os.path.join(save_path, 'Relatório_Mensal_De_Logs.xlsx')
        report.to_excel(report_file)
        
        # Contar acessos por tela e ordenar da mais acessada para a menos acessada
        route_usage = df['url'].value_counts().reset_index()
        route_usage.columns = ['url', 'access_count']
        route_usage = route_usage.sort_values(by='access_count', ascending=False)
        
        # Salvar a contagem de acessos em um arquivo Excel com nome 'Relatório_Geral_De_Logs.xlsx'
        access_count_file = os.path.join(save_path, 'Relatório_Geral_De_Logs.xlsx')
        route_usage.to_excel(access_count_file, index=False)
        
        messagebox.showinfo("Sucesso", f'Relatórios gerados: \n{report_file}\n{access_count_file}')
        
        # Exibir resumo do uso das rotas no console
        for route, count in route_usage.values:
            print(f'Rota {route} foi usada {count} vezes')
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
    finally:
        progress_var.set(0)

# Funções para selecionar a pasta e o local de salvamento
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_label.config(text=folder_path)

def select_save_location():
    save_path = filedialog.askdirectory()
    if save_path:
        save_label.config(text=save_path)

def generate_report():
    folder_path = folder_label.cget("text")
    save_path = save_label.cget("text")
    if not folder_path or not save_path:
        messagebox.showwarning("Aviso", "Selecione a pasta dos logs e o local de salvamento.")
        return
    
    progress_var.set(0)
    root.update_idletasks()
    
    logs = read_log_files(folder_path, progress_var)
    df = process_logs(logs, progress_var)
    generate_access_report(df, save_path, progress_var)

# Configuração da interface gráfica
root = Tk()
root.title("Gerador de Relatório de Acesso")

# Estilo da interface
style = Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TFrame", padding=10)
style.configure("TProgressbar", thickness=20)

frame = Frame(root)
frame.pack(padx=10, pady=10)

Label(frame, text="Selecione a pasta com os arquivos de log:").grid(row=0, column=0, sticky="w", pady=5)
folder_label = Label(frame, text="", background="white", width=50, anchor="w", relief="sunken")
folder_label.grid(row=1, column=0, pady=5)
Button(frame, text="Selecionar Pasta", command=select_folder).grid(row=1, column=1, padx=10)

Label(frame, text="Selecione o local de salvamento do relatório:").grid(row=2, column=0, sticky="w", pady=5)
save_label = Label(frame, text="", background="white", width=50, anchor="w", relief="sunken")
save_label.grid(row=3, column=0, pady=5)
Button(frame, text="Selecionar Local", command=select_save_location).grid(row=3, column=1, padx=10)

Button(frame, text="Gerar Relatório", command=generate_report).grid(row=4, columnspan=2, pady=20)

# Adicionando a barra de progresso
progress_var = StringVar()
progress_bar = Progressbar(frame, length=400, variable=progress_var, mode='determinate')
progress_bar.grid(row=5, columnspan=2, pady=10)

root.mainloop()
