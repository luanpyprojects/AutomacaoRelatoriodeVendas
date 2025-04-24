'''
Lê uma planilha Excel/CSV com dados de vendas (ex.: produto, quantidade, valor).
Gera um relatório automático com resumo (ex.: total vendido, produto mais vendido).
Salva o relatório em formato PDF com gráficos (ex.: vendas por produto).
Envia o relatório por e-mail (opcional, para aumentar o valor).

'''

#Passo 1- Importar Bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

#Passo 2- Importar dados
tabela= pd.read_csv('produtos.csv')
print(tabela)

#Passo 3- Calcular resumo
#Calcular Valor Total
total=(tabela['Quantidade']*tabela['Valor']).sum()
print(total)

#Calcular quantidade vendida
qtd_total=tabela['Quantidade'].sum()
print(qtd_total)

#Calcular produto mais vendido
mais_vendidos=tabela.groupby('Produto')['Quantidade'].sum()
mais_vendido=tabela.groupby('Produto')['Quantidade'].sum().idxmax()
print(mais_vendidos.to_string())
print(mais_vendido)

#Calcular quantidade do produto mais vendido
qtd_mais_vendido=tabela.groupby('Produto')['Quantidade'].sum().max()
print(qtd_mais_vendido)

#Calcular média dos valores
media=total/qtd_total
print(round(media,2))


#Passo 4- Gerar relatório com resumo da distribuição
tabela['Valor_Total'] = tabela['Quantidade'] * tabela['Valor']
vendas_por_produto = tabela.groupby('Produto')['Valor_Total'].sum()
print(vendas_por_produto.to_string())
plt.figure(figsize=(8,4))
vendas_por_produto.plot(kind='bar')
plt.title('Vendas por Produto')
plt.xlabel('Produto')
plt.ylabel('Faturamento')
plt.tight_layout()
plt.savefig('gráfico_vendas.png')
plt.close()

#Passo 5- Salvar relatório em formato pdf
pdf= canvas.Canvas('relatorio_vendas.pdf',pagesize=letter)
pdf.setFont('Helvetica',16)
pdf.drawString(1*inch,10*inch,'Relatório de Vendas')
pdf.setFont('Helvetica',12)
pdf.drawString(1*inch,9.5*inch,f'Total Vendido: R${total:.2f}')
pdf.drawString(1*inch,9.0*inch,f'Quantidade de Vendas: {qtd_total} unidades')
pdf.drawString(1*inch,8.5*inch,f'Produto mais vendido: {mais_vendido}')
pdf.drawString(1*inch,8.0*inch,f'Média Faturamento/Qtd: R${media:.2f}')
pdf.drawString(1*inch,7.5*inch,f'Faturamento por produto:')
y=7.0
for produto, valor in vendas_por_produto.items():
    pdf.drawString(1.5*inch,y*inch,f'{produto}: R${valor:.2f}')
    y -=0.3
pdf.drawImage('gráfico_vendas.png',1*inch,2*inch,width=6*inch,height=3*inch)
pdf.save()
print("Relatório salvo como'relatorio_vendas.pdf' ")





