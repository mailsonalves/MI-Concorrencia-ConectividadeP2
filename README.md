<div align="center" class = "all" >
  <h1>
      Relatório do problema 2: Passcom: Sistema de Venda de Passagens
  </h1>

  <h3>
    Mailson Alves Silva Santos<sup>1</sup>, Matheus Mota Santos<sup>2</sup>
  
  </h3>


  <p>
    Engenharia de Computação – Universidade Estadual de Feira de Santana (UEFS)
    Av. Transnordestina, s/n, Novo Horizonte
    Feira de Santana – BA, Brasil – 44036-900
  </p>

  <center>mailsonalves.new@gmail.com<sup>1</sup></center>
  <center>matheuzwork@gmail.com<sup>2</sup></center>

</div>

#  Introdução
Nos últimos anos, o crescimento exponencial do comércio eletrônico tem impulsionado a transformação digital em diversos setores, incluindo a aviação. As plataformas online se tornaram a principal forma de interação entre clientes e empresas aéreas, proporcionando conveniência, velocidade e preços competitivos. No entanto, com a diversificação de ofertas e a presença de múltiplas companhias aéreas no mercado, torna-se fundamental que os sistemas de compra de passagens sejam capazes de integrar informações de diferentes provedores de forma eficiente e sem sobrecarga para o usuário.

Este relatório tem como objetivo apresentar o desenvolvimento de um sistema distribuído de compra de passagens aéreas, que conecta clientes a três empresas aéreas distintas, facilitando a pesquisa de rotas, comparação de preços e a compra de bilhetes. A solução proposta é baseada em uma arquitetura distribuída, utilizando microserviços e comunicação entre sistemas por meio de APIs RESTful. Para garantir escalabilidade e performance, o sistema foi desenvolvido com a linguagem Python para a implementação de back-end, e a interface do usuário foi construída com React. Além disso, o sistema foi projetado para suportar alta disponibilidade e integridade de dados, mesmo em cenários de grande volume de acessos.

A seguir, detalharemos os aspectos técnicos e operacionais do sistema, além dos desafios enfrentados durante o processo de desenvolvimento e os resultados alcançados.

# Arquitetura da aplicação
A arquitetura do sistema é baseada no cliente-servidor, porém contendo uma comunicação entre servidores. Resumidamente, é como se quando um servidor for comunicar com outro, o remetente da mensagem é como um cliente. A figura 1 mostra como funciona a arquitetura do sistema e como ocorre a comunicação entre o componentes.
<p align="center">Figura 1. Arquitetura do sistema</p>
<div align="center">
<img src="https://github.com/user-attachments/assets/9216cdab-73fa-477c-a3b0-5bb4d9e3c42f" >
</div>
<h3>Banco de Dados</h3>
Foi escolhido o banco de dados relacional PostgreSQL para armazenar as informações do sistema. Cada servidor possui um banco de dados executando isoladamente em seu próprio container Docker. Cada usuário poderá se cadastrar e fazer login apenas a partir do seu servidor de origem, mas podendo visualizar e interagir com os dados dos outros servidores.
<h3>Comunicação entre servidores</h3>
Para gerenciar a lógica e regras de negócio da aplicação foi escolhido o framework FastAPI para o backend do sitema. A utilização do FastApi facilitou a comunicação cliente-servidor e servidor-servidor através das rotas especificadas em portas de rede disitintas. Além disso, o uso do framework facilitou a integração com o front-end da aplicação especificando como as requisições devem ser feitas aos servidores.
<h3>Interface Gráfica</h3>
Para a implementação da interface gráfica do sistema foi utilizado o framework ReactJS. A ideia é oferecer ao usuário final do sitema uma interface clara e intuitiva para proporcionar uma boa experência de compra.
Algumas das principais telas do sistema estão mostradas nas figuras a seguir. A figura 2 mostra  a tela de listagem de voos do sistema sem o usuário estar logado em uma das companhias aéreas.
Já a figura 3 mostra a finalização de compra da passagem.

<p align="center">Figura 2. Tela de pesquisa de passagens </p>
<div align="center">
<img src="https://github.com/user-attachments/assets/8055008e-bfc4-46d2-a871-b700d1fbb1f2" width="700">
</div>
<p align="center">Figura 3. Modal de compra de passagem </p>
<div align="center">
<img src="https://github.com/user-attachments/assets/44b5ac42-fd58-4fff-a02f-f3ac7716b9dd" width="700">
</div>

#  Protocolo de comunicação
A comunicação foi realizada por meio de uma API REST, que recebe e envia dados em formato JSON, adotando o princípio stateless, no qual cada requisição contém todas as informações necessárias para seu processamento. Os endpoints são protegidos por autenticação JWT, exigindo que os usuários estejam autenticados para realizar as seguintes operações: visualizar trechos, comprar passagens, consultar passagens e cancelar passagens. Foram implementados dois conjuntos de rotas: uma para a comunicação entre servidores e outra para a interação entre clientes e servidores. A documentação detalhada da API está disponível mais adiante neste artigo.

# Interface da Aplicação
Falar sobre o rest

# Concorrência Distribuída
O código utiliza uma abordagem de bloqueio pessimista para evitar conflitos quando vários usuários tentam reservar o mesmo voo ou assento ao mesmo tempo. A ideia principal desse bloqueio é garantir que, uma vez iniciado o processo de verificação de capacidade e de disponibilidade de assentos, outros processos que tentem acessar esses mesmos dados sejam temporariamente bloqueados até que a operação em andamento seja finalizada.

No fluxo da compra de passagem, o sistema primeiro verifica se a capacidade do voo permite novas reservas. A aplicação bloqueia momentaneamente o registro do voo para assegurar que apenas uma transação por vez possa atualizar o número de assentos ocupados. Se a capacidade máxima do voo já tiver sido atingida, o sistema interrompe a transação, evitando que o voo ultrapasse o limite de reservas.

Além disso, o bloqueio pessimista é aplicado na verificação de assentos individuais, garantindo que, durante a verificação, apenas uma transação tenha acesso ao registro específico do assento. Assim, se um usuário tentar reservar um assento que já foi atribuído, ele recebe um aviso de que o assento está ocupado. Isso evita que dois usuários reservem o mesmo assento em um mesmo voo.

Por fim, se todo o processo de verificação e reserva é concluído com sucesso, o bloqueio é liberado e o sistema finaliza a operação. Caso contrário, ele interrompe o processo e desfaz qualquer mudança, garantindo que os dados de assentos e voos permaneçam consistentes, mesmo sob alta demanda. 

Esse processo de bloqueio pessimista é fundamental para assegurar que reservas e verificações de disponibilidade ocorram de forma organizada, evitando conflitos e problemas de concorrência em operações de compra de passagens.

# Confiabilidade da solução
Caso um dos servidores fique indisponível, a aplicação não será interrompida para o cliente do servidor em questão. A listagem de voos exibirá apenas os voos disponíveis nos servidores ativos. Se um servidor se desconectar durante o processo de compra de uma passagem disponível nele, será exibida uma mensagem de erro específica (conforme imagem X), com o tratamento necessário para informar o usuário.

Como a passagem comprada é registrada tanto no servidor local quanto no servidor remoto, em caso de falha de conexão com o servidor remoto, serão realizadas até três tentativas de reenvio, caso o código de resposta seja diferente de 200 (sucesso) ou 400 (solicitação inválida). Caso o problema persista, a aplicação fará um rollback, removendo a compra no servidor local para garantir a consistência dos dados.

A disponibilidade e a confiabilidade da aplicação são asseguradas pelo próprio servidor do cliente.

# Avaliação da Solução
Testes foram realizados para analisar o comportamento do sistema em situações de falha em um dos servidores. Foi observado que, quando a operação não exige a participação de todos os servidores, os que permanecem ativos conseguem completar suas tarefas normalmente, atendendo ao requisito de que a falha de um servidor não deve afetar os demais. No entanto, ao tentar reservar uma passagem que depende de trechos gerenciados por todos os três servidores, a operação falha em todos eles, já que não é possível verificar a disponibilidade de assentos em todos os trechos necessários.

As operações que podem ser executadas de forma independente incluem a visualização de trechos, de passagens compradas, o registro e o login. Contudo, se algum servidor estiver fora do ar, os trechos específicos desse servidor não serão exibidos ao cliente, deixando as informações aparentes incompletas. Esse problema é registrado em log no terminal, indicando a falha em um ou mais servidores.

# Documentação do código

# Docker
Devido a necessidade de ter vários containers com serviços diferentes executando, foi usado o Docker Compose para gerenciá-los. Ao todo são 3 containers, sendo um para cada servidor.
Assim, o arquivo docker-compose.yaml une a execução dos contêineres, permitindo o build e execução dos componentes de cada uma das companhias aéreas a partir do comando:
<code>docker compose up --build</code>


As dependências são instaladas através do Dockerfile
# Conclusão
O PassCom foi desenvolvido como um sistema básico cliente-servidor, utilizando a API REST para comunicação e adotando princípios de servidor stateless. Isso permite uma comunicação eficiente entre clientes e servidores. A escolha da API REST contribui para uma melhor performance, maior confiabilidade e abre possibilidades para futuras expansões do sistema.

Durante o desenvolvimento, foi incorporado o uso do banco de dados PostgreSQL, que facilitou o armazenamento de informações e simplificou a realização de testes de concorrência. Além disso, a implementação de boas práticas de desenvolvimento, como autenticação, correção de erros e documentação da API, juntamente com o uso do Redis para controle de lock distribuído, fortaleceu a segurança do sistema.

Em resumo, os requisitos e funcionalidades do PassCom foram plenamente atendidos, incluindo os testes de concorrência. A experiência adquirida durante o desenvolvimento e implementação do projeto servirá como base para futuros trabalhos, incluindo no contexto profissional, uma vez que as tecnologias utilizadas são amplamente empregadas no mercado de trabalho.
