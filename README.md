## Kurulum

Projeyi yerel ortamınızda çalıştırmak için Docker ve Docker Compose kurulu olmalıdır.

1.  Projeyi klonlayın:
    ```bash
    git clone <proje_deposu_url>
    cd <proje_klasoru>
    ```
2.  `.env` dosyasını oluşturun. Projenizin kök dizininde `.env.example` dosyasını kopyalayarak `.env` adıyla kaydedin ve gerekli veritabanı bilgileri ile `SECRET_KEY` değerini doldurun.
    ```bash
    cp .env.example .env
    ```
3.  Docker Compose ile servisleri başlatın:
    ```bash
    docker compose up -d --build
4.  Veritabanı migrasyonlarını çalıştırın:
    ```bash
    docker compose exec web python manage.py migrate
    ```
5.  İsteğe bağlı olarak bir yönetici kullanıcısı oluşturun:
    ```bash
    docker compose exec web python manage.py createsuperuser
    ```
    Komut satırındaki adımları takip edin.

Proje artık `http://localhost:8000/` adresinde çalışıyor olmalıdır.

## API Dokümantasyonu

API endpoint'lerinin detaylı ve interaktif dokümantasyonuna aşağıdaki adreslerden erişebilirsiniz:

* **Swagger UI:** `http://localhost:8000/swagger/`
* **ReDoc:** `http://localhost:8000/redoc/`

Bu arayüzler üzerinden API endpoint'lerini inceleyebilir ve doğrudan test istekleri gönderebilirsiniz.

## API Endpointleri

API endpointleri `/v1/` prefix'i altındadır. Ana endpointler şunlardır:

* `/v1/users/`
* `/v1/todos/`
* `/v1/posts/`
* `/v1/comments/`
* `/v1/albums/`
* `/v1/photos/`


## Testleri Çalıştırma

API testlerini çalıştırmak için aşağıdaki komutu kullanın:

```bash
docker compose exec web python manage.py test