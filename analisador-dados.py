import pandas as pd
import matplotlib.pyplot as plt
import logging

# Configuração básica do logging
logging.basicConfig(
    filename='dados_processados.log',  # Nome do arquivo de log
    level=logging.INFO,  # O nível de log (INFO, DEBUG, ERROR, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato das mensagens
)



def carregar_dados(caminho_arquivo):
    try:
        logging.info(f"Tentando carregar o arquivo: {caminho_arquivo}")
        if caminho_arquivo.endswith('.csv'):
            dados = pd.read_csv(caminho_arquivo)
            logging.info(f"Arquivo CSV {caminho_arquivo} carregado com sucesso.")
        elif caminho_arquivo.endswith('.json'):
            dados = pd.read_json(caminho_arquivo)
            logging.info(f"Arquivo JSON {caminho_arquivo} carregado com sucesso.")
        else:
            raise ValueError("Formato de arquivo não suportado. Use CSV ou JSON.")
        return dados
    except Exception as erro:
        logging.error(f"Erro ao carregar dados do arquivo {caminho_arquivo}: {erro}")
        print(f"Erro ao carregar dados: {erro}")
        return None

def exibir_resumo_estatistico(dados):
    logging.info("Exibindo resumo estatístico dos dados.")
    print("\nResumo estatístico dos dados:")
    print(dados.describe(include='all'))

def exibir_informacoes_gerais(dados):
    logging.info(f"Quantidade de registros carregados: {len(dados)}")
    print(f"\nQuantidade de registros carregados: {len(dados)}")

    if 'Gender' in dados.columns:
        logging.info(f"Distribuição por gênero: {dados['Gender'].value_counts()}")
        print("\nDistribuição por gênero:")
        print(dados['Gender'].value_counts())
    else:
        logging.warning("Coluna 'Gender' não encontrada nos dados.")

    if 'Parent_Education_Level' in dados.columns:
        faltantes = dados['Parent_Education_Level'].isna().sum()
        logging.info(f"Registros sem informação sobre a educação dos pais: {faltantes}")
        print(f"\nRegistros sem informação sobre a educação dos pais: {faltantes}")
    else:
        logging.warning("Coluna 'Parent_Education_Level' não encontrada nos dados.")

def limpar_e_processar_dados(dados):
    logging.info("Iniciando limpeza e processamento dos dados.")
    if 'Parent_Education_Level' in dados.columns:
        dados = dados.dropna(subset=['Parent_Education_Level']).copy()
        logging.info(f"Removidos registros com valores ausentes na coluna 'Parent_Education_Level'.")
    else:
        logging.warning("Coluna 'Parent_Education_Level' não encontrada para remover valores ausentes.")

    if 'Attendance (%)' in dados.columns:
        mediana_attendance = dados['Attendance (%)'].median()
        dados['Attendance (%)'] = dados['Attendance (%)'].fillna(mediana_attendance)
        logging.info(f"Mediana de 'Attendance (%)' usada para preenchimento: {mediana_attendance}")
        print(f"\nMediana de Attendance usada para preenchimento: {mediana_attendance}")
        print(f"Somatório de Attendance após preenchimento: {dados['Attendance (%)'].sum()}")
    else:
        logging.warning("Coluna 'Attendance (%)' não encontrada para tratamento.")

    return dados

def estatisticas_coluna(dados):
    while True:
        logging.info("Listando colunas disponíveis para estatísticas.")
        print("\nColunas disponíveis:")
        print(list(dados.columns))

        coluna = input("\nDigite o nome da coluna para ver estatísticas ou digite 'sair' para encerrar: ").strip()

        if coluna.lower() == 'sair':
            logging.info("Usuário escolheu sair da consulta de colunas.")
            break

        # Convertendo o nome da coluna para minúsculas para comparação insensível a maiúsculas/minúsculas
        coluna_normalizada = coluna.lower()

        # Tratamento de erro caso a coluna digitada não exista
        colunas_disponiveis = [col.lower() for col in dados.columns]  # Normalizando todas as colunas para minúsculas

        if coluna_normalizada not in colunas_disponiveis:
            logging.warning(f"Coluna '{coluna}' não encontrada nos dados.")
            print("Coluna não encontrada. Tente novamente.")
            continue

        # Obtendo o nome correto da coluna (respeitando o formato original)
        coluna_corrigida = dados.columns[colunas_disponiveis.index(coluna_normalizada)]

        if not pd.api.types.is_numeric_dtype(dados[coluna_corrigida]):
            logging.warning(f"A coluna '{coluna_corrigida}' não contém valores numéricos.")
            print("A coluna selecionada não contém valores numéricos.")
            continue

        # Cálculo das estatísticas
        media = dados[coluna_corrigida].mean()
        mediana = dados[coluna_corrigida].median()
        moda = dados[coluna_corrigida].mode()
        desvio = dados[coluna_corrigida].std()

        logging.info(f"Estatísticas da coluna '{coluna_corrigida}': Média={media}, Mediana={mediana}, Moda={moda.tolist()}, Desvio Padrão={desvio}")
        print(f"\nEstatísticas da coluna '{coluna_corrigida}':")
        print(f"Média: {media}")
        print(f"Mediana: {mediana}")
        print(f"Moda: {moda.tolist()}")
        print(f"Desvio padrão: {desvio}")


def gerar_graficos(dados):
    logging.info("Iniciando geração de gráficos.")
    # Gráfico de dispersão: horas de sono vs nota final
    if 'Sleep_Hours_per_Night' in dados.columns and 'Final_Score' in dados.columns:
        plt.figure(figsize=(8, 5))
        plt.scatter(dados['Sleep_Hours_per_Night'], dados['Final_Score'], alpha=0.7, color='blue')
        plt.title("Horas de Sono vs Nota Final")
        plt.xlabel("Horas de Sono")
        plt.ylabel("Nota Final")
        plt.grid(True)
        plt.show()
        logging.info("Gráfico de dispersão 'Horas de Sono vs Nota Final' gerado.")
    else:
        logging.warning("Colunas 'Sleep_Hours_per_Night' ou 'Final_Score' não encontradas para o gráfico de dispersão.")

    # Gráfico de barras: idade vs média das notas intermediárias
    if 'Age' in dados.columns and 'Midterm_Score' in dados.columns:
        media_por_idade = dados.groupby('Age')['Midterm_Score'].mean()
        plt.figure(figsize=(8, 5))
        media_por_idade.plot(kind='bar', color='green')
        plt.title("Média da Nota Intermediária por Idade")
        plt.xlabel("Idade")
        plt.ylabel("Média da Nota Intermediária")
        plt.xticks(rotation=0)
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()
        logging.info("Gráfico de barras 'Média da Nota Intermediária por Idade' gerado.")
    else:
        logging.warning("Colunas 'Age' ou 'Midterm_Score' não encontradas para o gráfico de barras.")

    # Gráfico de pizza: faixas etárias
    if 'Age' in dados.columns:
        bins = [0, 17, 21, 24, float('inf')]
        labels = ['Até 17', '18 a 21', '22 a 24', '25 ou mais']
        categorias = pd.cut(dados['Age'], bins=bins, labels=labels, right=False)
        distribuicao = categorias.value_counts().sort_index()

        plt.figure(figsize=(6, 6))
        distribuicao.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title("Distribuição por Faixas Etárias")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()
        logging.info("Gráfico de pizza 'Distribuição por Faixas Etárias' gerado.")
    else:
        logging.warning("Coluna 'Age' não encontrada para o gráfico de pizza.")

def main():
    nome_usuario = input("Digite o seu nome: ").strip()  # Solicita o nome do usuário
    logging.info(f"Usuário {nome_usuario} iniciou o programa.")  # Registra o nome no log

    while True:
        caminho = input("Digite o caminho do arquivo CSV ou JSON (ou digite 'sair' para encerrar): ").strip()

        if caminho.lower() == 'sair':  # Se o usuário digitar 'sair', o programa encerra
            print("Saindo do programa...")
            logging.info(f"Usuário {nome_usuario} optou por sair.")
            break

        # Tenta carregar os dados
        dados = carregar_dados(caminho)
        
        if dados is not None:  # Se os dados forem carregados com sucesso, sai do loop
            logging.info("Dados carregados com sucesso!")
            print("\nDados carregados com sucesso!\n")
            print(dados.head())
            exibir_resumo_estatistico(dados)
            exibir_informacoes_gerais(dados)

            dados = limpar_e_processar_dados(dados)

            estatisticas_coluna(dados)

            gerar_graficos(dados)
            break  # Sai do loop após processar os dados com sucesso

        else:
            print("Caminho inválido ou erro ao carregar os dados. Tente novamente.")
            logging.error(f"Falha ao carregar os dados do caminho: {caminho}")



if __name__ == "__main__":
    main()