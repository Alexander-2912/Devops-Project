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

## Testing Menggunakan Selenium
```
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from pyvirtualdisplay import Display

display = Display(visible=0, size=(300,300))
display.start()

chromedriver_autoinstaller.install()

chrome_options = webdriver.ChromeOptions()

options = [
    "--window-size=1200, 1200",
    "--ignore-certificate-errors"
]

for option in options:
    chrome_options.add_argument(options)

class TestFormElements:
    def setup_class(cls):
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.get("http://localhost:5173/login")

    def teardown_class(cls):
        cls.driver.quit()

    def test_nama_label(self):
        nama_label = self.driver.find_element(By.XPATH, "//label[@for='username']")
        assert nama_label.text == "Username", "pengecekan nama gagal"

    def test_password_label(self):
        password_label = self.driver.find_element(By.XPATH, "//label[@for='password']")
        assert password_label.text == "Password", "pengecekan password gagal"
```

1. Import Libraries:

- import pytest: Mengimport library Pytest untuk menjalankan test case.

- from selenium import webdriver: Mengimport webdriver dari Selenium untuk mengontrol browser.

- from selenium.webdriver.common.by import By: Mengimport metode untuk menemukan elemen di halaman web.

- import chromedriver_autoinstaller: Mengimport library untuk menginstal ChromeDriver secara otomatis.

- from pyvirtualdisplay import Display: Mengimport library untuk membuat virtual display (digunakan untuk menjalankan tes di lingkungan tanpa GUI).

2. Konfigurasi Virtual Display:

- display = Display(visible=0, size=(300, 300)): Membuat virtual display dengan ukuran 300x300 piksel dan tidak terlihat.

- display.start(): Memulai virtual display.

3. Instalasi ChromeDriver:

- chromedriver_autoinstaller.install(): Mengunduh dan menginstal ChromeDriver.

4. Konfigurasi Chrome Options:

- chrome_options = webdriver.ChromeOptions(): Membuat objek untuk menyimpan opsi untuk browser Chrome.
  
- options : Daftar opsi untuk browser Chrome
  
- --window-size=1200, 1200: Mengatur ukuran jendela browser menjadi 1200x1200 piksel.
  
- --ignore-certificate-errors: Mengabaikan kesalahan sertifikat SSL.
  
- for option in options: Menambahkan setiap opsi ke objek chrome_options.

5. Test Class:

- class TestFormElements:: Mendefinisikan kelas untuk menampung test case.

6. Setup dan Teardown:

- def setup_class(cls):  Dijalankan sebelum semua test case dalam kelas ini dijalankan:

- cls.driver = webdriver.Chrome(options=chrome_options): Membuat instance Chrome webdriver dengan opsi yang telah ditentukan.

- cls.driver.get("http://localhost:5173/login"): Membuka halaman login di browser.

- def teardown_class(cls): Dijalankan setelah semua test case selesai dijalankan:

- cls.driver.quit(): Menutup browser.

7. Test Case:

- def test_nama_label(self):  Test case untuk memeriksa label nama:

- nama_label = self.driver.find_element(By.XPATH, "//label[@for='username']]"): Menemukan label nama menggunakan XPath.

- assert nama_label.text == "Username", "pengecekan nama gagal": Memastikan teks label nama adalah "Username".

- def test_password_label(self):  Test case untuk memeriksa label password:

- password_label = self.driver.find_element(By.XPATH, "//label[@for='password']]"): Menemukan label password.

- assert password_label.text == "Password", "pengecekan password gagal": Memastikan teks label password adalah "Password".

## Continuous Integration
```
name: CI (Continuous Integration)

on:
  pull_request:
    branches: [ "main" ]

jobs:

  build-testing:
    name: Build and Testing
    runs-on: windows-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
    
      - name: Install Docker Compose 
        run: |
          sudo apt-get update
          sudo apt-get install -y docker-compose
      
      - name: Build and Run Container
        run: |
          sudo docker compose up -d

      - name: Install Requirements for Testing
        run: |
          pip install -r testing\requirements.txt

      - name: Testing
        run: |
          sleep 20
          pytest testing/test.py
```

1. Name:

name: CI (Continuous Integration): Memberi nama pada workflow, memudahkan identifikasi.

2. On:

- pull_request: Menentukan bahwa workflow ini akan dijalankan ketika ada pull request dibuat.

- branches: [ "main" ]: Menentukan bahwa workflow ini hanya akan dijalankan untuk pull request yang dibuat terhadap branch "main".

3. Jobs:

Bagian ini mendefinisikan tugas-tugas yang akan dijalankan dalam workflow.

4. build-testing:

- name: Build and Testing: Memberi nama pada job ini.

- runs-on: windows-latest: Menentukan bahwa job ini akan dijalankan pada runner Windows.

5. Steps:

Bagian ini mendefinisikan langkah-langkah yang akan dijalankan dalam job.

- Checkout repository:

uses: actions/checkout@v2: Mengambil kode dari repository ke runner.

- Install Docker Compose:

sudo apt-get update: Memperbarui daftar paket yang tersedia.
sudo apt-get install -y docker-compose: Menginstal Docker Compose.

- Build and Run Container:

sudo docker compose up -d: Menjalankan perintah Docker Compose untuk membangun dan menjalankan kontainer.

- Install Requirements for Testing:

pip install -r testing\requirements.txt: Menginstal dependensi yang diperlukan untuk menjalankan tes.

- Testing:

sleep 20: Menunggu 20 detik untuk memastikan kontainer sudah berjalan dengan baik.
pytest testing/test.py: Menjalankan tes yang terdapat pada file testing/test.py.

## Continuous Delivery & Deployment
```
    name: CD (Continuous Delivery & Deployment)

    on: workflow_dispatch
    
    jobs:
        
        build-push:
            name: Build and Push Image To DockerHub
            runs-on: ubuntu-latest
    
            steps:
                - name: Checkout Repository
                  uses: actions/checkout@v2
    
                - name: Login to Docker Hub
                  uses: docker/login-action@v2
                  with:
                    username: ${{ secrets.DOCKERHUB_USERNAME }}
                    password: ${{ secrets.DOCKERHUB_TOKEN }}
    
                - name: Set up Docker Buildx
                  uses: docker/setup-buildx-action@v2
                  
                - name: Build and push flaskapp
                  uses: docker/build-push-action@v4
                  with:
                    context: ./Final/Flask
                    file: ./Final/Flask/Dockerfile
                    push: true
                    tags: ${{ secrets.DOCKERHUB_USERNAME }}/flask:${{ github.run_number }}/Flask:latest
                      
                - name: Build and push postgres
                  uses: docker/build-push-action@v4
                  with:
                    context: ./Final/vue_project
                    file: ./Final/vue_project/Dockerfile
                    push: true
                    tags: ${{ secrets.DOCKERHUB_USERNAME }}/vue_project:${{ github.run_number }}/vue_project:latest
        deploy: 
            name: Deploy to Server
            runs-on: self-hosted
            needs: build-push
    
            steps:
              - name : Pull latest images
                run: |
                    docker pull ${{ secrets.DOCKERHUB_USERNAME }}/Flask:latest
                    docker pull ${{ secrets.DOCKERHUB_USERNAME }}/vue_project:latest
          
              - name: Stop and Remove Existing Containers and Networks
                run: |
                    docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)
                    docker network prune -f
    
              - name: Create Network and Run containers
                run : |
                  sudo docker compose up -d

              - name: Remove unused data
                run: |
                  docker system prune -af
```

1. Name:

name: CD (Continuous Delivery & Deployment): Memberi nama pada workflow, memudahkan identifikasi.

2. On:

workflow_dispatch: Menentukan bahwa workflow ini akan dijalankan secara manual, bukan otomatis saat ada event tertentu.

3. Jobs:

Bagian ini mendefinisikan tugas-tugas yang akan dijalankan dalam workflow.

4. build-push:

- name: Build and Push Image To DockerHub: Memberi nama pada job ini.
- runs-on: windows-latest: Menentukan bahwa job ini akan dijalankan pada runner windows.

5. Steps (build-push):

- Checkout Repository: Mengambil kode dari repository ke runner.

- Login to Docker Hub: Login ke Docker Hub untuk mendorong image.

- Set up Docker Buildx: Mengatur Docker Buildx untuk membangun image multi-arsitektur.

- Build and push flaskapp: Membangun dan mendorong image flaskapp ke Docker Hub.

- Build and push vue_project: Membangun dan mendorong image vue_project ke Docker Hub.

6. deploy:

- name: Deploy to Server: Memberi nama pada job ini.

- runs-on: self-hosted: Menentukan bahwa job ini akan dijalankan pada runner yang di-host sendiri.

- needs: build-push: Menentukan bahwa job ini bergantung pada job build-push untuk selesai terlebih dahulu.

7. Steps (deploy):

- Pull latest images: Menarik image terbaru dari Docker Hub.

- Stop and Remove Existing Containers and Networks: Menghentikan dan menghapus kontainer dan jaringan yang sudah ada.

- Create Network and Run containers: Membuat jaringan dan menjalankan kontainer menggunakan Docker Compose.

- Remove unused data: Menghapus data yang tidak digunakan untuk menghemat ruang disk.

## Continue Development

```
name: CD (Continue Deployment)

on: workflow_dispatch

jobs:
    deploy:
        name: Deploy to Server
        runs-on: self-hosted

        steps:
            - name : Pull newest images
              run: |
                docker pull ${{secrets.DOCKERHUB_USERNAME}}//Flask:${{github.run_number}}
                docker pull ${{secrets.DOCKERHUB_USERNAME}}//vue_project:${{github.run_number}}

            - name : Stop and Remove Existing Containers and Networks
              run: |
                docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)
                docker network prune -f

            - name : Create Network and Run Containers
              run: |
                docker network create vite
                docker run -d -p 5000:5000 --network vite --hostname Flask --mount "type=volume,source=pgdata,destination=/var/lib" --name flask -e
                sleep 5
                docker run -d -p 5173:5173 --network vite --hostname vue_project %{{ secret.DOCKERHUB_USERNAME}}/vue_project:%{{github.run_number}}

            - name : Remove unused data
              run: |
                docker system prune -af
```

1. Name:

name: CD (Continue Deployment): Memberi nama pada workflow, memudahkan identifikasi.

2. On:

workflow_dispatch: Menentukan bahwa workflow ini akan dijalankan secara manual, bukan otomatis saat ada event tertentu.

3. Jobs:

Bagian ini mendefinisikan tugas-tugas yang akan dijalankan dalam workflow.

4. deploy:

- name: Deploy to Server: Memberi nama pada job ini.

- runs-on: self-hosted: Menentukan bahwa job ini akan dijalankan pada runner yang di-host sendiri (bukan runner GitHub).

5. Steps:

Pull newest images:
- docker pull ...: Menarik image terbaru dari Docker Hub menggunakan tag yang menyertakan nomor run workflow, memastikan penggunaan image yang sesuai dengan deployment ini.

Stop and Remove Existing Containers and Networks:
- docker stop ...: Menghentikan semua kontainer yang sedang berjalan.
- docker rm ...: Menghapus semua kontainer yang telah dihentikan.
- docker network prune -f: Menghapus semua jaringan yang tidak digunakan.

Create Network and Run Containers:

- docker network create vite: Membuat jaringan baru bernama "vite" untuk menghubungkan kontainer.
- docker run ... flask: Menjalankan kontainer untuk aplikasi Flask:
- -d: Menjalankan kontainer di background.
- -p 5000:5000: Memetakan port internal 5000 ke port 5000 pada host.
- --network vite: Menempatkan kontainer pada jaringan "vite".
- --hostname Flask: Memberikan hostname "Flask" pada kontainer.
- --mount ...: Memasang volume bernama "pgdata" ke direktori "/var/lib" di dalam kontainer, kemungkinan untuk penyimpanan data PostgreSQL.
- --name flask: Memberikan nama "flask" pada kontainer.
- -e: Mengatur variabel lingkungan, namun nilainya tidak ditampilkan dalam kode yang diberikan.
- sleep 5: Menunggu 5 detik untuk memastikan kontainer Flask sudah berjalan dengan baik sebelum menjalankan kontainer vue_project.
- docker run ... vue_project: Menjalankan kontainer untuk aplikasi vue_project dengan pengaturan yang mirip dengan kontainer Flask.

Remove unused data:

docker system prune -af: Menghapus semua data yang tidak digunakan, seperti image, kontainer, dan volume yang tidak lagi terpakai, untuk menghemat ruang disk.
