API em Flask para armazenamento de dados de Balança Corporal
Descrição
A API em Flask foi criada para disponibilizar e armazenar os dados da Balança Corporal Digital Omron HBF-514C. Através da API, é possível realizar a leitura dos dados coletados pela balança, bem como o armazenamento dos mesmos em um banco de dados.

Instruções de uso
Para iniciar a API via Docker (necessário ter o Docker instalado), execute o seguinte comando no terminal:

./deploy_api.sh

Se optar por não utilizar o Docker, execute os seguintes comandos para instalar os pacotes necessários:

pip install --no-cache-dir --upgrade -r requirements.txt
python app.py