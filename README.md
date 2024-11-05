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

Este relatório tem como objetivo apresentar o desenvolvimento de um sistema distribuído de compra de passagens aéreas, que conecta clientes a três empresas aéreas distintas, facilitando a pesquisa de rotas, comparação de preços e a compra de bilhetes. A solução proposta é baseada em uma arquitetura distribuída, utilizando microserviços e comunicação entre sistemas por meio de APIs RESTful. Para garantir escalabilidade e performance, o sistema foi desenvolvido com a linguagem Go para a implementação de back-end, e a interface do usuário foi construída com React. Além disso, o sistema foi projetado para suportar alta disponibilidade e integridade de dados, mesmo em cenários de grande volume de acessos.

A seguir, detalharemos os aspectos técnicos e operacionais do sistema, além dos desafios enfrentados durante o processo de desenvolvimento e os resultados alcançados.

# Arquitetura da aplicação
A arquitetura do sistema é baseada no cliente-servidor, porém contendo uma comunicação entre servidores. Resumidamente, é como se quando um servidor for comunicar com outro, o remetente da mensagem é como um cliente.
#  Protocolo de comunicação
A comunicação foi realizada por meio de uma API REST, que recebe e envia dados em formato JSON, adotando o princípio stateless, no qual cada requisição contém todas as informações necessárias para seu processamento. Os endpoints são protegidos por autenticação JWT, exigindo que os usuários estejam autenticados para realizar as seguintes operações: visualizar trechos, comprar passagens, consultar passagens e cancelar passagens. Foram implementados dois conjuntos de rotas: uma para a comunicação entre servidores e outra para a interação entre clientes e servidores. A documentação detalhada da API está disponível mais adiante neste artigo.

# Interface da Aplicação

# Concorrência Distribuída

# Confiabilidade da solução

# Avaliação da Solução

# Documentação do código

# Docker

# Conclusão