import tkinter as tk  # tkinter 라이브러리를 임포트하여 GUI를 생성

# 다양한 글꼴 스타일 정의
LARGE_FONT_STYLE = ("Arial", 40, "bold")  # 큰 글꼴 스타일
SMALL_FONT_STYLE = ("Arial", 16)  # 작은 글꼴 스타일
DIGITS_FONT_STYLE = ("Arial", 24, "bold")  # 숫자 글꼴 스타일
DEFAULT_FONT_STYLE = ("Arial", 20)  # 기본 글꼴 스타일

# 색상 정의
OFF_WHITE = "#F8FAFF"  # 연한 흰색
WHITE = "#FFFFFF"  # 흰색
LIGHT_BLUE = "#CCEDFF"  # 연한 파란색
LIGHT_GRAY = "#F5F5F5"  # 연한 회색
LABEL_COLOR = "#25265E"  # 라벨 글자 색상

class Calculator:
    def __init__(self):
        # 윈도우 설정
        self.window = tk.Tk()  # tkinter의 Tk 클래스를 사용하여 윈도우 생성
        self.window.geometry("1000x667")  # 윈도우 크기 설정
        self.window.resizable(0, 0)  # 윈도우 크기 조정 불가
        self.window.title("Calculator")  # 윈도우 제목 설정

        # 초기 상태 설정
        self.total_expression = ""  # 전체 수식
        self.current_expression = ""  # 현재 입력한 수식
        self.display_frame = self.create_display_frame()  # 디스플레이 프레임 생성

        # 레이블 생성 (수식 표시용)
        self.total_label, self.label = self.create_display_labels()

        # 숫자 버튼의 위치를 지정하는 딕셔너리
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),  # 7, 8, 9 숫자 버튼 위치
            4: (2, 1), 5: (2, 2), 6: (2, 3),  # 4, 5, 6 숫자 버튼 위치
            1: (3, 1), 2: (3, 2), 3: (3, 3),  # 1, 2, 3 숫자 버튼 위치
            0: (4, 2), '.': (4, 1)  # 0, '.' 숫자 버튼 위치
        }

        # 연산자 버튼 딕셔너리 (기호 변환)
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}  # 연산자 기호 설정

        # 단위 버튼 위치 설정
        self.unit_buttons = {
            'cm': (1, 5), 'm': (2, 5),  # cm와 m 단위 버튼
            'g': (3, 5), 'kg': (4, 5)  # g와 kg 단위 버튼
        }

        # 단위 변환 버튼 설정
        self.convert_buttons = {
            'cm → m': (1, 6), 'm → cm': (2, 6),  # cm과 m 단위 변환 버튼
            'g → kg': (3, 6), 'kg → g': (4, 6),  # g와 kg 단위 변환 버튼
            'mm → m': (1, 7), 'm → mm': (2, 7),  # mm와 m 단위 변환
            'nm → m': (3, 7), 'm → nm': (4, 7),  # nm와 m 단위 변환
            'µm → m': (1, 8), 'm → µm': (2, 8)   # µm과 m 단위 변환
        }

        # 버튼을 배치할 프레임 생성
        self.buttons_frame = self.create_buttons_frame()

        # 버튼 그리드의 행과 열 가중치 설정
        self.buttons_frame.rowconfigure(0, weight=1)  # 첫 번째 행 가중치 설정
        for x in range(1, 5):  # 두 번째부터 네 번째 행에 가중치 설정
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)  # 첫 번째부터 네 번째 열에 가중치 설정

        # 숫자 버튼, 연산자 버튼, 단위 버튼 생성
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_unit_buttons()  # 단위 버튼 생성
        self.create_special_buttons()  # 특수 버튼 생성
        self.bind_keys()  # 키 바인딩

    # 키보드 입력을 계산기 버튼과 연결하는 함수
    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())  # Enter 키로 계산
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))  # 숫자 키

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))  # 연산자 키

    # 특수 기능 버튼을 생성하는 함수 (초기화, 계산, 제곱, 제곱근)
    def create_special_buttons(self):
        self.create_clear_button()  # 초기화 버튼
        self.create_equals_button()  # 계산 버튼
        self.create_square_button()  # 제곱 버튼
        self.create_sqrt_button()  # 제곱근 버튼

    # 디스플레이 레이블을 생성하는 함수
    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)  # 전체 수식 라벨
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)  # 현재 입력한 수식 라벨
        label.pack(expand=True, fill='both')

        return total_label, label  # 라벨 반환

    # 디스플레이용 프레임을 생성하는 함수
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)  # 디스플레이 프레임
        frame.pack(expand=True, fill="both")
        return frame

    # 숫자 버튼을 클릭했을 때 수식에 숫자를 추가하는 함수
    def add_to_expression(self, value):
        self.current_expression += str(value)  # 숫자 추가
        self.update_label()  # 레이블 업데이트

    # 숫자 버튼을 생성하는 함수
    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():  # 숫자 버튼을 행, 열에 맞게 생성
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))  # 버튼 클릭 시 수식에 숫자 추가
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)  # 버튼 그리드 배치

    # 연산자를 추가하는 함수
    def append_operator(self, operator):
        self.current_expression += operator  # 연산자 추가
        self.total_expression += self.current_expression  # 전체 수식에 추가
        self.current_expression = ""  # 현재 수식 초기화
        self.update_total_label()  # 전체 수식 라벨 업데이트
        self.update_label()  # 현재 수식 라벨 업데이트

    # 연산자 버튼을 생성하는 함수
    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():  # 연산자 버튼 생성
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))  # 버튼 클릭 시 연산자 추가
            button.grid(row=i, column=4, sticky=tk.NSEW)  # 버튼 그리드 배치
            i += 1

    # 수식을 초기화하는 함수
    def clear(self):
        self.current_expression = ""  # 현재 수식 초기화
        self.total_expression = ""  # 전체 수식 초기화
        self.update_label()  # 레이블 업데이트
        self.update_total_label()  # 전체 수식 라벨 업데이트

    # 초기화 버튼을 생성하는 함수
    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)  # C 버튼
        button.grid(row=0, column=1, sticky=tk.NSEW)  # 버튼 배치

    # 제곱 연산을 수행하는 함수
    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))  # 제곱 연산
        self.update_label()  # 레이블 업데이트

    # 제곱 버튼을 생성하는 함수
    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)  # 제곱 버튼
        button.grid(row=0, column=2, sticky=tk.NSEW)  # 버튼 배치

    # 제곱근 연산을 수행하는 함수
    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))  # 제곱근 연산
        self.update_label()  # 레이블 업데이트

    # 제곱근 버튼을 생성하는 함수
    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)  # 제곱근 버튼
        button.grid(row=0, column=3, sticky=tk.NSEW)  # 버튼 배치

    # 수식을 계산하고 결과를 표시하는 함수
    def evaluate(self):
        self.total_expression += self.current_expression  # 전체 수식에 현재 수식 추가
        self.update_total_label()  # 전체 수식 라벨 업데이트
        try:
            self.current_expression = str(eval(self.total_expression))  # 수식 계산
            self.total_expression = ""  # 수식 초기화
        except Exception as e:
            self.current_expression = "Error"  # 계산 오류 발생 시 "Error" 표시
        finally:
            self.update_label()  # 레이블 업데이트

    # 계산 결과 버튼을 생성하는 함수
    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)  # 계산 버튼
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)  # 버튼 배치

    # 버튼을 배치할 프레임을 생성하는 함수
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)  # 버튼을 배치할 프레임
        frame.pack(expand=True, fill="both")
        return frame

    # 전체 수식 라벨을 업데이트하는 함수
    def update_total_label(self):
        expression = self.total_expression  # 전체 수식
        for operator, symbol in self.operations.items():  # 연산자 표시 변경
            expression = expression.replace(operator, f' {symbol} ')  # 연산자 기호 변경
        self.total_label.config(text=expression)  # 전체 수식 라벨 업데이트

    # 현재 수식 라벨을 업데이트하는 함수
    def update_label(self):
        self.label.config(text=self.current_expression[:11])  # 현재 수식의 최대 길이를 11로 제한하여 표시

    # 메인 루프를 실행하는 함수
    def run(self):
        self.window.mainloop()  # tkinter 메인 루프 실행

    # 단위 버튼과 변환 버튼을 생성하는 함수
    def create_unit_buttons(self):
        for unit, (row, col) in self.unit_buttons.items():  # 단위 버튼 생성
            button = tk.Button(self.buttons_frame, text=unit, bg=WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=unit: self.add_to_expression(x))  # 버튼 클릭 시 단위 추가
            button.grid(row=row, column=col, sticky=tk.NSEW)  # 버튼 배치

        # 단위 변환 버튼들
        for text, (row, col) in self.convert_buttons.items():  # 변환 버튼 생성
            button = tk.Button(self.buttons_frame, text=text, bg=WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=text: self.handle_conversion(x))  # 변환 버튼 클릭 시 처리
            button.grid(row=row, column=col, sticky=tk.NSEW)  # 버튼 배치

    # 단위 변환을 처리하는 함수
    def handle_conversion(self, conversion_type):
        if conversion_type == 'cm → m':
            if 'cm' in self.current_expression:
                value = float(self.current_expression.replace('cm', ''))  # cm 값을 추출하고 변환
                self.current_expression = str(value / 100) + ' m'  # cm → m 변환
        elif conversion_type == 'm → cm':
            if 'm' in self.current_expression:
                value = float(self.current_expression.replace('m', ''))  # m 값을 추출하고 변환
                self.current_expression = str(value * 100) + ' cm'  # m → cm 변환
        elif conversion_type == 'g → kg':
            if 'g' in self.current_expression:
                value = float(self.current_expression.replace('g', ''))  # g 값을 추출하고 변환
                self.current_expression = str(value / 1000) + ' kg'  # g → kg 변환
        elif conversion_type == 'kg → g':
            if 'kg' in self.current_expression:
                value = float(self.current_expression.replace('kg', ''))  # kg 값을 추출하고 변환
                self.current_expression = str(value * 1000) + ' g'  # kg → g 변환
        elif conversion_type == 'mm → m':
            if 'mm' in self.current_expression:
                value = float(self.current_expression.replace('mm', ''))  # mm 값을 추출하고 변환
                self.current_expression = str(value / 1000) + ' m'  # mm → m 변환
        elif conversion_type == 'm → mm':
            if 'm' in self.current_expression:
                value = float(self.current_expression.replace('m', ''))  # m 값을 추출하고 변환
                self.current_expression = str(value * 1000) + ' mm'  # m → mm 변환
        elif conversion_type == 'nm → m':
            if 'nm' in self.current_expression:
                value = float(self.current_expression.replace('nm', ''))  # nm 값을 추출하고 변환
                self.current_expression = str(value / 1e9) + ' m'  # nm → m 변환
        elif conversion_type == 'm → nm':
            if 'm' in self.current_expression:
                value = float(self.current_expression.replace('m', ''))  # m 값을 추출하고 변환
                self.current_expression = str(value * 1e9) + ' nm'  # m → nm 변환
        elif conversion_type == 'µm → m':
            if 'µm' in self.current_expression:
                value = float(self.current_expression.replace('µm', ''))  # µm 값을 추출하고 변환
                self.current_expression = str(value / 1e6) + ' m'  # µm → m 변환
        elif conversion_type == 'm → µm':
            if 'm' in self.current_expression:
                value = float(self.current_expression.replace('m', ''))  # m 값을 추출하고 변환
                self.current_expression = str(value * 1e6) + ' µm'  # m → µm 변환

        self.update_label()  # 변환 후 레이블 업데이트

# 프로그램 실행
if __name__ == "__main__":
    calc = Calculator()  # 계산기 객체 생성
    calc.run()  # 계산기 실행
