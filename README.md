# 1. Install the requirements locally
Navigate to project directory and run the below commands to install required packages

sudo apt install python3.11-venv
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

# 2. Server setup aand run using docker

docker build -t forex_trading_platform_api_server .
docker run -d -p 8081:8081 forex_trading_platform_api_server
