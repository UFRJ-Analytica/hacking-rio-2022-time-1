# Turtle Head - 2022
## UFRJ Analytica Time 1 / ODS 14 - Vida na Água / Equipe 57

### Apresentação
Nosso time propõe o desenvolvimento de uma aplicação web para que o usuário conheça as tartarugas da sua regioão. Através dessa atividade lúdica, pretendemos chamar atenção para a causa das tartarugas marinhas e os impactos da ação do ser humano na vida marinha. Afinal, tu te tornas eternamente responsável pelo que cativas.

### O Produto
Nossa aplicação web, desenvolvida exclusivamente com *software* de código aberto e destinada a utilização por celulares, permite que o usuário cadastre tartarugas marinhas que encontrar, realizando o upload de uma foto. A aplicação reconhece automaticamente a localização do usuário e, através de um software de identificação de contorno, identifica se a tartaruga já foi cadastrada. Sendo assim, é possível que os usuários acompanhem as jornadas de diversas tartarugas que viajam pelo mundo inteiro.


## Informações Adicionais

### Integrantes
* [Maria Luiza Wuillaume](https://github.com/MariaLuizaCw) é graduanda em Engenharia de Computação e Informação na Universidade Federal do Rio de Janeiro (UFRJ) e é desenvolvedora na equipe de ciência de dados da UFRJ, a [UFRJ Analytica](https://analytica.ufrj.br).
* [Matheus Abrantes](https://github.com/mattgouvea) é graduando em Ciência da Computação na Universidade Federal do Rio de Janeiro (UFRJ) e é competidor na equipe de ciência de dados da UFRJ, a [UFRJ Analytica](https://analytica.ufrj.br)
* [Tiago Silva](https://github.com/pdstiago) é graduando em Ciência da Computação na Universidade Federal do Rio de Janeiro (UFRJ) e é competidor na equipe de ciência de dados da UFRJ, a [UFRJ Analytica](https://analytica.ufrj.br).
* [Yasmin Forestti](https://github.com/YasminForestti) é graduanda em Engenharia de Computação e Informação na Universidade Federal do Rio de Janeiro (UFRJ) e é competidora na equipe de ciência de dados da UFRJ, a [UFRJ Analytica](https://analytica.ufrj.br).
* [Vinicius Lettieri](https://github.com/viniciuslettieri) é graduando em Ciência da Computação na Universidade Federal do Rio de Janeiro (UFRJ) e é competidor na equipe de ciência de dados da UFRJ, a [UFRJ Analytica](https://analytica.ufrj.br).

### Bibliotecas e *Frameworks*
Para o front-end utilizamos a linguagem JavaScript e o framework Vue.js. A ferramenta de prototipagem Figma também foi utilizada para esquematizar o design da nossa interface.

Nosso back-end foi desenvolvido em Python sobre o framework Flask e utiliza a ferramenta SQLAlchemy para a criação do banco de dados em Postgres. Para facilitar o gerenciamento de todas as bibliotecas e versões, utilizamos a ferramenta de containerização Docker.

Os algoritmos de identificação de contorno para reconhecimento das tartarugas foram validados nos notebooks e, em seguida, transferidos para o back-end da aplicação.

### Como executar este projeto?
Por padrão, os serviços de back-end, front-end e banco de dados são alocados no localhost, porta: 5000, 3000, 5432 respectivamente.
#### Lista de comandos:
- Primeira vez executando o projeto:``docker compose up --build``
Observação: o arrquivo example.env deve ser renomeado para .env
- Execuções seguintes:``docker compose up -d``
- Fechar o projeto:``docker compose down``

