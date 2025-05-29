import streamlit as st
import random

st.set_page_config(page_title="Tic Tac Toe - Ayan Shah vs AI", page_icon="🎲", layout="centered")
st.markdown("""
    <style>
    .big-title { font-size: 3em; color: #ff9800; text-align: center; font-family: 'Comic Sans MS', cursive, sans-serif; }
    .winner { font-size: 2em; color: #4caf50; text-align: center; font-family: 'Comic Sans MS', cursive, sans-serif; }
    .draw { font-size: 2em; color: #2196f3; text-align: center; font-family: 'Comic Sans MS', cursive, sans-serif; }
    .cell-btn button { height: 80px !important; width: 80px !important; font-size: 2.5em !important; border-radius: 20px !important; background: #fffde7 !important; border: 3px solid #ff9800 !important; }
    .cell-btn button:disabled { background: #ffe0b2 !important; color: #bdbdbd !important; }
    </style>
""", unsafe_allow_html=True)
st.markdown('<div class="big-title">Tic Tac Toe 🎲<br><span style="font-size:0.7em;">Ayan Shah (X) vs AI (O)</span></div>', unsafe_allow_html=True)

if 'board' not in st.session_state:
    st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
    st.session_state.turn = 'user'
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.confetti = False

# Emoji for X and O
X_EMOJI = '❌'
O_EMOJI = '⭕'

# Fun background color for kids
st.markdown('<style>body {background-color: #fff8e1;}</style>', unsafe_allow_html=True)

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
            st.session_state.message = '<div class="winner">AI wins! Better luck next time, Ayan Shah. 🤖</div>'
        elif not get_empty_cells(board):
            st.session_state.game_over = True
            st.session_state.message = '<div class="draw">It\'s a draw! 😃</div>'
        else:
            st.session_state.turn = 'user'

def print_board(board):
    for i in range(3):
        cols = st.columns(3, gap="large")
        for j in range(3):
            cell = board[i][j]
            btn_key = f"{i},{j}-{cell}-{st.session_state.turn}-{st.session_state.game_over}"
            display = X_EMOJI if cell == 'X' else (O_EMOJI if cell == 'O' else ' ')
            if cell == ' ' and not st.session_state.game_over and st.session_state.turn == 'user':
                with cols[j]:
                    if st.button(display, key=btn_key, help=f"Place {X_EMOJI} here", use_container_width=True, type="primary"):
                        board[i][j] = 'X'
                        if check_winner(board, 'X'):
                            st.session_state.game_over = True
                            st.session_state.message = '<div class="winner">Congratulations Ayan Shah! You win! 🎉</div>'
                            st.session_state.confetti = True
                        elif not get_empty_cells(board):
                            st.session_state.game_over = True
                            st.session_state.message = '<div class="draw">It\'s a draw! 😃</div>'
                        else:
                            st.session_state.turn = 'ai'
            else:
                with cols[j]:
                    st.button(display, key=btn_key+"-disabled", disabled=True, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 Restart Game", use_container_width=True):
    st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
    st.session_state.turn = 'user'
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.confetti = False

print_board(st.session_state.board)

if st.session_state.turn == 'ai' and not st.session_state.game_over:
    ai_move(st.session_state.board)
    print_board(st.session_state.board)

if st.session_state.message:
    st.markdown(st.session_state.message, unsafe_allow_html=True)
    if st.session_state.confetti:
        st.balloons()

st.markdown("""
---
<div style='text-align:center; color:#ff9800; font-family: "Comic Sans MS", cursive, sans-serif;'>
Have fun playing, kids! 😃🎈
</div>
""", unsafe_allow_html=True)
