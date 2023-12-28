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

Menginformasikan Docker bahwa container ini akan mendengarkan pada port 5000. Ini bukanlah perintah yang mengarahkan Docker untuk memaparkan atau membuka port, tetapi hanya memberikan informasi.

4. COPY . /app:

Menyalin seluruh konten dari direktori saat ini (di mana Dockerfile berada) ke direktori "/app" di dalam container. Ini mencakup file-file yang diperlukan untuk menjalankan aplikasi.

5. RUN python -m pip install -r requirements.txt:

Menjalankan perintah untuk menginstal dependencies yang didefinisikan dalam file "requirements.txt" ke dalam container. Ini dilakukan selama proses pembuatan image.

7. CMD ["python", "run.py"]:

Menentukan perintah default yang akan dijalankan ketika container dijalankan. Dalam hal ini, container akan menjalankan skrip Python "run.py". Perintah CMD ini dapat digantikan 
jika ada perintah yang diberikan saat menjalankan container.
