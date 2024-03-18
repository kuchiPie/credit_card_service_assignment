
# Credit Card Service

Credit Card Service to register user, apply loan, make payments, get statement and cron job for billing

# [Medium Article](https://medium.com/django-unleashed/assignment-for-backend-sde-intern-b0eb0ec72246) explaining the code:

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Make Sure Redis Server is up and running at port 6379

### Installation & Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/kuchiPie/credit_card_service.git
   ```

2. Create a Virtual Environment using your favroite tool.

3. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

4. Change Directory

   ```bash
   cd credit_card_service
   ```

5. Start Development Server

   ```bash
   python manage.py runserver
   ```

6. Start Celery Worker

   ```bash
   python -m celery -A credit_card_service worker -l info
   ```

7. Start Celery Beat

   ```bash
   python -m celery -A credit_card_service beat -l info
   ```

Access the project at [http://localhost:8000/](http://localhost:8000/).
