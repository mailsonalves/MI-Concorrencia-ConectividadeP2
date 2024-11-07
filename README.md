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
<p></p>
<div align="center">
<img src="https://github.com/user-attachments/assets/bf350d98-357b-434a-a786-8b0a745f8237" >
</div>
<p></p>
<p align="center">Figura 1. Arquitetura do sistema</p>
<p></p>
Os componentes da arquitetura do sitema Passcom são:
<ul>
  <li>
    Banco de dados: há um banco de dados para a persistência de dados.
  </li>
  <li>
    Servidores: existem 3 servidores no PassCom, cada um representando uma companhia aérea.
  </li>
  <li>
    Interface de usuário: a interface web foi um bônus do sistema, visto que não era um requisito obrigatório. Em prol disso, possui uma aparência simples, mas legível e funcional.
  </li>
  <li>
    Cliente: o usuário que interage com o sistema, mandando mensagens e recebendo dos servidores.
  </li>
  <li>
    Protocolo de comunicação: utilizado com API REST.
  </li>
  <li>
    Lógica de negócios: feita no back-end, é o conjunto de regras, processos e tratamentos de erros que definem toda a parte funcional do sistema, como a compra de passagem, verificação de assento, entre outros.

  </li>
</ul>






<h3>Banco de Dados</h3>
Foi escolhido o banco de dados relacional PostgreSQL para armazenar as informações do sistema. Cada servidor possui um banco de dados executando isoladamente em seu próprio container Docker. Cada usuário poderá se cadastrar e fazer login apenas a partir do seu servidor de origem, mas podendo visualizar e interagir com os dados dos outros servidores. A figura 1 mostra o diagrama de entidade-relacionamento entre as classes do banco de dados.
<p></p>
<div align="center">
<img src="" width="700">
</div>
<p align="center">Figura 3. Diagrama de entidade e relacionamento do Banco de Dados </p>
<p></p>

<h3>Comunicação entre servidores</h3>
Para gerenciar a lógica e regras de negócio da aplicação foi escolhido o framework FastAPI para o backend do sitema. A utilização do FastApi facilitou a comunicação cliente-servidor e servidor-servidor através das rotas especificadas em portas de rede disitintas. Além disso, o uso do framework facilitou a integração com o front-end da aplicação especificando como as requisições devem ser feitas aos servidores.
<h3>Interface Gráfica</h3>
Para a implementação da interface gráfica do sistema foi utilizado o framework ReactJS. A ideia é oferecer ao usuário final do sitema uma interface clara e intuitiva para proporcionar uma boa experência de compra.
Algumas das principais telas do sistema estão mostradas nas figuras a seguir. A figura 3 mostra  a tela inicial de listagem de voos do sistema sem o usuário estar logado em uma das companhias aéreas.
Já a figura 3 mostra o modal de Login para o usuário se autenticar no sistema.

<p></p>
<div align="center">
<img src="https://github.com/user-attachments/assets/d4a3a998-67db-4dd0-8eca-2da1cebe6364" width="700">
</div>
<p align="center">Figura 3. Tela inicial do sistema </p>
<p></p>

<div align="center">
<img src="https://github.com/user-attachments/assets/27a3117b-9030-4a34-bf2d-2f175c591c5b" width="700">
</div>
<p align="center">Figura 4. Modal de login do sistema</p>
<p></p>

#  Protocolo de comunicação
A comunicação foi realizada por meio de uma API REST, que recebe e envia dados em formato JSON, adotando o princípio stateless, no qual cada requisição contém todas as informações necessárias para seu processamento. Os endpoints são protegidos por autenticação JWT, exigindo que os usuários estejam autenticados para realizar as seguintes operações: visualizar trechos, comprar passagens, consultar passagens e cancelar passagens. Foram implementados dois conjuntos de rotas: uma para a comunicação entre servidores e outra para a interação entre clientes e servidores. A documentação detalhada da API está disponível mais adiante neste artigo.

# Interface da Aplicação
Falar sobre o rest

# Funcionamento da Aplicação
Um resumo dos principais endpoints e do funcionamento da aplicação envolve o processo de compra de passagem, onde foi feito o tratamento da concorrência distribuida do sitema.
A seguir, explicaremos o funcionamento dos endpoints  (/buy_ticket) e (/delete_ticket) que são críticos no processo de concorrência entre os servidores das 3 empresas envolvidas.

Mais adiante no tópico da Documentação do código serão mostrados os demais endpoints da aplicação. 
<h3>Compra de passagem</h3>
No processo de compra de passagem deste sistema, o usuário realiza a solicitação através de uma rota específica (/buy_ticket) que espera receber alguns dados essenciais, como o identificador do usuário (user_id), as informações da passagem e uma sessão de banco de dados para controlar a transação.
A Figura 5 mostra a tela de compra de passagem, onde é feito o processo indicado anteriormente.
<p></p>
<div align="center">
<img src="https://github.com/user-attachments/assets/87d0b74e-cd7b-449b-b18a-b6a659c8ef05" width="700">
</div>
<p align="center">Figura 5. Tela de compra de passagem</p>
<p></p>
Para garantir a segurança, é feita a validação do user_id fornecido, convertendo-o para o formato UUID e lançando um erro caso o ID seja inválido. Em seguida, o sistema verifica se o usuário está devidamente autenticado e se o ID da requisição corresponde ao ID do usuário logado, assegurando que apenas o dono da conta possa concluir a compra.

Uma vez validada a identidade do usuário, o processo de compra segue para a verificação da companhia aérea associada à passagem. Se a companhia aérea escolhida for BrasilPass, a transação é tratada localmente no sistema. Isso inclui verificar a capacidade do voo e garantir que o assento selecionado esteja disponível. O código conta quantas passagens já foram compradas para o voo em questão e compara com a capacidade total do voo. Caso o limite de assentos ou de passagens para o voo já tenha sido atingido, um erro é lançado e a compra é cancelada. Se todas as condições de voo forem atendidas, a passagem é então registrada no banco de dados, e a transação é finalizada com sucesso. A Figura 6 mostra a tela de confirmação de compra, caso todas as verificações tenham sido bem sucessidas.
<p></p>
<div align="center">
<img src="https://github.com/user-attachments/assets/f0c7185d-0baf-48b7-acae-b25dadbe4090" width="700">
</div>
<p align="center">Figura 6. Tela de de confimação de compra de passagem</p>
<p></p>


Por outro lado, se a companhia aérea associada for BrAirlines ou VoeBr, a compra da passagem é redirecionada para um serviço externo específico da companhia. O sistema realiza uma chamada POST para o endpoint de cada companhia aérea, enviando os dados da passagem e o user_id. Como essas operações externas podem falhar por diversos motivos (como instabilidade de rede), o código tenta realizar a compra até três vezes, aguardando brevemente entre as tentativas. Caso todas as tentativas falhem, o sistema reverte qualquer transação que já tenha sido registrada localmente, mantendo a integridade dos dados. Se o serviço externo responder positivamente e a compra for completada, a passagem é então armazenada no banco de dados local para registro e controle.


<h3>Listagem e Exclusão de passagem</h3>
A figura 7 mostra a listagem de passagens compradas por um usuário.
<p></p>
<div align="center">
<img src="https://github.com/user-attachments/assets/07c60706-c4a7-40d4-8366-c41fe619896c" width="700">
</div>
<p align="center">Figura 7. Tela de listagem de passagens compradas</p>
<p></p>

No processo de exclusão de passagem neste sistema, o usuário faz uma solicitação para deletar um bilhete específico utilizando uma rota dedicada (/delete_ticket). Primeiramente, o código valida o identificador da passagem (passagem_id), que deve estar em formato UUID. Se o identificador não for válido, o sistema retorna um erro, impedindo qualquer operação com IDs incorretos. Em seguida, o código verifica se o usuário está autenticado e autorizado, pois somente o proprietário da passagem pode excluí-la. Caso o usuário não esteja logado ou não seja o dono do bilhete, uma exceção é lançada para informar que ele não tem permissão para a ação.

Depois de confirmar as permissões e a autenticidade do usuário, o sistema busca a passagem no banco de dados. Se a passagem não for encontrada, ele retorna um erro específico, garantindo que apenas passagens válidas e registradas possam ser excluídas. Quando a passagem existe e as permissões estão em ordem, o código prossegue com a tentativa de exclusão no banco de dados local. Essa exclusão é uma operação crítica e, por isso, o sistema envolve a transação em um mecanismo de segurança, que faz rollback em caso de falhas. Assim, qualquer problema no processo é revertido para manter a consistência dos dados.

Para passagens de companhias aéreas externas (ou seja, diferentes de BrasilPass), o sistema realiza uma etapa adicional para deletar a passagem no servidor da companhia aérea específica. Dependendo da companhia (BrAirlines ou VoeBr), ele chama a função delete_ticket_external, que envia uma requisição DELETE ao servidor externo correspondente, com o identificador da passagem incluído. Caso o servidor externo responda com um erro ou status que não seja de sucesso, o sistema interrompe o processo e emite um erro, informando o usuário de que houve uma falha na exclusão no servidor externo. Esse tratamento detalhado de exceções assegura que o sistema mantenha o usuário bem informado e que a exclusão seja consistente entre o banco de dados local e os servidores externos.

A função delete_ticket_external é responsável por gerenciar as conexões com os servidores externos, tratando qualquer erro de status HTTP ou exceções inesperadas, garantindo uma comunicação estável e o recebimento de respostas confiáveis. Quando todas as verificações e operações são bem-sucedidas, a passagem é completamente deletada e o sistema retorna uma mensagem de confirmação ao usuário, informando que a passagem foi excluída com sucesso.

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

Endpoints da aplicação
<p align="center">Tabela 2. Endpoints de Usuário</p>

| EndPoint        | Método                                                               | Descrição                                    | Parametros       | Resposta                                                    |                         
| -------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |------------------------------------------------------- |------------------------------------------------------ |
| POST /      | POST | Cria um novo usuário.                                       | Um objeto do tipo UserSchema que inclui os dados do usuário (nome, username, senha, email)          |  UserSchemaPublic com os dados do usuário recém-criado.    |
| GET /users      | GET |  Retorna uma lista de usuários limitada pelo parâmetro limit                                       |  limit (int) — o número máximo de usuários a serem retornados (padrão: 15)..            | 200 OK se a lista for retornada com sucesso, 500 Internal Server Error se ocorrer um erro ao listar os usuários.    |

<p></p>
<p align="center">Tabela 2. Endpoints de Voo</p>

| EndPoint        | Método                                                               | Descrição                                    | Parametros       | Resposta                                                    |                         
| -------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |------------------------------------------------------- |------------------------------------------------------ |
| POST /      | POST | Cria um novo voo.                                      | voo (VooSchema): Objeto contendo as informações do voo, incluindo origem, destino         |  Retorna um objeto VooSchema com os dados do voo recém-criado.   |
| GET /      | GET |  Lista voos locais e remotos, limitando a quantidade de resultados com base no parâmetro limit.                                       |  limit (int): Limite de voos a serem retornados (padrão: 15).            | Retorna uma lista de objetos VooSchemaList com os dados dos voos.    |
<p></p>
<p align="center">Tabela 2. Endpoints de Ticket (passagem)</p>

| EndPoint        | Método                                                               | Descrição                                    | Parametros       | Resposta                                                    |                         
| -------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |------------------------------------------------------- |------------------------------------------------------ |
| /buy_ticket_no_login       | POST | Compra uma passagem sem a necessidade de login.                                       | user_id (string): ID do usuário, db_session (DatabaseSession): Sessão do banco de dados. , passagem (PassagemSchema): Dados da passagem.           |  Status Code:200 OK, Retorna os dados da passagem comprada.    |
| /buy_ticket      | POST | Compra uma passagem com autenticação.                                       |  user_id (UUID): ID do usuário, db_session (DatabaseSession): Sessão do banco de dados,passagem (PassagemSchema2): Dados da passagem, current_user (Depends): Usuário autenticado.            | Status Code: 200 OK, Retorna os dados da passagem comprada.     |
<p></p>

# Docker
Devido a necessidade de ter vários containers com serviços diferentes executando, foi usado o Docker Compose para gerenciá-los. Ao todo são 3 containers, sendo um para cada servidor.
Assim, o arquivo docker-compose.yaml une a execução dos contêineres, permitindo o build e execução dos componentes de cada uma das companhias aéreas a partir do comando:

```
docker compose up --build
```

As dependências são instaladas através do Dockerfile
# Conclusão
O PassCom foi desenvolvido como um sistema básico cliente-servidor, utilizando a API REST para comunicação e adotando princípios de servidor stateless. Isso permite uma comunicação eficiente entre clientes e servidores. A escolha da API REST contribui para uma melhor performance, maior confiabilidade e abre possibilidades para futuras expansões do sistema.

Durante o desenvolvimento, foi incorporado o uso do banco de dados PostgreSQL, que facilitou o armazenamento de informações e simplificou a realização de testes de concorrência. Além disso, a implementação de boas práticas de desenvolvimento, como autenticação, correção de erros e documentação da API, juntamente com o uso do Redis para controle de lock distribuído, fortaleceu a segurança do sistema.

Em resumo, os requisitos e funcionalidades do PassCom foram plenamente atendidos, incluindo os testes de concorrência. A experiência adquirida durante o desenvolvimento e implementação do projeto servirá como base para futuros trabalhos, incluindo no contexto profissional, uma vez que as tecnologias utilizadas são amplamente empregadas no mercado de trabalho.
