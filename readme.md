# 🗄️ Database Backup to Cloudflare R2

Sistema de backups automáticos para bases de datos  
(MySQL, PostgreSQL, SQL Server, Oracle) con subida a **Cloudflare R2**.

✔ Multi-DB  
✔ Seguro (mínimo privilegio)  
✔ Compatible con CRON  
✔ Docker / No-Docker  
✔ Producción ready  

---

## 🧠 Arquitectura

DB → dump (CLI nativo) → gzip → Cloudflare R2

---

## 📁 Estructura del proyecto

backup/
├── main.py
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-entrypoint.sh
├── databases/
│ ├── base.py
│ ├── mysql.py
│ └── postgres.py
├── storage/
│ └── r2_storage.py
├── utils/
│ └── compress.py
├── .env
└── README.md


---

## ⚙️ Variables de entorno (`.env`)

```env
# DB ENGINE
DB_ENGINE=mysql

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=secret
DB_NAME=perfil_membresias

# R2
R2_BUCKET=backup-db
R2_ACCESS_KEY=AKxxxxxxxx
R2_SECRET_KEY=xxxxxxxx
R2_ENDPOINT=https://<ACCOUNT_ID>.r2.cloudflarestorage.com

# CRON (solo Docker)
CRON_SCHEDULE=0 3 * * *
```

## ▶️ USO SIN DOCKER

~~~
pip install -r requirements.txt
python main.py
crontab -e
0 3 * * * /usr/bin/python3 /ruta/main.py >> /var/log/db_backup.log 2>&1
~~~

## 🐳 USO CON DOCKER (RECOMENDADO)

### 🐳 Build de imagen

~~~
docker build -t db-backup-r2 .
~~~

###  ▶️ Ejecutar backup manual

~~~
docker run --rm --env-file .env db-backup-r2
~~~

~~~
docker run -d \
  --name db-backup-cron \
  --env-file .env \
  db-backup-r2
~~~