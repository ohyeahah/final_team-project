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
