  // Seleciona todos os elementos de gráficos
  const graficos = document.querySelectorAll('.eda-grafico');
  const modal = document.getElementById('modal');
  const modalImg = document.getElementById('modal-img');
  const modalText = document.getElementById('modal-text');
  const span = document.getElementsByClassName('close')[0];

  // Dados de descrição dos gráficos
  const graficoDescricoes = {
      heatmap: "Este gráfico representa a distribuição de acidentes de trânsito em diferentes regiões. As cores indicam a intensidade dos acidentes.",
      linechart: "Este gráfico mostra a evolução dos acidentes ao longo do tempo, permitindo visualizar as tendências mensais.",
      barchart01: "Este gráfico de barras mostra a frequência de acidentes por tipo de colisão, destacando os mais comuns.",
      barchart02: "Este gráfico de barras ilustra os diferentes fatores de risco associados aos acidentes de trânsito.",
      barchart03: "Este gráfico apresenta a distribuição dos acidentes de trânsito por faixa etária dos motoristas envolvidos."
  };

  // Ao clicar em um gráfico, abre o modal com a imagem e descrição
  graficos.forEach(grafico => {
      grafico.addEventListener('click', function() {
          const graphType = this.getAttribute('data-graph'); // Pega o tipo do gráfico
          modal.style.display = 'block';
          modalImg.src = this.querySelector('img').src; // Atualiza a imagem do modal
          if (graficoDescricoes[graphType]) {
              modalText.textContent = graficoDescricoes[graphType]; // Atualiza a descrição se houver
          } else {
              modalText.textContent = "Descrição não disponível."; // Mensagem caso a descrição não seja encontrada
          }
      });
  });

  // Fecha o modal quando o usuário clica no "X"
  span.onclick = function() {
      modal.style.display = 'none';
  }

  // Fecha o modal se o usuário clicar fora da área de conteúdo do modal
  window.onclick = function(event) {
      if (event.target === modal) {
          modal.style.display = 'none';
      }
  }


//   taxa de fatalidade

document.querySelector('.fatalidade-section form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: new URLSearchParams(data)
        });

        const resultado = await response.json();

        if (response.ok) {
            document.querySelector('.resultado').textContent = 
                `Taxa de fatalidade: ${resultado.probabilidade}% (${resultado.fatalidade ? 'Fatal' : 'Não Fatal'})`;
        } else {
            document.querySelector('.resultado').textContent = `Erro: ${resultado.erro}`;
        }
    } catch (err) {
        document.querySelector('.resultado').textContent = `Erro de conexão com o servidor.`;
    }
});


