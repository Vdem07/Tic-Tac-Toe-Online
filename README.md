# Tic-Tac-Toe-Online
Tic-Tac-Toe-Online is a simple 1-on-1 multiplayer Tic-Tac-Toe game with online play support.

# Features
1. Online 1v1 gameplay.
2. Automatic opponent pairing.
3. Colorful UI using Tkinter.
4. Works over local network or the internet (e.g., via Radmin VPN).

# Requirements
Python 3.x

# Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/Tic-Tac-Toe-Online.git
```
```
cd Tic-Tac-Toe-Online
```
2. Install dependencies (if necessary):
```
pip install tkinter
```
# Running the Game

## Local Network Play

1. Start the server:
```
python server.py
```
2. Start the client (can be on another device):
```
python client.py
```
3. Enter the server's IP address when prompted by the client.

## Remote Play via the Internet
1. Install Radmin VPN (or another VPN tool) on both devices.
2. Connect both devices to the same Radmin VPN network.
3. Start the server on one device.
4. Start the client and enter the server's IP address (found in Radmin VPN).

# Automatic Server and Client Startup
Run _run.py_ to automatically launch both the server and the client:
```
python run.py
```

# License
This project is licensed under the MIT license.
