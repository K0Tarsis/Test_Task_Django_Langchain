# Test Task: Django Langchain

## Preparation

### 1. Create a `.env` File
Rename sample-env to `.env` and add the following environment variables in the `.env` file:

- `POSTGRES_USER`   
- `POSTGRES_PASSWORD`   
- `POSTGRES_DB` 
- `POSTGRES_PORT`    
- `OPENAI_API_KEY`   

---

### 2. Build and Start the Application  
Run in project directory:
```bash
docker-compose up --build
```

---

### URLs
After starting the application, you can access the following:

- **Django Project:** [http://localhost:8000/](http://localhost:8000/)  
- **Swagger (API Documentation):** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)  
- **Streamlit App:** [http://localhost:8080/](http://localhost:8080/)  

---

## General Description

The project integrates several technologies for data scraping and background processing:

### Technologies Used:
- **Selenium**: Scrapes data from websites.  
- **Celery**: Manages background tasks, including data scraping.  
- **Celery-Beat**: Schedules periodic tasks automatically.  

### Features:
1. A Celery task is scheduled **once per hour** to scrape data.  
2. The scraping process can also be triggered **manually** via **Swagger** or **Streamlit**.  

### Permissions:
All API endpoints have permissions set to `AllowAny` to simplify testing during development.
