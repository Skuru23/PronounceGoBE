# fast-next-monolith-template

## Setup environment

### 1. Open terminal and run:

```git
  git clone https://github.com/theinfitech/getit-seminar.git`
```

### 2. Create 2 .env files

- After successfully cloning, open project in vscode. Create 2 .env files and copy content from backend/.env.example file to 2 files just created:
  - .env (at root folder)
  - /backend/.env

   ```bash
    cat backend/.env.example | tee .env backend/.env
  ```

### 3. Run docker and install backend packages

- Use keyboard shortcut `Ctrl + Shift + P` -> type: `Dev Containers: Open Folder in Container` and enter. This command will reopen vscode, run project in Dev Container Environment and install all necessary packages for backend environment. Wait 3-4 minutes for completely installing.

### 4. Test run backend.

- In root folder, run backend:

  ```bash
    uvicorn backend.main:app --reload
  ```

- Open browser and type `http://127.0.0.1:8000/docs`. If the Swagger docs screen appears, it means it has been run successfully.

### 5. Migrate model to Postgresql.

- In root folder, run command:

  ```bash
    alembic upgrade heads
  ```

- To migrate new content in model to database
  + Check to see if the latest code has been pulled?

    ```bash
      git pull origin dev
    ```

  + Update to the newest version

    ```bash
      alembic upgrade heads
    ```

  + Migrating the newly changed content in the model into the database:

    ```bash
      alembic revision --autogenerate -m "Comment for change"
    ```


### 6. Check PostgreSQL connection

- Open DBeaver -> New Database Connection -> Choose PostgreSQL
- Fill Host, Database, Username, Password, Port input using info in .env file
- Test connection. If success then finish.

- **NOTE**: In case there is already a database running on port 5432, check the ports tab next to the terminal tab, find port 5432 and forwarded address, for example: localhost:33412. Get port 33412 and replace port 5432 in DBeaver.


### 7. Install frontend packages

- In frontend folder -> Download all necessary npm packages:

  ```bash
    pnpm i
  ```

### 8. Setting domain for local

- Add `127.0.0.1 organization.localhost` to file `/etc/hosts`
    - Step 1: open terminal enter command `sudo nano /etc/hosts`
    - Step 2: add line `127.0.0.1 organization.localhost` -> save config
  ``OR
  - Linux: `sudo sh -c "echo '127.0.0.1 organization.localhost' >> /etc/hosts"`( manually add config )
- Setting local `.env` using `localhost` instead of `localhost:3000`
