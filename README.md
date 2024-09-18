
```markdown
# Online Auction System

This project is an online auction system built using Django. The system allows users to participate in auctions, place bids in real-time, and automatically update the current price using WebSocket connections. Celery is used to handle background tasks like closing auctions when the time expires. Redis is used as the message broker for Celery and to manage WebSocket sessions.

## Features

- Real-time bidding using WebSockets
- Countdown timer for each auction
- User authentication and profile management
- Auto-incrementing bids based on a minimum bid increment
- Backend logic to validate bids
- Auctions automatically end when time runs out

## Requirements

- Python 3.x
- Django 3.x or later
- Redis
- Celery
- Channels (for WebSocket)
- PostgreSQL or MySQL (for the database)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/auction-system.git
cd auction-system
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Redis server

The system uses Redis to manage WebSocket communication and Celery tasks. Install and start the Redis server.

For Ubuntu:

```bash
sudo apt update
sudo apt install redis-server
```

Start Redis server:

```bash
sudo service redis-server start
```

Ensure Redis is running:

```bash
redis-cli ping
# You should see PONG if Redis is running successfully
```

### 5. Set up environment variables

Create a `.env` file in the project root and add the following environment variables:

```env
SECRET_KEY='your-secret-key'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1


# Redis and Celery configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CHANNEL_LAYERS_BACKEND=redis://localhost:6379/1
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Start Redis workers

Celery requires workers to process background tasks. In a separate terminal, run:

```bash
celery -A auction_system worker --loglevel=info
```

This starts the Celery worker, which will handle background tasks like closing auctions when they end.

You also need to start the Celery beat scheduler to run periodic tasks:

```bash
celery -A auction_system beat --loglevel=info
```

### 8. Start the Django development server

```bash
python manage.py runserver
```

### 9. Run the WebSocket server

The system uses Django Channels to handle WebSocket communication. Run the Channels server:

```bash
daphne -b 127.0.0.1 -p 8001 auction_system.asgi:application
```

## Usage

Once the server is running, users can browse auction listings, place bids, and see real-time updates when new bids are placed. The system will automatically notify users if they've been outbid or if the auction has ended.

### WebSocket Communication

The WebSocket connection handles real-time communication between the server and clients. Each auction has its own WebSocket URL that clients connect to in order to receive live bid updates.

### Celery and Redis

Celery is used to manage asynchronous tasks. Redis is the message broker that Celery relies on to queue and manage these tasks. For example, when an auction ends, a Celery task is scheduled to close the auction and notify the winner.



## Running Tests

You can run tests using the Django test runner:

```bash
python manage.py test
```



### To run the server in production:

1. Collect static files:

```bash
python manage.py collectstatic
```

2. Start the Django server and Celery workers as systemd services or using a process manager like Supervisor.



