import streamlit as st
import numpy as np
from PIL import Image

# Constants for the game
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '

# Function to check if a player has won
def check_win(board, player):
    # Check rows, columns, and diagonals
    for row in range(3):
        if all([cell == player for cell in board[row]]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

# Function to check if the game is a draw
def check_draw(board):
    return all([cell != EMPTY for row in board for cell in row])

# Minimax algorithm for AI (O)
def minimax(board, depth, is_maximizing):
    if check_win(board, PLAYER_O):
        return 10 - depth
    if check_win(board, PLAYER_X):
        return depth - 10
    if check_draw(board):
        return 0
    
    if is_maximizing:
        best = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER_O
                    best = max(best, minimax(board, depth + 1, False))
                    board[row][col] = EMPTY
        return best
    else:
        best = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER_X
                    best = min(best, minimax(board, depth + 1, True))
                    board[row][col] = EMPTY
        return best

# Function for AI to make a move
def ai_move(board):
    best_val = -float('inf')
    best_move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                board[row][col] = PLAYER_O
                move_val = minimax(board, 0, False)
                board[row][col] = EMPTY
                if move_val > best_val:
                    best_val = move_val
                    best_move = (row, col)
    return best_move

# Function to draw the board visually
def draw_board(board):
    img = Image.new("RGB", (300, 300), color=(255, 255, 255))
    for row in range(3):
        for col in range(3):
            color = (255, 255, 255)  # White background for cells
            if board[row][col] == PLAYER_X:
                img.paste(Image.open("x_image.png"), (col*100, row*100))  # Custom X image
            elif board[row][col] == PLAYER_O:
                img.paste(Image.open("o_image.png"), (col*100, row*100))  # Custom O image
    return img

# Main game loop
def main():
    st.title("Tic-Tac-Toe Game")
    st.markdown("Play against the AI! You are **X** and the AI is **O**.")
    
    # Initialize session state
    if "board" not in st.session_state:
        st.session_state.board = [[EMPTY] * 3 for _ in range(3)]
        st.session_state.game_over = False
        st.session_state.turn = PLAYER_X  # Player X starts first
    
    # Display the board
    img = draw_board(st.session_state.board)
    st.image(img)
    
    # Check if the game is over
    if st.session_state.game_over:
        if check_win(st.session_state.board, PLAYER_X):
            st.success("You win!")
        elif check_win(st.session_state.board, PLAYER_O):
            st.error("AI wins!")
        elif check_draw(st.session_state.board):
            st.warning("It's a draw!")
        return
    
    # User makes a move
    if st.session_state.turn == PLAYER_X:
        row = st.number_input("Choose row (0-2):", min_value=0, max_value=2, step=1)
        col = st.number_input("Choose column (0-2):", min_value=0, max_value=2, step=1)
        
        if st.button("Make move"):
            if st.session_state.board[row][col] == EMPTY:
                st.session_state.board[row][col] = PLAYER_X
                if check_win(st.session_state.board, PLAYER_X):
                    st.session_state.game_over = True
                else:
                    st.session_state.turn = PLAYER_O
                    ai_move_result = ai_move(st.session_state.board)
                    st.session_state.board[ai_move_result[0]][ai_move_result[1]] = PLAYER_O
                    if check_win(st.session_state.board, PLAYER_O):
                        st.session_state.game_over = True
                    else:
                        st.session_state.turn = PLAYER_X

# Run the game in Streamlit
if __name__ == "__main__":
    main()
