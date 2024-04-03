from flask import Flask, render_template, request, redirect, url_for
import plotly.graph_objs as go
import numpy as np

app = Flask(__name__)

# Dados iniciais para o fluxo de caixa
transacoes = {'Receitas': [], 'Despesas': [], 'Lucro': []}

def gerar_grafico():
    meses = list(range(1, len(transacoes['Receitas']) + 1))

    # Criar o gráfico de barras para receitas e despesas
    receitas = go.Bar(
        x=meses,
        y=transacoes['Receitas'],
        name='Receitas',
        marker=dict(color='rgb(65, 158, 118)')
    )
    despesas = go.Bar(
        x=meses,
        y=transacoes['Despesas'],
        name='Despesas',
        marker=dict(color='rgb(219, 64, 82)')
    )

    # Criar o gráfico de linhas para o lucro
    lucro = go.Scatter(
        x=meses,
        y=transacoes['Lucro'],
        mode='lines+markers',
        name='Lucro',
        line=dict(color='rgb(47, 109, 182)')
    )

    # Layout do gráfico
    layout = go.Layout(
        title='Fluxo de Caixa Detalhado',
        xaxis=dict(title='Meses'),
        yaxis=dict(title='Valor (R$)'),
        legend=dict(x=0, y=1.0),
        plot_bgcolor='rgb(243, 243, 243)',
        paper_bgcolor='rgb(243, 243, 243)',
        bargap=0.15
    )

    # Criar a figura e adicionar os gráficos
    fig = go.Figure(data=[receitas, despesas, lucro], layout=layout)

    # Converter a figura para HTML
    grafico_html = fig.to_html(full_html=False)

    return grafico_html

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tipo = request.form['tipo']
        valor = float(request.form['valor'])
        parcela = request.form.get('parcela', False)

        if tipo == 'entrada':
            transacoes['Receitas'].append(valor)
        elif tipo == 'saida':
            if parcela:
                transacoes['Despesas'] += [valor] * len(transacoes['Receitas'])
            else:
                transacoes['Despesas'].append(valor)
        
        transacoes['Lucro'] = [receita - despesa for receita, despesa in zip(transacoes['Receitas'], transacoes['Despesas'])]

        return redirect(url_for('index'))

    # Gerar gráfico do fluxo de caixa
    grafico_html = gerar_grafico()
    return render_template('index.html', grafico=grafico_html)

if __name__ == "__main__":
    app.run(debug=True, threaded=True, use_reloader=False)
