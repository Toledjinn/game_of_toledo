# Game of Toledo

## 📜 Descrição

**Game of Toledo** é um jogo de plataforma 2D de corrida infinita criado em Python com a biblioteca Pygame Zero. O jogador controla um cavaleiro que deve pular entre plataformas geradas proceduralmente, desviando de inimigos perigosos que patrulham a área. O objetivo é sobreviver e percorrer a maior distância.

## ✨ Funcionalidades

  * **Geração Procedural de Níveis:** O mundo do jogo é infinito e gerado dinamicamente, garantindo que cada partida seja única.
  * **Animações de Sprite Detalhadas:** Animações fluidas para o herói e inimigos, incluindo estados de "parado" (idle), "correndo" e "pulando".
  * **Menu Principal Completo:** Um menu inicial com opções para "Iniciar Jogo", "Ligar/Desligar Música e Sons" e "Sair".
  * **Sistema de Som e Música:** Música de fundo para imersão e efeitos sonoros para as ações do jogador.
  * **Inimigos com IA Simples:** Os inimigos patrulham suas plataformas, criando um desafio dinâmico para o jogador.
  * **Sistema de Câmera com Rolagem:** A câmera segue o progresso do jogador, criando a sensação de um mundo contínuo.
  * **Pontuação:** O jogo registra a distância percorrida como pontuação final.

## 🛠️ Tecnologias Utilizadas

  * **Linguagem:** Python 3
  * **Biblioteca:** Pygame Zero (`pgzrun`)
  * **Módulos Nativos:** `random`

## 🚀 Como Executar o Projeto

Para rodar o jogo em sua máquina local, siga os passos abaixo:

1.  **Clone este repositório:**

    ```bash
    git clone https://github.com/Toledjinn/game_of_toledo.git
    cd game_of_toledo
    ```

2.  **Certifique-se de ter o Python instalado.** Este projeto foi desenvolvido com Python 3.13.7

3.  **Instale a biblioteca Pygame Zero:**

    ```bash
    pip install pgzero
    ```

4. **Execute o jogo:**

    ```bash
    pgzrun main.py
    ```

## 🎮 Controles

  * **Seta Esquerda / Seta Direita:** Mover o personagem.
  * **Barra de Espaço / Seta para Cima:** Pular.
  * **Mouse:** Navegar e clicar nos botões do menu.
