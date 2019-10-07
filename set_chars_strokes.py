from db import reset_char_strokes, conn

if __name__ == '__main__':
    reset_char_strokes()
    conn.close()
