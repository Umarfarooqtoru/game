import streamlit as st
import random

st.set_page_config(page_title="Tic Tac Toe - Ayan Shah vs AI")
st.title("Tic Tac Toe: Ayan Shah (X) vs AI (O)")

if 'board' not in st.session_state:
    st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
    st.session_state.turn = 'user'
    st.session_state.game_over = False
    st.session_state.message = ""

def check_winner(board, player):
    for i in range(3):
        if all([cell == player for cell in board[i]]):
            return True
        if all([board[j][i] == player for j in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

def ai_move(board):
    empty = get_empty_cells(board)
    if empty:
        row, col = random.choice(empty)
        board[row][col] = 'O'
        if check_winner(board, 'O'):
            st.session_state.game_over = True
            st.session_state.message = "AI wins! Better luck next time, Ayan Shah."
        elif not get_empty_cells(board):
            st.session_state.game_over = True
            st.session_state.message = "It's a draw!"
        else:
            st.session_state.turn = 'user'

def print_board(board):
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            cell = board[i][j]
            # Make the key unique by including cell value and turn
            btn_key = f"{i},{j}-{cell}-{st.session_state.turn}-{st.session_state.game_over}"
            if cell == ' ' and not st.session_state.game_over and st.session_state.turn == 'user':
                if cols[j].button(" ", key=btn_key):
                    board[i][j] = 'X'
                    if check_winner(board, 'X'):
                        st.session_state.game_over = True
                        st.session_state.message = "Congratulations Ayan Shah! You win!"
                    elif not get_empty_cells(board):
                        st.session_state.game_over = True
                        st.session_state.message = "It's a draw!"
                    else:
                        st.session_state.turn = 'ai'
            else:
                cols[j].button(cell, key=btn_key, disabled=True)

if st.button("Restart Game"):
    st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
    st.session_state.turn = 'user'
    st.session_state.game_over = False
    st.session_state.message = ""

print_board(st.session_state.board)

if st.session_state.turn == 'ai' and not st.session_state.game_over:
    ai_move(st.session_state.board)
    print_board(st.session_state.board)

if st.session_state.message:
    st.success(st.session_state.message)
