import threading
import matplotlib.pyplot as plt

# Defina a função para criar o gráfico
def criar_grafico():
    plt.figure(figsize=(10, 6))
    # Coloque aqui o código para criar o gráfico
    plt.plot([1, 2, 3], [4, 5, 6])
    plt.title('Meu Gráfico')
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.show()

# Execute a função em uma nova thread
thread = threading.Thread(target=criar_grafico)
thread.start()
