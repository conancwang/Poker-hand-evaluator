from main import evaluation, parse_cards, equity

def cards(s):
    return [parse_cards(c) for c in s.split()]   

def test_pair():
    board = cards("3h 3d 6d Kh 9s Tc 5c")
    result = evaluation(board)
    assert result == (2, 3, 13, 10, 9)

def test_two_pair():
    board = cards("5h 5d Kd Kh 9s Tc 2c")
    result = evaluation(board)
    assert result == (3, 13, 5, 10)

def test_trips():
    board = cards("Td Th Tc 7h 3c 8s 6h")
    result = evaluation(board)
    assert result == (4, 10, 8, 7)

def test_straight():
    board = cards("Kh Kd As 2h 3d 4c 5h")
    result = evaluation(board)
    assert result == (5, 5)

def test_flush():
    board = cards("6h Kh Ah 2h 3d 4c 5h")
    result = evaluation(board)
    assert result == (6, 14, 13, 6, 5, 2)      

def test_fullhouse():
    board = cards("Td Th Tc 7h 3c 8s 7d")
    result = evaluation(board)
    assert result == (7, 10, 7)

def test_quads():
    board = cards("Qd Qh Qc Qs 3c 8s 7d")       
    result = evaluation(board)
    assert result == (8, 12, 8)

def test_straight_flush():
    board = cards("Kc Kd Ah 2h 3h 4h 5h")
    result = evaluation(board)
    assert result == (9, 5)