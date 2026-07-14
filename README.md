### Dependências necessárias:

* Psycopg2
* Pillow
* Tkinter

```bash
pip install customtkinter Pillow psycopg2-binary python-dotenv
```

É preciso configurar um arquivo `.env` na raiz do projeto contendo as informações de conexão com o banco de dados com o seguinte formato:

```env
DB_HOST=localhost
DB_NAME=pet
DB_USER=postgres
DB_PASSWORD=sua_senha
```
