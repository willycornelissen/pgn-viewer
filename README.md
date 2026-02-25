# Visualizador de Xadrez PGN

Este projeto é uma aplicação desktop leve e intuitiva para visualizar jogos de xadrez armazenados em arquivos no formato PGN (*Portable Game Notation*).

## 🚀 Solução Tecnológica

A aplicação foi desenvolvida utilizando a linguagem **Python 3**, escolhida pela sua robustez no processamento de dados e vasta disponibilidade de bibliotecas especializadas. Os pilares da solução são:

1.  **python-chess**: Uma biblioteca poderosa que lida com toda a lógica das regras do xadrez, validação de movimentos e, crucialmente, o parsing (leitura) de arquivos PGN complexos.
2.  **Pygame**: Utilizado para a interface gráfica (GUI). O Pygame oferece controle total sobre a renderização de quadros, permitindo uma navegação fluida e responsiva entre as jogadas.
3.  **Sistema Híbrido de Renderização**: O código foi projetado para ser resiliente. Ele prioriza o uso de imagens PNG profissionais (se presentes na pasta `assets/`), mas possui um motor de desenho vetorial integrado que gera as peças matematicamente caso os arquivos de imagem estejam ausentes.

## 🛠️ Pré-requisitos

*   Python 3.10 ou superior.
*   Ambiente Linux/WSL (recomendado) ou Windows/macOS.

## 📦 Instalação

1.  **Clone ou baixe** este repositório.
2.  **Crie e ative um ambiente virtual** (recomendado para evitar conflitos):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    # ou
    .\venv\Scripts\activate   # No Windows
    ```
3.  **Instale as dependências**:
    ```bash
    pip install pygame python-chess
    ```

## 🎨 Personalização Visual (Opcional)

Para obter um visual profissional (estilo Lichess/Chess.com), você pode baixar imagens das peças e colocá-las em uma pasta chamada `assets/` no diretório raiz do projeto. O script reconhecerá automaticamente os seguintes nomes:
*   Brancas: `wK.png`, `wQ.png`, `wR.png`, `wB.png`, `wN.png`, `wP.png`
*   Pretas: `bK.png`, `bQ.png`, `bR.png`, `bB.png`, `bN.png`, `bP.png`

## 📖 Documentação do Usuário

### Como Executar
Abra o terminal na pasta do projeto e execute o comando passando o caminho do arquivo PGN que deseja visualizar:

```bash
python pgn_viewer.py caminho/do/seu/arquivo.pgn
```

### Controles de Navegação
Uma vez que a janela do tabuleiro abrir, utilize o teclado para interagir:

*   **Seta para a Direita (→)**: Avança para a próxima jogada do jogo.
*   **Seta para a Esquerda (←)**: Retrocede para a jogada anterior.
*   **Tecla ESC**: Fecha a aplicação.

### Funcionalidades Especiais
*   **Destaque de Movimento**: O tabuleiro destaca automaticamente a casa de origem e a casa de destino do último movimento realizado, facilitando o acompanhamento da partida.
*   **Renderização Dinâmica**: Se você não possuir arquivos de imagem, o sistema desenhará peças estilizadas automaticamente para garantir que você possa estudar suas partidas sem interrupções.
