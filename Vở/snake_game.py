import os
import time
import random
import msvcrt  # Thư viện này chỉ dùng trên Windows để đọc phím ngay lập tức

# --- Cấu hình Game ---
WIDTH = 40  # Chiều rộng khu vực chơi
HEIGHT = 15 # Chiều cao khu vực chơi
INIT_SPEED = 0.1 # Tốc độ ban đầu (giây)

# --- Khởi tạo ---
class SnakeGame:
    def __init__(self):
        # Thiết lập khu vực chơi
        self.width = WIDTH
        self.height = HEIGHT
        
        # Khởi tạo rắn ở giữa
        start_y = HEIGHT // 2
        start_x = WIDTH // 4
        self.snake = [[start_y, start_x], [start_y, start_x - 1]]
        
        # Hướng di chuyển ban đầu (1: phải, 2: trái, 3: lên, 4: xuống)
        self.direction = 1 
        
        # Khởi tạo điểm số
        self.score = 0
        
        # Tạo thức ăn
        self.food = self.create_food()
        
        # Tốc độ game
        self.delay = INIT_SPEED

    def create_food(self):
        """Tạo thức ăn ở vị trí ngẫu nhiên không trùng với thân rắn"""
        while True:
            y = random.randint(1, self.height - 2)
            x = random.randint(1, self.width - 2)
            if [y, x] not in self.snake:
                return [y, x]

    def clear_screen(self):
        """Xóa màn hình console"""
        # Kiểm tra hệ điều hành: 'nt' là Windows, 'posix' là Linux/macOS
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_game(self):
        """Vẽ toàn bộ khung game, rắn và thức ăn"""
        self.clear_screen()
        
        # Tạo khung lưới trống
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]

        # Vẽ biên
        for x in range(self.width):
            grid[0][x] = '#'
            grid[self.height - 1][x] = '#'
        for y in range(self.height):
            grid[y][0] = '#'
            grid[y][self.width - 1] = '#'
        
        # Vẽ thức ăn
        grid[self.food[0]][self.food[1]] = '*'

        # Vẽ rắn
        for i, (y, x) in enumerate(self.snake):
            # Đầu rắn 'O', thân rắn 'o'
            grid[y][x] = 'O' if i == 0 else 'o'
        
        # Hiển thị tất cả lên màn hình
        output = "\n".join("".join(row) for row in grid)
        print(output)
        print(f"Score: {self.score} | Speed: {self.delay:.3f}s")

    def get_user_input(self):
        """Đọc phím bấm mà không cần nhấn Enter (Chỉ hoạt động trên Windows)"""
        if msvcrt.kbhit():
            key = msvcrt.getch()
            try:
                # Xử lý các phím mũi tên (chúng thường là 2 byte, bắt đầu bằng b'\xe0')
                if key == b'\xe0':
                    key = msvcrt.getch()
                    if key == b'H' and self.direction != 4: # Mũi tên lên
                        self.direction = 3
                    elif key == b'P' and self.direction != 3: # Mũi tên xuống
                        self.direction = 4
                    elif key == b'K' and self.direction != 1: # Mũi tên trái
                        self.direction = 2
                    elif key == b'M' and self.direction != 2: # Mũi tên phải
                        self.direction = 1
                
                # Có thể thêm phím 'q' để thoát
                elif key == b'q':
                    return True # Trả về True để kết thúc game

            except Exception:
                pass
        return False

    def update_snake(self):
        """Tính toán vị trí đầu rắn mới dựa trên hướng di chuyển"""
        head_y, head_x = self.snake[0]
        
        # 1: phải (+x), 2: trái (-x), 3: lên (-y), 4: xuống (+y)
        if self.direction == 1:
            head_x += 1
        elif self.direction == 2:
            head_x -= 1
        elif self.direction == 3:
            head_y -= 1
        elif self.direction == 4:
            head_y += 1
            
        new_head = [head_y, head_x]
        
        # 1. Kiểm tra va chạm biên
        if (new_head[0] <= 0 or new_head[0] >= self.height - 1 or
            new_head[1] <= 0 or new_head[1] >= self.width - 1):
            return True # Game Over
            
        # 2. Kiểm tra va chạm chính mình
        if new_head in self.snake:
            return True # Game Over

        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.score += 10
            self.food = self.create_food()
            if self.delay > 0.03:
                self.delay -= 0.005
        else:
            self.snake.pop()
            
        return False 
    def run(self):
        """Vòng lặp chính của Game"""
        game_over = False
        
        while not game_over:
            self.draw_game()
            
            if self.get_user_input():
                break # Thoát nếu nhấn 'q'

            game_over = self.update_snake()
        
            time.sleep(self.delay)

        self.clear_screen()
        print("#" * self.width)
        print(f"|{'GAME OVER'.center(self.width - 2)}|")
        print(f"|{'Final Score:'.center(self.width - 2)}|")
        print(f"|{str(self.score).center(self.width - 2)}|")
        print("#" * self.width)
        time.sleep(5) # Chờ 5 giây

if __name__ == "__main__":
    if os.name != 'nt':
        print("Lỗi: Phiên bản game này cần thư viện 'msvcrt', chỉ chạy trên Windows.")
        print("Vui lòng sử dụng lại phiên bản 'curses' nếu bạn dùng Linux/macOS.")
    else:
        game = SnakeGame()
        game.run()