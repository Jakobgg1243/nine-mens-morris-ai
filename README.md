# Nine Men's Morris AI

A Python implementation of the strategy game Nine Men's Morris featuring a minimax-based AI, multiple simulation modes, and a playable Streamlit web interface.

## Features
- Play Nine Men's Morris against an AI
- Minimax AI with alpha-beta pruning
- Game phases: placement, movement, and flying
- Mill detection and piece removal logic
- AI vs AI simulation mode
- AI vs Random and AI vs Greedy opponents
- Streamlit web version for browser play
- Optional pygame version for local desktop play

## AI Overview
The AI uses minimax search with alpha-beta pruning and a heuristic evaluation function based on:
- Material advantage (piece count)
- Mills and potential mills
- Mobility (available moves)
- Board control

Move ordering is used to improve search efficiency.

## Project Structure
src/nmm/
- game.py: Game state, rules, and phase logic  
- moves.py: Legal move generation and move application  
- minimax.py: AI search (minimax + alpha-beta pruning)  
- evaluation.py: Heuristic evaluation function  
- simulation.py: AI vs AI / AI vs other agents  

streamlit_app.py: Streamlit web interface  
main.py: Pygame-based local version  

## How to Run Locally

Clone the repository:
git clone https://github.com/Jakobgg1243/nine-mens-morris-ai.git  
cd nine-mens-morris-ai  

Install dependencies for Streamlit version:
pip install -r requirements.txt  

Run Streamlit app:
streamlit run streamlit_app.py  

(Optional) Install pygame for local version:
pip install pygame  

Run pygame version:
python main.py