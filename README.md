API em Flask para armazenamento de dados de Balança Corporal
Descrição
A API em Flask foi criada para disponibilizar e armazenar os dados da Balança Corporal Digital Omron HBF-514C. Através da API, é possível realizar a leitura dos dados coletados pela balança, bem como o armazenamento dos mesmos em um banco de dados.

Instruções de uso
Para iniciar a API, é necessário ter o Docker instalado. Em seguida, basta executar o seguinte comando no terminal:

css
Copy code
docker-compose up --build
Assim que a API estiver rodando, é possível realizar as seguintes operações:

GET /dados: Retorna todos os dados armazenados no banco de dados.
POST /dados: Adiciona um novo dado ao banco de dados.
DELETE /dados/{id}: Remove o dado com o ID especificado do banco de dados.