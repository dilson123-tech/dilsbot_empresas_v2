const form = document.getElementById('chatForm');
const respostaDiv = document.getElementById('resposta');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const mensagem = document.getElementById('mensagem').value;

  respostaDiv.innerHTML = "<em>🤖 Pensando na melhor resposta para sua empresa...</em>";

  try {
    const resposta = await fetch('https://dilsbot-backend-production.up.railway.app/pergunta', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ mensagem: mensagem }), // ← ESSENCIAL!
    });

    const data = await resposta.json();
    respostaDiv.innerHTML = `<strong>Resposta:</strong><br>${data.resposta || data.erro}`;
  } catch (error) {
    respostaDiv.innerHTML = "❌ Erro ao conectar com a IA.";
  }
});
