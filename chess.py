class ChessBoard:
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.current_player = 'white'
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_kingside_rook_moved = False
        self.white_queenside_rook_moved = False
        self.black_kingside_rook_moved = False
        self.black_queenside_rook_moved = False
        self.en_passant = None
        self.move_history = []

    def print_board(self):
        for row in self.board:
            print(' '.join(row))

    def is_valid_square(self, row, col):
        return row >= 0 and row <= 7 and col >= 0 and col <= 7

    def is_valid_pawn_move(self, start_row, start_col, end_row, end_col):
        direction = -1 if self.current_player == 'white' else 1
        if start_col == end_col:
            if self.board[end_row][end_col] != '.':
                return False
            if start_row + direction == end_row:
                return True
            if start_row + 2 * direction == end_row and start_row == (6 if self.current_player == 'white' else 1) and self.board[end_row - direction][end_col] == '.':
                return True
        else:
            if abs(start_col - end_col) != 1 or start_row + direction != end_row:
                return False
            if self.board[end_row][end_col] != '.':
                return True
            if self.en_passant and end_row == self.en_passant[0] and end_col == self.en_passant[1]:
                return True

        return False

    def is_valid_knight_move(self, start_row, start_col, end_row, end_col):
        return abs(end_row - start_row) == 2 and abs(end_col - start_col) == 1 or abs(end_row - start_row) == 1 and abs(end_col - start_col) == 2

    def is_valid_bishop_move(self, start_row, start_col, end_row, end_col):
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False

        row_direction = 1 if end_row > start_row else -1
        col_direction = 1 if end_col > start_col else -1
        row, col = start_row + row_direction, start_col + col_direction

        while row != end_row and col != end_col:
            if self.board[row][col] != '.':
                return False
            row += row_direction
            col += col_direction

        return True

    def is_valid_rook_move(self, start_row, start_col, end_row, end_col):
            def is_valid_rook_move(self, start_row, start_col, end_row, end_col):
        if start_row != end_row and start_col != end_col:
            return False

        if start_row == end_row:
            direction = 1 if end_col > start_col else -1
            col = start_col + direction
            while col != end_col:
                if self.board[start_row][col] != '.':
                    return False
                col += direction
        else:
            direction = 1 if end_row > start_row else -1
            row = start_row + direction
            while row != end_row:
                if self.board[row][start_col] != '.':
                    return False
                row += direction

        return True

    def is_valid_queen_move(self, start_row, start_col, end_row, end_col):
        return self.is_valid_rook_move(start_row, start_col, end_row, end_col) or self.is_valid_bishop_move(start_row, start_col, end_row, end_col)

    def is_valid_king_move(self, start_row, start_col, end_row, end_col):
        if abs(start_row - end_row) > 1 or abs(start_col - end_col) > 1:
            if self.current_player == 'white' and not self.white_king_moved:
                if end_row == 0 and end_col == 6 and self.board[0][5] == '.' and self.board[0][6] == '.' and not self.is_in_check() and not self.is_under_attack(0, 4) and not self.is_under_attack(0, 5):
                    return True
                elif end_row == 0 and end_col == 2 and self.board[0][1] == '.' and self.board[0][2] == '.' and self.board[0][3] == '.' and not self.is_in_check() and not self.is_under_attack(0, 4) and not self.is_under_attack(0, 3):
                    return True
            elif self.current_player == 'black' and not self.black_king_moved:
                if end_row == 7 and end_col == 6 and self.board[7][5] == '.' and self.board[7][6] == '.' and not self.is_in_check() and not self.is_under_attack(7, 4) and not self.is_under_attack(7, 5):
                    return True
                elif end_row == 7 and end_col == 2 and self.board[7][1] == '.' and self.board[7][2] == '.' and self.board[7][3] == '.' and not self.is_in_check() and not self.is_under_attack(7, 4) and not self.is_under_attack(7, 3):
                    return True
            return False

        return True

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        if piece == '.' or (piece.isupper() and self.current_player == 'black') or (piece.islower() and self.current_player == 'white'):
            return False

        if piece.lower() == 'p':
            if not self.is_valid_pawn_move(start_row, start_col, end_row, end_col):
                return False
        elif piece.lower() == 'n':
            if not self.is_valid_knight_move(start_row, start_col, end_row, end_col):
                return False
        elif piece.lower() == 'b':
                        if not self.is_valid_bishop_move(start_row, start_col, end_row, end_col):
                return False
        elif piece.lower() == 'r':
            if not self.is_valid_rook_move(start_row, start_col, end_row, end_col):
                return False
        elif piece.lower() == 'q':
            if not self.is_valid_queen_move(start_row, start_col, end_row, end_col):
                return False
        elif piece.lower() == 'k':
            if not self.is_valid_king_move(start_row, start_col, end_row, end_col):
                return False
        else:
            return False

        # check if move causes check to current player's own king
        if self.is_in_check_after_move(start_row, start_col, end_row, end_col):
            return False

        return True

    def is_in_check(self):
        king_row, king_col = self.find_king(self.current_player)
        return self.is_under_attack(king_row, king_col)

    def is_under_attack(self, row, col):
        # check if any opponent's piece can attack this position
        opponent = 'black' if self.current_player == 'white' else 'white'
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != '.' and self.board[r][c].lower() != 'k' and self.board[r][c].islower() == (opponent == 'white'):
                    if self.is_valid_move(r, c, row, col):
                        return True
        return False

    def is_in_check_after_move(self, start_row, start_col, end_row, end_col):
        temp_board = copy.deepcopy(self.board)
        temp_board[end_row][end_col] = temp_board[start_row][start_col]
        temp_board[start_row][start_col] = '.'

        return self.is_under_attack(self.find_king(self.current_player)[0], self.find_king(self.current_player)[1])

    def find_king(self, player):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == 'K' and player == 'white':
                    return r, c
                elif self.board[r][c] == 'k' and player == 'black':
                    return r, c

    def is_draw_by_insufficient_material(self):
        # check if there are only kings or kings and knights on the board
        pieces = set()
        for row in self.board:
            for piece in row:
                if piece != '.':
                    pieces.add(piece)
                    if pieces == {'k', 'K'} or pieces == {'k', 'K', 'n'} or pieces == {'k', 'K', 'N'}:
                        return True
        return False

    def is_draw_by_stalemate(self):
        # current player is not in check and cannot make any move
        if not self.is_in_check() and not any(self.is_valid_move(r, c, r2, c2) for r in range(8) for c in range(8) for r2 in range(8) for c2 in range(8)):
            return True
        return False

    def is_draw_by_threefold_repetition(self):
        # check if the current board state has appeared 3 times already
        count = 0
        for state in self.board_history:
            if state == self.board:
                count += 1
        if count >= 3:
            return True
        return False

                if not self.is_valid_bishop_move(start_row, start_col, end_row, end_col):
                return False
        elif piece.lower() == 'r':
            if not self.is_valid_rook_move(start_row, start_col, end_row, end_col):
                return False
        elif piece.lower() == 'q':
            if not self.is_valid_queen_move(start_row, start_col, end_row, end_col):
                return False
        elif piece.lower() == 'k':
            if not self.is_valid_king_move(start_row, start_col, end_row, end_col):
                return False
        else:
            return False

        # check if move causes check to current player's own king
        if self.is_in_check_after_move(start_row, start_col, end_row, end_col):
            return False

        return True

    def is_in_check(self):
        king_row, king_col = self.find_king(self.current_player)
        return self.is_under_attack(king_row, king_col)

    def is_under_attack(self, row, col):
        # check if any opponent's piece can attack this position
        opponent = 'black' if self.current_player == 'white' else 'white'
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != '.' and self.board[r][c].lower() != 'k' and self.board[r][c].islower() == (opponent == 'white'):
                    if self.is_valid_move(r, c, row, col):
                        return True
        return False

    def is_in_check_after_move(self, start_row, start_col, end_row, end_col):
        temp_board = copy.deepcopy(self.board)
        temp_board[end_row][end_col] = temp_board[start_row][start_col]
        temp_board[start_row][start_col] = '.'

        return self.is_under_attack(self.find_king(self.current_player)[0], self.find_king(self.current_player)[1])

    def find_king(self, player):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == 'K' and player == 'white':
                    return r, c
                elif self.board[r][c] == 'k' and player == 'black':
                    return r, c

    def is_draw_by_insufficient_material(self):
        # check if there are only kings or kings and knights on the board
        pieces = set()
        for row in self.board:
            for piece in row:
                if piece != '.':
                    pieces.add(piece)
                    if pieces == {'k', 'K'} or pieces == {'k', 'K', 'n'} or pieces == {'k', 'K', 'N'}:
                        return True
        return False

    def is_draw_by_stalemate(self):
        # current player is not in check and cannot make any move
        if not self.is_in_check() and not any(self.is_valid_move(r, c, r2, c2) for r in range(8) for c in range(8) for r2 in range(8) for c2 in range(8)):
            return True
        return False

    def is_draw_by_threefold_repetition(self):
        # check if the current board state has appeared 3 times already
        count = 0
        for state in self.board_history:
            if state == self.board:
                count += 1
        if count >= 3:
            return True
        return False

        def is_game_over(self):
        if self.is_checkmate():
            print(f"CHECKMATE! {self.current_player.capitalize()} wins!")
            return True
        elif self.is_draw_by_insufficient_material():
            print("Draw by insufficient material.")
            return True
        elif self.is_draw_by_stalemate():
            print("Stalemate. Draw!")
            return True
        elif self.is_draw_by_threefold_repetition():
            print("Draw by threefold repetition.")
            return True
        return False

    def is_checkmate(self):
        return self.is_in_check() and not any(self.is_valid_move(r, c, r2, c2) for r in range(8) for c in range(8) for r2 in range(8) for c2 in range(8) if self.board[r][c] != '.')

    def make_move(self, start_row, start_col, end_row, end_col):
        if not self.is_valid_move(start_row, start_col, end_row, end_col):
            return False

        self.board_history.append(copy.deepcopy(self.board))
        piece = self.board[start_row][start_col]
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = '.'

        # handle pawn promotion
        if piece.lower() == 'p' and end_row in [0, 7]:
            self.board[end_row][end_col] = input("Enter the promoted piece (Q/R/B/N): ")

        # handle en passant capture
        if piece.lower() == 'p' and end_col != start_col and self.board[end_row][end_col] == '.':
            self.board[start_row][end_col] = '.'

        # handle castling
        if piece.lower() == 'k' and abs(end_col - start_col) == 2:
            if end_col > start_col:
                self.board[start_row][7] = '.'
                self.board[start_row][end_col-1] = 'R'
            else:
                self.board[start_row][0] = '.'
                self.board[start_row][end_col+1] = 'R'

        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True




