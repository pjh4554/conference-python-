import time
import calendar
from datetime import *
import pandas as pd
import datetime as dt
import csv
import os.path
from os import path
import datetime as dt
from pytimekr import pytimekr
import numpy as np

promt = """
=======================
    1. 예약 현황
    2. 예약 추가
    3. 예약 수정
    4. 예약 취소
    5. 나가기
=======================
"""
meeting_room = ["별", "달", "해"]
last_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def review_calendar():  # 예약현황을 보여주는 함수
    year = int(input("보고싶은 년도를 입력하세요:(ex)2023) "))
    month = int(input("보고싶은 월을 입력하세요:(ex)11) "))
    c = calendar.monthcalendar(year, month)
    make_calendar(year, month, c)
    print("")
    print("=" * 52)
    d = int(input("보고싶은 날짜를 입력하세요(ex) 15): "))
    if path.exists(f"{year}년{month}월{d}일.csv") == True:
        reserve_data = pd.read_csv(
            f"{year}년{month}월{d}일.csv",
            index_col=0,
            encoding="cp949",
        )
        print(reserve_data.fillna(" "))
    else:
        input("예약된 정보가 없습니다.엔터를 눌러주세요: ")
        pass
    input("엔터를 누르면 처음 화면으로 돌아갑니다.: ")


def want_calendar():  # int number 2을 누를때 필요한 함수
    year = int(input("예약하고 싶은 년도를 입력하세요:(ex)2023) "))
    month = int(input("예약하고 싶은 월을 입력하세요:(ex)11) "))
    c = calendar.monthcalendar(year, month)
    make_calendar(year, month, c)
    print("")
    print("=" * 52)
    possible_day(year, month)
    make_dataframe_csv(year, month, day)


def make_calendar(year, month, p):  # 달력을 만드는 함수
    print("=" * 52)
    print("월\t화\t수\t목\t금\t토\t일")
    print("=" * 52)
    re = last_day[month - 1]
    for op in range(1, re + 1):  # 공휴일 빨간색 만드는 함수
        k = dt.date(year, month, op)
        for qw in pytimekr.holidays(year):
            if k == qw:
                for i in range(len(p)):
                    for j in range(7):
                        if op == p[i][j]:
                            p[i][j] = "\033[31m" + str(p[i][j]) + "\033[0m"
    for u in range(1, 32):  # 예약이 있는 날짜에 숫자를 넣는 함수
        if path.exists(f"{year}년{month}월{u}일.csv") == True:
            qwe = pd.read_csv(f"{year}년{month}월{u}일.csv", index_col=0, encoding="cp949")
            for i in range(len(p)):
                for j in range(7):
                    if u == p[i][j]:
                        p[i][j] = f"{p[i][j]}({qwe.count().sum()})"
                        if qwe.count().sum() == 24:
                            p[i][j] = "\033[31m" + str(p[i][j]) + "\033[0m"
                    else:
                        pass
        else:
            pass
    for i in range(len(p)):  # 달력을 만드는 함수
        for j in range(7):
            if p[i][j] == 0:
                print(" \t", end="")
            elif j != 6:
                if j == 5:
                    p[i][5] = "\033[31m" + str(p[i][5]) + "\033[0m"
                    print(f"{p[i][5]}\t", end="")

                else:
                    print(f"{p[i][j]}\t", end="")
            elif j == 6:
                p[i][6] = "\033[31m" + str(p[i][6]) + "\033[0m"
                print(f"{p[i][j]}\t")


def possible_day(year, month):  # 원하는 달의 가능한 날짜를 보여줌
    global day
    k = calendar.monthcalendar(year, month)  # 달력을 이중 리스트로 나타냄
    df = pd.DataFrame(k)  # 데이터 프레임화
    df.columns = ["월", "화", "수", "목", "금", "토", "일"]  # 콜룸(첫번째 행)을 설정
    
    # 데이터 프레임에서 원하는 열을 뽑는방법
    a = df["월"].values.tolist()
    b = df["화"].values.tolist()
    c = df["수"].values.tolist()
    d = df["목"].values.tolist()
    e = df["금"].values.tolist()
    f = sorted(set(a + b + c + d + e))  # 중복을 없애고 정리
    re = last_day[month - 1]
    for op in range(1, re + 1):
        k = dt.date(year, month, op)
        for qw in pytimekr.holidays(year):
            if k == qw:
                lo = op
                rt = f.index(lo)
                del f[rt]
            else:
                pass
    for u in range(1, 32):
        if path.exists(f"{year}년{month}월{u}일.csv") == True:
            qwe = pd.read_csv(f"{year}년{month}월{u}일.csv", index_col=0, encoding="cp949")
            if qwe.count().sum() == 24:
                bg = f.index(u)
                del f[bg]
            else:
                pass
    while True:  # 예약 불가능한 날짜를 고를시 g로 돌아감
        print(*f[1:])  # 리스트 안의 내용을 괄호와 컴마 없이 뽑는 방법 *
        day = int(input("예약가능한 날짜입니다. 원하시는 날짜를 고르세요: "))
        if f.count(day) == 0:  # 리스트안에 없으면 예약을 못하게 하는 함수
            input("예약이 불가능한 날짜 입니다. 엔터를 눌러주세요: ")
        else:
            break


def make_dataframe_csv(year, month, day):  # 원하는 날짜에 예약함
    if path.exists(f"{year}년{month}월{day}일.csv") == True:
        reserve_data = pd.read_csv(
            f"{year}년{month}월{day}일.csv", index_col=0, encoding="cp949"
        )

        print(reserve_data.fillna(" "))
    else:
        reserve_data = pd.DataFrame(
            index=[
                "09:00",
                "10:00",
                "11:00",
                "12:00",
                "13:00",
                "14:00",
                "15:00",
                "16:00",
            ],
            columns=meeting_room,
        )

        reserve_data.to_csv(f"{year}년{month}월{day}일.csv", encoding="cp949")
        # data_frame_reserve_data = pd.read_csv(f"{year}년{month}월{day}일.csv")
        print(reserve_data.fillna(" "))
    name = input("이름을 입력해주세요: ")
    reserve_time = input("원하시는 시간을 선택해주세요ex) 09:00: ")
    reserve_room = input("원하시는 방을 선택해주세요.ex) 별: ")
    reserve_data.loc[reserve_time, reserve_room] = name  # loc와 iloc의 차이를 잘 알아두기
    print(reserve_data.fillna(" "))
    input("예약되었습니다.엔터를 눌러주세요: ")
    reserve_data.to_csv(f"{year}년{month}월{day}일.csv", encoding="cp949")


def organized(a, b):  # 중복이 많이 되서 정리한 함수
    reserve_data.loc[a, b] = " "
    print(reserve_data.fillna(" "))


print("현재 날짜:", datetime.now())
input("엔터를 눌러주세요: ")
while True:
    print(promt)
    number = int(input("원하시는 번호를 입력하세요.: "))
    if number == 1:
        review_calendar()
    elif number == 2:
        want_calendar()
    elif number == 3:
        modified_year, modified_month, modified_day = map(
            int, input("수정할 날짜를 입력하세요.ex)2023 11 2: ").split()
        )
        if path.exists(f"{modified_year}년{modified_month}월{modified_day}일.csv") == True:
            reserve_data = pd.read_csv(
                f"{modified_year}년{modified_month}월{modified_day}일.csv",
                index_col=0,
                encoding="cp949",
            )
            print(reserve_data.fillna(" "))
        else:
            input("예약된 정보가 없습니다.엔터를 누르면 처음 화면으로 돌아갑니다.: ")
            continue
        cancel_time, cancel_room = input("취소할 시간과 방을 적어주세요.ex)09:00 별: ").split()
        organized(cancel_time, cancel_room)
        reserve_data.to_csv(
            f"{modified_year}년{modified_month}월{modified_day}일.csv", encoding="cp949"
        )
        input("취소되었습니다.엔터를 눌러주세요: ")
        modified_time, modified_room, modified_name = input(
            "수정할 시간과 방과 이름을 적어주세요.ex)09:00 별 박종현: "
        ).split()
        reserve_data.loc[modified_time, modified_room] = modified_name
        print(reserve_data.fillna(" "))
        input("수정되었습니다.엔터를 눌러주세요: ")
        reserve_data.to_csv(
            f"{modified_year}년{modified_month}월{modified_day}일.csv", encoding="cp949"
        )
        continue
    elif number == 4:
        delete_year, delete_month, delete_day = map(
            int, input("삭제할 날짜를 입력하세요.(ex:2023 11 2): ").split()
        )
        if path.exists(f"{delete_year}년{delete_month}월{delete_day}일.csv") == True:
            reserve_data = pd.read_csv(
                f"{delete_year}년{delete_month}월{delete_day}일.csv",
                index_col=0,
                encoding="cp949",
            )
            print(reserve_data.fillna(" "))
        else:
            input("삭제할 정보가 없습니다.엔터를 누르면 처음 화면으로 돌아갑니다.: ")
        delete_time, delete_room = input("삭제할 시간과 방을 입력하세요.ex)09:00 별: ").split()
        organized(delete_time, delete_room)
        input("삭제되었습니다.엔터를 눌러주세요: ")
        reserve_data.to_csv(
            f"{delete_year}년{delete_month}월{delete_day}일.csv", encoding="cp949"
        )
    elif number == 5:
        break
    else:
        pass
