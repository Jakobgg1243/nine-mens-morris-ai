def print_board(state):
    b = state.board

    def p(pos):
        return b[pos] if b[pos] != " " else "·"   

    print("\n" + "=" * 65)
    print("                     Nine Men's Morris")
    print("=" * 65)

    print(f"        {p(0)} ---------------- {p(1)} ---------------- {p(2)}" + "        0 ---------------- 1 ---------------- 2")

    print("        |                  |                  |"*2)

    print(f"        |      {p(3)} --------- {p(4)} --------- {p(5)}      |" + "        |      3 --------- 4 --------- 5      |")

    print("        |      |           |           |      |"*2)

    print(f"        |      |     {p(6)} --- {p(7)} --- {p(8)}     |      |" + "        |      |     6 --- 7 --- 8     |      |")

    print("        |      |     |           |     |      |"*2)

    print(f"        {p(9)} ---- {p(10)} --- {p(11)}           {p(12)} --- {p(13)} ---- {p(14)}" + "        9 ---- 10 -- 11          12 -- 13 --- 14")

    print("        |      |     |           |     |      |"*2)

    print(f"        |      |     {p(15)} --- {p(16)} --- {p(17)}     |      |" + "        |      |     15 -- 16 -- 17    |      |")

    print("        |      |           |           |      |"*2)

    print(f"        |      {p(18)} --------- {p(19)} --------- {p(20)}      |" + "        |      18 -------- 19 -------- 20     |") 

    print("        |                  |                  |"*2)

    print(f"        {p(21)} ---------------- {p(22)} ---------------- {p(23)}" + "        21 --------------- 22 --------------- 23")

    print("=" * 65)
    print(f"Phase: {state.phase:<12} | Current Turn: {state.current_player}")
    print(f"X pieces on board: {state.on_board['X']}     O pieces on board: {state.on_board['O']}")
    print("=" * 65 + "\n")