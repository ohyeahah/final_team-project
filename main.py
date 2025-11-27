# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk
import os
import sys
import tkinter.ttk as ttk
import json
from datetime import datetime

# --- [핵심 수정 1] 동적 경로 설정 ---
# 현재 실행 중인 파이썬 파일의 위치를 찾습니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 이미지 폴더 경로를 현재 파일 위치 기준으로 설정합니다.
# (만약 이미지가 'img' 같은 하위 폴더에 있다면 os.path.join(BASE_DIR, "img")로 수정하세요)
IMAGE_PATH = BASE_DIR 

# --- [핵심 수정] UI/UX 개선을 위한 스타일 정의 ---
BG_COLOR = "#f7f8fa"
CARD_COLOR = "#ffffff"
POINT_COLOR = "#6c63ff"
HOVER_COLOR = "#5a55d6"
FONT_NAME = "Noto Sans KR"

# 영화 목록
MOVIES = [
    {
        "title": "신과 함께",
        "time": "10:00",
        "plot": "소방관 김자홍은 아이를 구하다 죽고, 저승차사 해원맥·덕춘·강림의 인도를 받아 7개의 지옥에서 재판을 받게 된다.\n차사들은 자홍이 의로운 귀인이라 믿고 환생을 돕지만, 재판이 진행되며 그의 숨겨진 과거가 드러난다.\n예상치 못한 진실과 시련 속에서 저승의 비밀과 새로운 세계의 문이 열린다.",
        "rating": 0,
        "reviews": []
    },
    {
        "title": "클래식",
        "time": "13:00",
        "plot": "현재의 지혜는 친구의 연애를 돕던 중, 오래된 편지와 테이프를 통해 어머니 주희의 첫사랑 이야기를 알게 된다.\n과거의 주희는 친구를 대신해 연서를 전하다 준하와 운명처럼 사랑에 빠지지만, 시대의 벽 앞에서 이뤄지지 못한다.\n세대를 넘어 이어지는 사랑의 기억은 결국 지혜의 현실 속에서 또 한 번의 인연으로 되살아난다.",
        "rating": 0,
        "reviews": []
    },
    {
        "title": "기생충",
        "time": "15:00",
        "plot": "가난한 김가족은 하나둘씩 부잣집 박가의 집에 위장 취업하며 기생하듯 스며든다.\n완벽했던 위장 생활은 지하실의 비밀이 드러나며 서서히 균열을 맞는다.\n두 가족의 욕망과 계급의 충돌은 결국 비극적인 결말로 치닫는다.",
        "rating": 0,
        "reviews": []
    },
    {
        "title": "감기",
        "time": "18:00",
        "plot": "치명적인 바이러스가 퍼지며 도시가 순식간에 폐쇄되고, 혼란과 공포가 극에 달한다.\n구급대원 지구는 감염된 연인을 구하기 위해 봉쇄된 지역으로 뛰어든다.\n생존을 위한 사투 속에서 인간의 이기심과 사랑이 극명하게 드러난다.",
        "rating": 0,
        "reviews": []
    },
    {
        "title": "국제시장",
        "time": "20:00",
        "plot": "어린 시절 한국전쟁 속에서 가족과 생이별한 덕수는 가족을 지키기 위해 평생을 희생하며 살아간다.\n독일 광부, 베트남 파병 등 시대의 고난 속에서도 그는 가장으로서의 책임을 묵묵히 감당한다.\n덕수의 인생은 곧 대한민국 근현대사의 축소판이자, 가족을 위한 한 세대의 헌신을 상징한다.",
        "rating": 0,
        "reviews": []
    },
    {
        "title": "범죄도시",
        "time": "22:00",
        "plot": "강력반 형사 마석도는 중국조폭들이 장악한 구로·가리봉 일대의 범죄 조직을 소탕한다.\n잔혹한 조직 보스 장첸이 등장하며 도시 전체가 피로 물들고, 긴장감이 폭발한다.\n마석도는 압도적인 힘과 직감으로 장첸을 끝내 제압하며 통쾌한 정의를 보여준다.",
        "rating": 0,
        "reviews": []
    },
]

# 티켓 가격
TICKET_PRICES = {
    "adult": 14000,
    "youth": 12000,
    "child": 8000,
}

# 버튼 호버 효과를 위한 함수
def on_enter(e):
    e.widget['background'] = HOVER_COLOR

def on_leave(e):
    e.widget['background'] = POINT_COLOR

# 인원 유형별 색상
PERSON_COLORS = {
    "성인": "#6495ED",  # 파랑 (Cornflower Blue)
    "청소년": "#90EE90", # 초록 (LightGreen)
    "어린이": "#FFD700"   # 노랑 (Gold)
}

class SeatSelectionWindow(tk.Toplevel):
    def __init__(self, parent, people_counts, booked_seats):
        super().__init__(parent)
        self.title("좌석 선택")
        self.geometry("550x400")
        self.resizable(False, False)
        self.transient(parent)
        self.config(bg=BG_COLOR)
        self.grab_set()
        
        self.parent = parent
        self.people_counts = people_counts
        self.selection_queue = ([ "성인" ] * people_counts.get("adult", 0) +
                                [ "청소년" ] * people_counts.get("youth", 0) +
                                [ "어린이" ] * people_counts.get("child", 0))
        self.total_seats_to_select = len(self.selection_queue)
        self.selected_seats = {} 
        self.booked_seats = booked_seats
        self.seat_buttons = {}
        self.result = None

        default_font = font.Font(family=FONT_NAME, size=10)
        
        screen_label = tk.Label(self, text="SCREEN", font=(FONT_NAME, 14, "bold"), bg="gray", fg="white")
        screen_label.pack(pady=20, fill="x", padx=20)

        seats_frame = tk.Frame(self, bg=BG_COLOR)
        seats_frame.pack(pady=10)

        for r in range(5):
            row_char = chr(ord('A') + r)
            for c in range(10):
                seat_name = f"{row_char}{c+1}"
                btn = tk.Button(seats_frame, text=seat_name, width=4, font=default_font, bg="lightgrey", relief="flat")
                btn.config(command=lambda b=btn, sn=seat_name: self.seat_click(b, sn))
                btn.grid(row=r, column=c, padx=2, pady=2)
                if seat_name in self.booked_seats:
                    btn.config(state="disabled", bg="red")
                self.seat_buttons[seat_name] = btn

        bottom_frame = tk.Frame(self, bg=BG_COLOR)
        bottom_frame.pack(pady=10)

        self.info_label = tk.Label(bottom_frame, text="", font=default_font, bg=BG_COLOR)
        self.info_label.pack(pady=(0, 10))

        confirm_btn = tk.Button(self, text="선택 완료", font=default_font, command=self.confirm_selection, bg=POINT_COLOR, fg="white", relief="flat", padx=10, pady=5)
        confirm_btn.pack(pady=5)
        confirm_btn.bind("<Enter>", on_enter)
        confirm_btn.bind("<Leave>", on_leave)

        self.update_info_label()

    def seat_click(self, seat_button, seat_name):
        if seat_name in self.selected_seats:
            person_type = self.selected_seats.pop(seat_name)
            self.selection_queue.insert(0, person_type)
            seat_button.config(bg="lightgrey", relief="flat")
        else:
            if self.selection_queue:
                person_type = self.selection_queue.pop(0)
                self.selected_seats[seat_name] = person_type
                color = PERSON_COLORS.get(person_type)
                seat_button.config(bg=color, relief="flat")
            else:
                messagebox.showwarning("선택 초과", f"최대 {self.total_seats_to_select}개의 좌석만 선택할 수 있습니다.", parent=self)
        
        self.update_info_label()

    def update_info_label(self):
        if self.selection_queue:
            next_person = self.selection_queue[0]
            color = PERSON_COLORS.get(next_person)
            self.info_label.config(text=f"'{next_person}' 좌석을 선택해주세요. ({len(self.selected_seats)}/{self.total_seats_to_select})", fg=color)
        else:
            self.info_label.config(text=f"모든 좌석을 선택했습니다. ({len(self.selected_seats)}/{self.total_seats_to_select})", fg="black")
    
    def confirm_selection(self):
        if self.selection_queue:
            messagebox.showwarning("좌석 부족", f"{self.total_seats_to_select}개의 좌석을 모두 선택해주세요.", parent=self)
            return
        
        self.result = sorted(self.selected_seats.keys())
        self.destroy()

class PaymentWindow(tk.Toplevel):
    def __init__(self, parent, total_price):
        super().__init__(parent)
        self.title("결제")
        self.geometry("300x200")
        self.resizable(False, False)
        self.transient(parent)
        self.config(bg=BG_COLOR)
        self.grab_set()

        self.total_price = total_price
        self.success = False

        default_font = font.Font(family=FONT_NAME, size=11) 
        tk.Label(self, text=f"총 결제 금액: {total_price:,}원", font=font.Font(family=FONT_NAME, size=13, weight="bold"), bg=BG_COLOR).pack(pady=15)
        
        input_frame = tk.Frame(self, bg=BG_COLOR)
        input_frame.pack(pady=5)
        tk.Label(input_frame, text="지불할 금액:", font=default_font, bg=BG_COLOR).pack(side="left", padx=5)
        self.amount_entry = tk.Entry(input_frame, font=default_font, width=12, justify="right")
        self.amount_entry.pack(side="left")

        pay_btn = tk.Button(self, text="결제하기", font=default_font, command=self.process_payment, bg=POINT_COLOR, fg="white", relief="flat", padx=10, pady=5)
        pay_btn.pack(pady=15)
        pay_btn.bind("<Enter>", on_enter)
        pay_btn.bind("<Leave>", on_leave)

    def process_payment(self):
        try:
            paid_amount = int(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("입력 오류", "숫자만 입력해주세요.", parent=self)
            return

        if paid_amount < self.total_price:
            messagebox.showwarning("금액 부족", "지불할 금액이 부족합니다.", parent=self)
        else:
            change = paid_amount - self.total_price
            messagebox.showinfo("결제 성공", f"결제가 완료되었습니다.\n거스름돈: {change:,}원", parent=self)
            self.success = True
            self.destroy()

class MovieTicketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("영화 티켓 예매 시스템")
        self.root.geometry("850x750")
        self.root.resizable(True, True)
        self.root.configure(bg=BG_COLOR)
        self.current_photo = None 
        self.current_rating = 0
        self.is_restarting = False

        self.default_font = font.Font(family=FONT_NAME, size=11)
        self.title_font = font.Font(family=FONT_NAME, size=14, weight="bold")

        self.booked_seats_data = {}
        self.load_data()

        self.create_widgets()
        self.show_plot(None)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_data(self):
        # 예매된 좌석 정보 로드
        try:
            seat_file_path = os.path.join(BASE_DIR, "booked_seats.json")
            if os.path.exists(seat_file_path):
                with open(seat_file_path, 'r', encoding='utf-8') as f:
                    self.booked_seats_data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"예매 좌석 파일 로드 오류: {e}")
            self.booked_seats_data = {}

        # 영화 후기 정보 로드
        try:
            review_file_path = os.path.join(BASE_DIR, "movie_reviews.json")
            if os.path.exists(review_file_path):
                with open(review_file_path, 'r', encoding='utf-8') as f:
                    loaded_reviews = json.load(f)
                    for movie, data in loaded_reviews.items():
                        for m in MOVIES:
                            if m['title'] == movie:
                                m['reviews'] = data.get('reviews', [])
                                break
        except (IOError, json.JSONDecodeError) as e:
            print(f"후기 파일 로드 오류: {e}")
            self.booked_seats_data = {}

        # 영화 후기 정보 로드
        try:
            review_file_path = os.path.join(BASE_DIR, "movie_reviews.json")
            if os.path.exists(review_file_path):
                with open(review_file_path, 'r', encoding='utf-8') as f:
                    loaded_reviews = json.load(f)
                    for movie, data in loaded_reviews.items():
                        for m in MOVIES:
                            if m['title'] == movie:
                                m['reviews'] = data.get('reviews', [])
                                break
        except (IOError, json.JSONDecodeError) as e:
            print(f"후기 파일 로드 오류: {e}")
            self.booked_seats_data = {}

    def save_data(self):
        # 예매된 좌석 정보 저장
        seat_file_path = os.path.join(BASE_DIR, "booked_seats.json")
        with open(seat_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.booked_seats_data, f, ensure_ascii=False, indent=4)

    def create_widgets(self):
        # --- 메뉴바 생성 ---
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # 파일 메뉴
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="파일", menu=file_menu)
        file_menu.add_command(label="재시작", command=self.restart_app)
        file_menu.add_separator()
        file_menu.add_command(label="종료", command=self.on_closing)

        # 옵션 메뉴
        options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="옵션", menu=options_menu)
        options_menu.add_command(label="모든 예매 좌석 초기화", command=self.reset_all_seats)

        # --- 영화 선택 섹션 ---
        movie_frame = tk.LabelFrame(self.root, text="영화 선택", font=self.default_font, padx=10, pady=10, bg=CARD_COLOR, bd=0)
        movie_frame.pack(padx=15, pady=10, fill="x")

        self.movie_listbox = tk.Listbox(movie_frame, font=self.default_font, height=len(MOVIES), exportselection=False, relief="flat", bg=BG_COLOR, selectbackground=POINT_COLOR)
        for movie_data in MOVIES:
            self.movie_listbox.insert(tk.END, f"{movie_data['title']} ({movie_data['time']})")
        self.movie_listbox.pack(fill="x")
        self.movie_listbox.select_set(0)
        self.movie_listbox.bind("<<ListboxSelect>>", self.show_plot)

        # --- 정보 및 후기 컨테이너 ---
        main_info_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_info_frame.pack(padx=15, pady=5, fill="both", expand=True)
        main_info_frame.columnconfigure(1, weight=1)

        # --- 영화 정보 섹션 (왼쪽) ---
        info_frame = tk.LabelFrame(main_info_frame, text="영화 정보", font=self.default_font, padx=15, pady=15, bg=CARD_COLOR, bd=0)
        info_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.poster_label = tk.Label(info_frame, bg=CARD_COLOR)
        self.poster_label.pack(pady=(0, 10))

        self.plot_label = tk.Label(info_frame, font=self.default_font, wraplength=230, justify="left", anchor="nw", bg=CARD_COLOR)
        self.plot_label.pack(fill="both", expand=True)

        # --- 영화 후기 섹션 (오른쪽) --- 
        review_frame = tk.LabelFrame(main_info_frame, text="영화 후기", font=self.default_font, padx=15, pady=15, bg=CARD_COLOR, bd=0)
        review_frame.grid(row=0, column=1, sticky="nsew")
        review_frame.rowconfigure(1, weight=1)
        review_frame.columnconfigure(0, weight=1)

        # 후기 목록 
        self.review_list_label = tk.Label(review_frame, text="후기 목록", font=(FONT_NAME, 11, "bold"), bg=CARD_COLOR, anchor="w")
        self.review_list_label.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        self.review_listbox = tk.Listbox(review_frame, height=8, font=(FONT_NAME, 10), relief="flat", bg=BG_COLOR, selectbackground=POINT_COLOR)
        self.review_listbox.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=5)

        # 후기 삭제 버튼
        delete_review_btn = tk.Button(review_frame, text="후기 삭제", font=(FONT_NAME, 10), command=self.delete_review, bg="#ff6b6b", fg="white", relief="flat", padx=10)
        delete_review_btn.grid(row=0, column=1, sticky="e", padx=(5,0))
        delete_review_btn.bind("<Enter>", lambda e: e.widget.config(bg="#e05252"))
        delete_review_btn.bind("<Leave>", lambda e: e.widget.config(bg="#ff6b6b"))


        # 후기 작성 
        add_review_frame = tk.Frame(review_frame, bg=CARD_COLOR)
        add_review_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        add_review_frame.columnconfigure(0, weight=1)

        tk.Label(add_review_frame, text="별점:", font=self.default_font, bg=CARD_COLOR).grid(row=0, column=0, sticky="w")
        self.star_rating_frame = tk.Frame(add_review_frame, bg=CARD_COLOR)
        self.star_rating_frame.grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.star_buttons = []
        for i in range(5):
            star_btn = tk.Button(self.star_rating_frame, text='☆', font=(FONT_NAME, 14), bd=0, bg=CARD_COLOR, activebackground=CARD_COLOR, fg='gold', activeforeground='gold', relief='flat', command=lambda r=i+1: self.rate_movie(r))
            star_btn.pack(side="left")
            self.star_buttons.append(star_btn)

        self.review_entry = tk.Entry(add_review_frame, font=self.default_font, relief="flat", bg=BG_COLOR)
        self.review_entry.grid(row=2, column=0, sticky="ew")

        review_submit_btn = tk.Button(add_review_frame, text="후기 등록", font=(FONT_NAME, 10), command=self.add_review, bg=POINT_COLOR, fg="white", relief="flat", padx=10)
        review_submit_btn.grid(row=2, column=1, sticky="e", padx=(5, 0))
        review_submit_btn.bind("<Enter>", on_enter)
        review_submit_btn.bind("<Leave>", on_leave)

        # --- 인원 수 선택 섹션 ---
        count_frame = tk.LabelFrame(self.root, text="인원 수 선택", font=self.default_font, padx=10, pady=10, bg=CARD_COLOR, bd=0)
        count_frame.pack(padx=15, pady=5, fill="x")

        self.spinboxes = {}
        person_types = {"성인": "adult", "청소년": "youth", "어린이": "child"}

        for i, (label_text, key) in enumerate(person_types.items()):
            tk.Label(count_frame, text=f"{label_text}:", font=self.default_font, bg=CARD_COLOR).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            spinbox = tk.Spinbox(count_frame, from_=0, to=10, width=5, font=self.default_font, justify="center", relief="flat")
            spinbox.grid(row=i, column=1, padx=5, pady=5)
            self.spinboxes[key] = spinbox
            price = TICKET_PRICES[key]
            tk.Label(count_frame, text=f"({price:,}원)", font=self.default_font, bg=CARD_COLOR).grid(row=i, column=2, padx=5, pady=5, sticky="w")

        # --- 버튼 섹션 ---
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=15)

        book_button = tk.Button(button_frame, text="예매하기", font=self.default_font, command=self.book_ticket, bg=POINT_COLOR, fg="white", relief="flat", padx=15, pady=5)
        book_button.pack(side="left", padx=10)
        book_button.bind("<Enter>", on_enter)
        book_button.bind("<Leave>", on_leave)

        reset_button = tk.Button(button_frame, text="초기화", font=self.default_font, command=self.reset_fields, bg="#D3D3D3", fg="black", relief="flat", padx=15, pady=5)
        reset_button.pack(side="left", padx=10)

    def show_plot(self, event):
        try:
            selected_indices = self.movie_listbox.curselection()
            if not selected_indices:
                selected_index = 0
            else:
                selected_index = selected_indices[0]
            
            movie_data = MOVIES[selected_index]
            
            plot_text = movie_data.get("plot", "선택된 영화의 줄거리 정보가 없습니다.")
            self.plot_label.config(text=plot_text, bg=CARD_COLOR)

            image_filename = f"{movie_data['title']}.png"
            # [수정] IMAGE_PATH 변수를 사용하여 경로 결합
            image_full_path = os.path.join(IMAGE_PATH, image_filename)

            if os.path.exists(image_full_path):
                img = Image.open(image_full_path)
                img.thumbnail((130, 200))
                self.current_photo = ImageTk.PhotoImage(img)
                self.poster_label.config(image=self.current_photo, bg=CARD_COLOR)
            else:
                self.poster_label.config(image='', bg=CARD_COLOR)
                # print(f"경고: 이미지 파일을 찾을 수 없습니다 - {image_full_path}") # 디버깅용
            
            self.update_review_display()
            self.rate_movie(0) # 별점 초기화

        except IndexError:
            pass

    def rate_movie(self, rating):
        self.current_rating = rating
        for i, btn in enumerate(self.star_buttons):
            if i < rating:
                btn.config(text='★')
            else:
                btn.config(text='☆')

    def add_review(self):
        try:
            selected_index = self.movie_listbox.curselection()[0]
        except IndexError:
            messagebox.showwarning("선택 오류", "후기를 추가할 영화를 선택해주세요.")
            return

        review_text = self.review_entry.get()
        if not self.current_rating and not review_text:
            messagebox.showwarning("입력 오류", "별점 또는 후기 내용을 입력해주세요.")
            return

        movie_data = MOVIES[selected_index]
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        # 별점과 후기 텍스트를 함께 저장
        full_review = f"({timestamp}) 별점: {'★'*self.current_rating}{'☆'*(5-self.current_rating)} - {review_text}"
        movie_data["reviews"].append(full_review)

        self.review_entry.delete(0, tk.END)
        self.rate_movie(0) # 별점 초기화
        self.update_review_display()

    def delete_review(self):
        try:
            selected_movie_index = self.movie_listbox.curselection()[0]
            selected_review_index = self.review_listbox.curselection()[0]
        except IndexError:
            messagebox.showwarning("선택 오류", "삭제할 후기를 목록에서 선택해주세요.")
            return

        if messagebox.askyesno("삭제 확인", "선택한 후기를 정말로 삭제하시겠습니까?"):
            movie_data = MOVIES[selected_movie_index]
            del movie_data["reviews"][selected_review_index]
            self.update_review_display()

    def update_review_display(self):
        selected_index = self.movie_listbox.curselection()[0] if self.movie_listbox.curselection() else 0
        movie_data = MOVIES[selected_index]
        self.review_listbox.delete(0, tk.END)
        if movie_data["reviews"]:
            for review in movie_data["reviews"]:
                self.review_listbox.insert(tk.END, review)
        else:
            self.review_listbox.insert(tk.END, "아직 등록된 후기가 없습니다.")

    def book_ticket(self):
        try:
            selected_index = self.movie_listbox.curselection()[0]
            selected_movie_data = MOVIES[selected_index]
            selected_movie_display = f"{selected_movie_data['title']} ({selected_movie_data['time']})"
        except IndexError:
            messagebox.showwarning("선택 오류", "영화를 선택해주세요.")
            return

        try:
            num_adults = int(self.spinboxes["adult"].get())
            num_youths = int(self.spinboxes["youth"].get())
            num_children = int(self.spinboxes["child"].get())
        except ValueError:
            messagebox.showerror("입력 오류", "인원 수는 숫자로 입력해야 합니다.")
            return

        people_counts = {
            "adult": num_adults,
            "youth": num_youths,
            "child": num_children
        }
        total_people = sum(people_counts.values())

        if total_people == 0:
            messagebox.showwarning("예매 오류", "예매 인원이 없습니다.\n인원 수를 선택해주세요.")
            return

        movie_title = selected_movie_data['title']
        current_booked_seats = self.booked_seats_data.get(movie_title, [])
        seat_window = SeatSelectionWindow(self.root, people_counts, current_booked_seats)
        self.root.wait_window(seat_window)

        selected_seats = seat_window.result
        if not selected_seats:
            return

        total_price = (num_adults * TICKET_PRICES["adult"]) + \
                      (num_youths * TICKET_PRICES["youth"]) + \
                      (num_children * TICKET_PRICES["child"])

        payment_window = PaymentWindow(self.root, total_price)
        self.root.wait_window(payment_window)

        if not payment_window.success:
            messagebox.showinfo("예매 취소", "결제가 취소되어 예매가 완료되지 않았습니다.")
            return

        # 예매 성공 시 좌석 정보 업데이트 및 저장
        if movie_title not in self.booked_seats_data:
            self.booked_seats_data[movie_title] = []
        self.booked_seats_data[movie_title].extend(selected_seats)
        self.save_data()

        receipt = (
            f"===== 예매 내역 =====\n\n"
            f"선택한 영화: {selected_movie_display}\n\n"
            f"성인: {num_adults}명\n"
            f"청소년: {num_youths}명\n"
            f"어린이: {num_children}명\n\n"
            f"선택 좌석: {', '.join(selected_seats)}\n\n"
            f"--------------------\n"
            f"총 결제 금액: {total_price:,}원"
        )

        # --- [핵심 수정 3] 파일 저장 위치 동적 설정 ---
        try:
            # BASE_DIR을 사용하여 항상 파이썬 파일과 같은 위치에 저장
            file_name = "예매표.txt"
            file_path = os.path.join(BASE_DIR, file_name)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(receipt)
            
            final_message = f"{receipt}\n\n--------------------\n위 내용이 아래 경로에 저장되었습니다:\n{file_path}"
            messagebox.showinfo("예매 완료", final_message)
        except Exception as e:
            messagebox.showerror("파일 저장 오류", f"예매 내역을 파일로 저장하는 중 오류가 발생했습니다.\n{e}")

    def reset_fields(self):
        self.movie_listbox.selection_clear(0, tk.END)
        self.movie_listbox.select_set(0)
        self.show_plot(None)
        self.review_entry.delete(0, tk.END)

        for spinbox in self.spinboxes.values():
            spinbox.delete(0, tk.END)
            spinbox.insert(0, "0")

    def on_closing(self, is_restarting=False):
        # 프로그램 종료 시 후기 데이터 저장
        reviews_to_save = {}
        for movie in MOVIES:
            if movie['reviews']:
                reviews_to_save[movie['title']] = {'reviews': movie['reviews']}
        
        review_file_path = os.path.join(BASE_DIR, "movie_reviews.json")
        with open(review_file_path, 'w', encoding='utf-8') as f:
            json.dump(reviews_to_save, f, ensure_ascii=False, indent=4)

        if not is_restarting:
            self.root.destroy()

    def restart_app(self):
        """프로그램을 재시작합니다."""
        self.on_closing(is_restarting=True)
        python = sys.executable
        os.execl(python, python, *sys.argv)
         
    def reset_all_seats(self):
        """모든 예매된 좌석 정보를 초기화합니다."""
        if messagebox.askyesno("초기화 확인", "정말로 모든 영화의 예매된 좌석 정보를 초기화하시겠습니까?\n이 작업은 되돌릴 수 없습니다.\n\n초기화 후 프로그램이 재시작됩니다."):
            seat_file_path = os.path.join(BASE_DIR, "booked_seats.json")
            if os.path.exists(seat_file_path):
                os.remove(seat_file_path)
            self.restart_app()