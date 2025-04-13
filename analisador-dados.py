import pandas as pd
import matplotlib.pyplot as plt



def carregar_dados(caminho_arquivo):
    try:
        if caminho_arquivo.endswith('.csv'):
            dados = pd.read_csv(caminho_arquivo)
        elif caminho_arquivo.endswith('.json'):
            dados = pd.read_json(caminho_arquivo)
        else:
            raise ValueError("Formato de arquivo não suportado. Use CSV ou JSON.")
        
        # Imprimir os nomes das colunas para verificar se há problemas
        print(f"\nNomes das colunas carregadas: {dados.columns.tolist()}")

        return dados
    except Exception as erro:
        print(f"Erro ao carregar dados: {erro}")
        return None



def exibir_resumo_estatistico(dados):
    print("\nResumo estatístico dos dados:")
    print(dados.describe(include='all'))


def exibir_informacoes_gerais(dados):
    print(f"\nQuantidade de registros carregados: {len(dados)}")

    if 'Gender' in dados.columns:
        print("\nDistribuição por gênero:")
        print(dados['Gender'].value_counts())
    else:
        print("\nColuna 'Gender' não encontrada nos dados.")

    if 'Parent_Education_Level' in dados.columns:
        faltantes = dados['Parent_Education_Level'].isna().sum()
        print(f"\nRegistros sem informação sobre a educação dos pais: {faltantes}")
    else:
        print("\nColuna 'Parent_Education_Level' não encontrada nos dados.")


def limpar_e_processar_dados(dados):
    if 'Parent_Education_Level' in dados.columns:
        dados = dados.dropna(subset=['Parent_Education_Level'])

    if 'Attendance (%)' in dados.columns:
        mediana_attendance = dados['Attendance (%)'].median()
        dados['Attendance (%)'].fillna(mediana_attendance, inplace=True)
        print(f"\nMediana de Attendance (%) usada para preenchimento: {mediana_attendance}")
        print(f"Somatório de Attendance (%) após preenchimento: {dados['Attendance (%)'].sum()}")
    else:
        print("\nColuna 'Attendance (%)' não encontrada nos dados.")

    return dados


def estatisticas_coluna(dados):
    print("\nColunas disponíveis:")
    print(list(dados.columns))

    coluna = input("\nDigite o nome da coluna para ver estatísticas: ").strip()

    colunas_validas = {c.lower(): c for c in dados.columns}
    coluna_key = coluna.lower()

    if coluna_key not in colunas_validas:
        print("Coluna não encontrada.")
        return

    coluna = colunas_validas[coluna_key]

    if not pd.api.types.is_numeric_dtype(dados[coluna]):
        print("A coluna selecionada não contém valores numéricos.")
        return

    media = dados[coluna].mean()
    mediana = dados[coluna].median()
    moda = dados[coluna].mode()
    desvio = dados[coluna].std()

    print(f"\nEstatísticas da coluna '{coluna}':")
    print(f"Média: {media}")
    print(f"Mediana: {mediana}")
    print(f"Moda: {moda.tolist()}")
    print(f"Desvio padrão: {desvio}")


def gerar_graficos(dados):
    # Gráfico de dispersão: horas de sono vs nota final
    if 'Sleep_Hours_per_Night' in dados.columns and 'Final_Score' in dados.columns:
        plt.figure(figsize=(8, 5))
        plt.scatter(dados['Sleep_Hours_per_Night'], dados['Final_Score'], alpha=0.7, color='blue')
        plt.title("Horas de Sono vs Nota Final")
        plt.xlabel("Horas de Sono")
        plt.ylabel("Nota Final")
        plt.grid(True)
        plt.show()
    else:
        print("\nColunas 'Sleep_Hours_per_Night' ou 'Final_Score' não encontradas para o gráfico de dispersão.")

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
    else:
        print("\nColunas 'Age' ou 'Midterm_Score' não encontradas para o gráfico de barras.")

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
    else:
        print("\nColuna 'Age' não encontrada para o gráfico de pizza.")


def main():
    caminho = input("Digite o caminho do arquivo CSV ou JSON: ")
    dados = carregar_dados(caminho)

    if dados is not None:
        print("\nDados carregados com sucesso!\n")
        print(dados.head())
        exibir_resumo_estatistico(dados)
        exibir_informacoes_gerais(dados)

        dados = limpar_e_processar_dados(dados)

        estatisticas_coluna(dados)

        gerar_graficos(dados)

    else:
        print("Falha ao carregar os dados.")


if __name__ == "__main__":
    main()
