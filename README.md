
# Gerador de Relatório de Acesso

Este projeto é um aplicativo de interface gráfica para gerar relatórios de acesso a partir de arquivos de log. Ele lê arquivos de log de uma pasta especificada, processa os logs e gera relatórios em formato Excel.

## Funcionalidades

- Leitura de arquivos de log.
- Processamento de logs para extrair informações de data, URL e nome do arquivo.
- Geração de relatórios de acesso diário em formato Excel.
- Geração de contagem de acessos por página em formato Excel.

## Requisitos

### Dependências

Para executar o script Python, você precisará instalar as seguintes bibliotecas:

- pandas
- matplotlib
- reportlab

Você pode instalar todas as dependências usando o comando abaixo:

```sh
pip install pandas matplotlib reportlab
```

### Dependências para criação do executável

Para empacotar o script em um executável (.exe), você precisará do PyInstaller:

```sh
pip install pyinstaller
```

## Como Usar

### Execução do Script Python

1. Clone este repositório ou baixe os arquivos do projeto.
2. Instale as dependências usando o comando mencionado acima.
3. Execute o script Python:

```sh
python gerador_relatorio.py
```

### Criação do Executável

1. Certifique-se de que todas as dependências estejam instaladas.
2. Execute o PyInstaller para criar o executável:

```sh
pyinstaller --onefile --windowed gerador_relatorio.py
```

3. O executável será gerado na pasta `dist`.

### Distribuição

Você pode distribuir o arquivo executável gerado na pasta `dist` para os usuários finais. Eles não precisarão ter Python ou quaisquer bibliotecas instaladas para executar o aplicativo.

## Estrutura do Projeto

```
gerador_relatorio/
│
├── gerador_relatorio.py                # Script principal do projeto
├── README.md                           # Este arquivo README
├── dist/
├──├── gerador de relatorio com logs    #arquivo exe do programa
```