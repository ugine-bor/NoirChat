# NoirChat: Simple and Focused Communication

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-username/noirchat)
[![Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20Linux%20%7C%20I2P-lightgrey.svg)](https://github.com/your-username/noirchat)

**Welcome to NoirChat** - a minimalist and private web chat designed for straightforward and secure communication. It is lightweight, fast, and designed for easy deployment on your system, whether Windows, Linux, or within the anonymous I2P network.

**Demo:** [Demo link here if available]

## Features

* **Real-time Instant Messaging:** Facilitates communication with minimal latency through WebSocket technology.
* **Simplicity and Minimalism:** A clean interface focused solely on core communication functionalities.
* **Privacy Focused:** Easily deployable on a private server or within I2P for enhanced privacy.
* **Cross-Platform Compatibility:** Operates on Windows and Linux, with a specific version optimized for I2P.
* **Configurable:** Settings are managed through environment variables (`.env`).
* **Rate Limiting:** Integrated protection against spam and message flooding.
* **Security Measures:** Implements CSP, X-Content-Type-Options, and X-Frame-Options headers for enhanced security.
* **Message History:** Retains the most recent 100 messages.
* **Adaptive Text Input:**  Input field height dynamically adjusts to text content.
* **Favicon Generation:** Dynamically generated favicon.

## Getting Started

### Prerequisites

Before installation, ensure the following components are installed:

* **Python 3.x**
* **pip** (Python package installer)
* **Redis** (in-memory data structure store) - required for session management and rate limiting.
* **Node.js and npm** (for `socket.io.js` if local installation is preferred).

### Installation and Setup

Choose the version appropriate for your operating system:

**Windows Version**

#### Windows Installation Steps

1. **Clone the repository:**
   ```bash
   git clone [Your Repository URL]
   cd noirchat
   ```

2. **Create a Python virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
    * Copy `.env.example` to `.env`.
    * Edit `.env` to specify required settings (secret key, Redis ports, message sizes, etc.).
    * **It is crucial to set `KEY` in `.env` to a strong, randomly generated string.**

5. **Start the Redis server:**
    * Ensure the Redis server is running and accessible on the port specified in `.env` (default is `6379`).
    * Redis for Windows can be downloaded from
      the [official Redis website](https://redis.io/docs/getting-started/installation/installing-redis-on-windows/).

6. **Launch NoirChat:**
   ```bash
   run.bat
   ```

7. **Access NoirChat in a web browser:**
    * Navigate to `http://localhost:[MAIN_PORT]` (default port is `5000` unless modified in `.env`).

#### `run.bat` for Windows

```batch
@echo off
setlocal

REM Activate virtual environment if not already active
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call venv\Scripts\activate
)

echo Starting NoirChat...
python main.py

endlocal
```


**Linux Version**

#### Linux Installation Steps

1. **Clone the repository:**
   ```bash
   git clone [Your Repository URL]
   cd noirchat
   ```

2. **Create a Python virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
    * Copy `.env.example` to `.env`.
    * Edit `.env` to specify required settings (secret key, Redis ports, message sizes, etc.).
    * **It is crucial to set `KEY` in `.env` to a strong, randomly generated string.**

5. **Start the Redis server:**
    * Ensure the Redis server is running and accessible on the port specified in `.env` (default is `6379`).
    * Install Redis if not already installed using your system's package manager (
      e.g., `sudo apt-get install redis-server` for Debian/Ubuntu).

6. **Launch NoirChat:**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

7. **Access NoirChat in a web browser:**
    * Navigate to `http://localhost:[MAIN_PORT]` (default port is `5000` unless modified in `.env`).

#### `run.sh` for Linux

```bash
#!/bin/bash

# Activate virtual environment if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Starting NoirChat..."
python3 main.py
```


**Linux I2P Version**

#### Linux I2P Installation Steps

**Important:** This version is intended for running NoirChat within the anonymous I2P network. Ensure you have the I2P
router installed and configured before proceeding.

1. **Follow the Linux installation steps (above):**
    * Complete the instructions in the "Linux Version" section to install dependencies and create a virtual environment.

2. **Configure environment variables for I2P:**
    * In the `.env` file, modify the following variables:
        * `HOST=127.0.0.1` (or `0.0.0.0` if chat access is needed from within I2P but not from the local machine).
        * `MAIN_PORT=[choose a free port, e.g., 7000]` (or another port that does not conflict with other I2P services).
        * **Ensure `REDIS_PORT` and `REDIS_HOST` match your Redis server settings if it is running within I2P.**

3. **Start the Redis server in I2P (optional, for local Redis in I2P):**
    * Configure and run a Redis server if you intend to use it locally within your I2P environment. For simplicity, it's
      often feasible to use a Redis instance running outside I2P, but consider the privacy implications.

4. **Launch NoirChat for I2P:**
   ```bash
   chmod +x run_i2p.sh
   ./run_i2p.sh
   ```

5. **Access NoirChat in an I2P browser:**
    * Use a browser configured for I2P (e.g., the I2P browser or Tor Browser with I2P proxy settings).
    * Navigate to `http://[your I2P domain name].i2p:[MAIN_PORT]` (or `http://127.0.0.1:[MAIN_PORT]` for local testing).

#### `run_i2p.sh` for Linux I2P

```bash
#!/bin/bash

# Activate virtual environment if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Starting NoirChat in I2P mode..."
python3 main.py
```

**Important for I2P:**

* **Privacy:** Running within I2P enhances privacy, but understanding I2P's operation and properly configuring your
  router and browser is essential.
* **Performance:** Performance within I2P may be slower compared to a standard network.
* **Accessibility:** For other I2P users to access your chat, you need to configure I2P hosting and publicize
  your `.i2p` domain.


## Configuration

NoirChat is configured via environment variables, set in the `.env` file.

| Variable         | Description                                        | Default Value                                                      |
|------------------|----------------------------------------------------|--------------------------------------------------------------------|
| `KEY`            | Flask secret key for token signing                 | `your_default_secret_key` (must be changed)                        |
| `HOST`           | IP address to bind the server to                   | `0.0.0.0`                                                          |
| `MAIN_PORT`      | Port for the web server and WebSocket              | `5000`                                                             |
| `REDIS_HOST`     | Redis server hostname                              | `127.0.0.1`                                                        |
| `REDIS_PORT`     | Redis server port                                  | `6379`                                                             |
| `REDIS_PASS`     | Redis server password (if any)                     | `None`                                                             |
| `REDIS_SERVER`   | Path to the Redis server executable                | `redis-server`                                                     |
| `REDIS_CONF`     | Path to the Redis server configuration file        | `redis.conf`                                                       |
| `REDIS_DUMP`     | Filename for Redis database dump                   | `dump.rdb`                                                         |
| `MESSAGE_SIZE`   | Maximum message size in characters                 | `500`                                                              |
| `MESSAGE_EXPIRE` | Time-to-live for rate limits in Redis (in seconds) | `60`                                                               |
| `COOKIE_LIFE`    | Token cookie expiration time (in seconds)          | `86400` (1 day)                                                    |
| `RATE_LIMITS`    | JSON array for rate limiting rules                 | `[[60, 10], [300, 50]]` (10 messages per minute, 50 per 5 minutes) |

**To modify configuration:**

1. Copy `.env.example` to `.env`.
2. Edit `.env` with any text editor.
3. Restart NoirChat for changes to take effect.

## Contact

No contact ¯\_(ツ)_/¯

---

Thank you for using NoirChat.