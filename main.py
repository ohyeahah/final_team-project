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