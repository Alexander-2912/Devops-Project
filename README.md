# Background Project
Projek Introduction to Devops ini adalah lanjutan dari projek Introduction to Web Development Architecture. Projek ini berfokus pada melakukan deployment pada aplikasi website hingga mencapai tahap 
aplikasi web tersebut mendapatkan nama domain sehingga dapat diakses lewat internet. Projek ini menggunakan beberapa tools atau teknik pemrograman, seperti Docker (Dockerfile dan Docker Compose),
CI/CD Pipeline, Nginx, dan Selenium.

# Penjelasan Langkah-Langkah Pembuatan/Code

## DockerFile untuk Flask
```
FROM python:3.10.12-bullseye

WORKDIR /app

EXPOSE 5000

# Install pip requirements
COPY . /app
RUN python -m pip install -r requirements.txt

CMD ["python", "run.py"]
```
1. FROM python:3.10.12-bullseye:

Menggunakan base image dari Python versi 3.10.12 pada sistem operasi Debian Bullseye. Ini menjadi dasar untuk image yang akan dibuat.

2. WORKDIR /app:

Menetapkan direktori kerja (working directory) di dalam container ke "/app". Ini adalah lokasi di dalam container di mana file-file proyek akan ditempatkan dan perintah-perintah 
selanjutnya akan dijalankan.

3. EXPOSE 5000:

Baris ini menginstruksikan Docker untuk membuka port 5000 saat image dijalankan. Baris ini memberi tahu Docker untuk mengizinkan koneksi masuk ke port tersebut.

4. COPY . /app:

Menyalin seluruh konten dari direktori saat ini (di mana Dockerfile berada) ke direktori "/app" di dalam container. Ini mencakup file-file yang diperlukan untuk menjalankan aplikasi.

5. RUN python -m pip install -r requirements.txt:

Menjalankan perintah untuk menginstal dependencies yang didefinisikan dalam file "requirements.txt" ke dalam container. Ini dilakukan selama proses pembuatan image.

7. CMD ["python", "run.py"]:

Menentukan perintah default yang akan dijalankan ketika container dijalankan. Dalam hal ini, container akan menjalankan skrip Python "python run.py".

## DockerFile untuk vue_project
```
FROM node:18

WORKDIR /frontend

COPY package*.json ./
COPY .env ./

RUN npm install
COPY . .

RUN npm run build

EXPOSE 8080

CMD ["npm", "run", "preview"]
```

1.FROM node:18:

Menggunakan base image dari Node.js versi 18. Ini adalah dasar untuk image yang akan dibuat.

2. WORKDIR /frontend:

Menetapkan direktori kerja (working directory) di dalam container ke "/frontend". Ini adalah lokasi di dalam container di mana file-file proyek akan ditempatkan dan perintah-perintah selanjutnya akan dijalankan.

3. COPY package.json ./*:

Menyalin file package.json dan package-lock.json dari direktori saat ini ke direktori kerja di dalam container. Ini dilakukan terlebih dahulu untuk memanfaatkan layer cache Docker dan mengoptimalkan proses pembangunan.

4. COPY .env ./:

Menyalin file ".env" dari direktori saat ini ke direktori kerja di dalam container. Ini memasukkan konfigurasi lingkungan yang diperlukan oleh aplikasi.

5. RUN npm install:

Menjalankan perintah untuk menginstal semua dependencies yang didefinisikan dalam file package.json.

6. COPY . ./:

Menyalin seluruh konten dari direktori saat ini ke direktori kerja di dalam container. Ini mencakup file-file proyek dan aplikasi yang akan dijalankan.

7. RUN npm run build:

Menjalankan perintah untuk membangun aplikasi frontend. Ini termasuk kompilasi kode, pengelolaan dependensi, dan langkah-langkah pembangunan lainnya.

8. EXPOSE 8080:

Baris ini menginstruksikan Docker untuk membuka port 8080 saat image dijalankan. Baris ini memberi tahu Docker untuk mengizinkan koneksi masuk ke port tersebut.

9. CMD ["npm", "run", "preview"]:

Menentukan perintah default yang akan dijalankan ketika container dijalankan. Dalam hal ini, container akan menjalankan skrip "npm run preview".

## Docker Compose untuk Flask dan vue_project
```
version: '3.4'

services:
  flask-app:
    container_name: flask-compose
    image: flask:0.0.6
    build:
      context: ./Final/Flask
      dockerfile: Dockerfile
    restart: always
    ports:
      - "5010:5000"
    depends_on:
      - postgres

  postgres:
    container_name: postgres-compose
    image: postgres:12
    restart: always
    ports:
      - "5433:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres
    volumes:
      - postgres-data:/var/lib/postgresql/data

  frontend:
    image: frontend:latest
    build:
      context: ./Final/vue_project
      dockerfile: Dockerfile
    ports:
      - 8090:8080
    depends_on:
      - flask-app 

volumes:
  postgres-data:
```

1. version: '3.4':

Mendefinisikan versi format Docker Compose yang akan digunakan. Dalam hal ini, versi 3.4 digunakan.

2. services:

Bagian ini mulai mendefinisikan layanan-layanan yang akan dijalankan sebagai kontainer.

3. flask-app:

- Mendefinisikan layanan untuk aplikasi Flask.
  
- container_name: flask-compose: Menetapkan nama kontainer menjadi "flask-compose".
  
- image: flask:0.0.6: Menggunakan image Docker bernama "flask:0.0.6".
  
- build:: Mendefinisikan bagaimana image akan dibangun.
  
- context: ./Final/Flask: Menentukan direktori konteks untuk build.
  
- dockerfile: Dockerfile: Menentukan file Dockerfile yang akan digunakan.
  
- restart: always: Menetapkan agar kontainer selalu di-restart jika berhenti atau terhenti.
  
- ports:: Menetapkan pemetaan port, dengan port 5010 dari host diarahkan ke port 5000 di kontainer.
  
- depends_on:: Menetapkan bahwa layanan ini bergantung pada layanan postgres.

4. postgres:

- Mendefinisikan layanan untuk database PostgreSQL.

- container_name: postgres-compose: Menetapkan nama kontainer menjadi "postgres-compose".

- image: postgres:12: Menggunakan image Docker PostgreSQL versi 12.

- restart: always: Menetapkan agar kontainer selalu di-restart jika berhenti atau terhenti.
- ports:: Menetapkan pemetaan port, dengan port 5433 dari host diarahkan ke port 5432 di kontainer.
- environment:: Menetapkan variabel lingkungan untuk konfigurasi PostgreSQL.
- volumes:: Menetapkan volume untuk menyimpan data PostgreSQL.

5. frontend:

- Mendefinisikan layanan untuk aplikasi frontend.

- image: frontend:latest: Menggunakan image Docker bernama "frontend:latest".

- build:: Mendefinisikan bagaimana image akan dibangun.

- context: ./Final/vue_project: Menentukan direktori konteks untuk build.

- dockerfile: Dockerfile: Menentukan file Dockerfile yang akan digunakan.

- ports:: Menetapkan pemetaan port, dengan port 8090 dari host diarahkan ke port 8080 di kontainer.

- depends_on:: Menetapkan bahwa layanan ini bergantung pada layanan flask-app.

6. volumes::

Mendefinisikan volume Docker bernama "postgres-data" yang digunakan oleh layanan postgres untuk menyimpan data PostgreSQL
