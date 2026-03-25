import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ==========================================
# 1. PREPARAÇÃO DOS DADOS (ETL Básico)
# ==========================================
# Carregando o arquivo
df = pd.read_csv("Questionário Cultural (respostas) - Respostas ao formulário 1.csv")

# Limpeza dos nomes das colunas
df.columns = [col.strip() for col in df.columns]

# Isolando o público-alvo (apenas quem assistiu)
df_watched = df[df['Você já assistiu ao filme Tropa de Elite?'] == 'Sim'].copy()

# Convertendo textos para números nas colunas de notas
df_watched['Nota geral do filme (0 a 10)'] = pd.to_numeric(df_watched['Nota geral do filme (0 a 10)'], errors='coerce')
df_watched['O quão verídico você acha que o filme é'] = pd.to_numeric(df_watched['O quão verídico você acha que o filme é'], errors='coerce')

# Configurando o estilo visual "Corporate" (Limpo e profissional)
sns.set_theme(style="whitegrid", font_scale=1.1)

# ==========================================
# ANÁLISE 1: TAXA DE APROVAÇÃO MACRO
# ==========================================
plt.figure(figsize=(7, 6))
gostou = df_watched['Gostou do filme?'].value_counts()

# Gráfico de Pizza
plt.pie(gostou, labels=gostou.index, autopct='%1.1f%%', 
        colors=['#28a745', '#dc3545'], startangle=140, 
        textprops={'fontsize': 14, 'color': 'white', 'weight': 'bold'})
plt.title("1. Aprovação Geral da Obra", fontsize=16, fontweight='bold', pad=20)
plt.show()

# ==========================================
# ANÁLISE 2: NÍVEL MÉDIO DE AVALIAÇÃO (DISTRIBUIÇÃO)
# ==========================================
plt.figure(figsize=(10, 5))
media_nota = df_watched['Nota geral do filme (0 a 10)'].mean()

sns.histplot(df_watched['Nota geral do filme (0 a 10)'], bins=10, kde=True, color='#005b96', edgecolor='white')
plt.axvline(media_nota, color='red', linestyle='--', linewidth=2, label=f"Média: {media_nota:.1f}/10")

plt.title("2. Distribuição da Avaliação de Qualidade", fontsize=16, fontweight='bold')
plt.xlabel("Nota (0 a 10)", fontsize=12)
plt.ylabel("Frequência de Espectadores", fontsize=12)
plt.legend()
plt.show()

# ==========================================
# ANÁLISE 3: O IMPACTO DO REALISMO NO SUCESSO DO FILME
# ==========================================
# Responde à pergunta: "Quem acha mais real tende a gostar mais?"
plt.figure(figsize=(10, 6))
sns.regplot(data=df_watched, x='O quão verídico você acha que o filme é', y='Nota geral do filme (0 a 10)', 
            scatter_kws={'alpha': 0.6, 's': 100, 'color': '#005b96'}, 
            line_kws={'color': '#d9534f', 'linewidth': 3})

plt.title("3. Correlação: Realismo Percebido vs. Nota Atribuída", fontsize=16, fontweight='bold')
plt.xlabel("Nível de Realismo Percebido (0 a 10)", fontsize=12)
plt.ylabel("Nota Geral do Filme (0 a 10)", fontsize=12)
plt.show()

# ==========================================
# ANÁLISE 4: IMERSÃO E IDENTIFICAÇÃO PSICOLÓGICA
# ==========================================
# Vamos analisar em que o público mais se identifica: Personagem, Conflito ou Cenário?
cols_identificacao = [c for c in df_watched.columns if 'Em que medida você se identificou' in c]
df_id = df_watched[cols_identificacao].copy()
df_id.columns = ['Personagens', 'Situações/Conflitos', 'Ambiente/Cenário']

# Transformando os dados para formato "longo" (ideal para gráficos agrupados)
df_id_melt = df_id.melt(var_name='Aspecto da Obra', value_name='Nível de Identificação')
ordem_niveis = ['Nenhuma', 'Pouca', 'Moderada', 'Muita', 'Total']

plt.figure(figsize=(12, 6))
sns.countplot(data=df_id_melt, x='Aspecto da Obra', hue='Nível de Identificação', 
              hue_order=ordem_niveis, palette='Blues')

plt.title("4. Imersão: Com quais elementos a audiência se conecta?", fontsize=16, fontweight='bold')
plt.ylabel("Quantidade de Espectadores")
plt.legend(title='Nível de Identificação', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# ==========================================
# ANÁLISE 5: O QUE O FILME ENTREGA (TEMAS RELEVANTES)
# ==========================================
coluna_temas = 'Quais dos seguintes temas abordados pelo filme você considera mais relevantes? (Selecione até 3)'
# O código abaixo separa os temas que vêm juntos separados por vírgula na mesma célula do CSV
temas = df_watched[coluna_temas].dropna().str.split(', ').explode().str.strip()
top_temas = temas.value_counts().head(5)

plt.figure(figsize=(10, 5))
sns.barplot(x=top_temas.values, y=top_temas.index, palette='viridis')
plt.title("5. Top 5 Temas Mais Impactantes da Obra", fontsize=16, fontweight='bold')
plt.xlabel("Quantidade de Votos (Menções)", fontsize=12)
plt.show()

# ==========================================
# ANÁLISE 6: INTELIGÊNCIA DE MERCADO PARA SEQUÊNCIA
# ==========================================
coluna_sequencia = 'Com base nos temas abordados do filme, numa provável sequência, quais temas devem ser abordados principalmente:'
temas_seq = df_watched[coluna_sequencia].dropna().str.split(', ').explode().str.strip()
top_seq = temas_seq.value_counts().head(5)

plt.figure(figsize=(10, 5))
sns.barplot(x=top_seq.values, y=top_seq.index, palette='magma')
plt.title("6. Demanda de Audiência: O que querem ver em uma Continuação?", fontsize=16, fontweight='bold')
plt.xlabel("Quantidade de Votos", fontsize=12)
plt.show()

print("Relatório de Pesquisa de Mercado gerado com sucesso!")