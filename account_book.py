# account_book.py

# 가계부 내역을 저장할 리스트
transactions = []

# 프로그램을 시작하는 부분
def main():
    while True:
        print("\n--- 가계부 프로그램 ---")
        print("1. 수입/지출 기록")
        print("2. 전체 내역 보기")
        print("3. 잔액 조회")
        print("4. 종료")
        
        choice = input("원하는 메뉴를 선택하세요: ")

        if choice == '1':
            print("수입/지출 기록 기능을 실행합니다.")
        elif choice == '2':
            print("전체 내역 보기 기능을 실행합니다.")
        elif choice == '3':
            print("잔액 조회 기능을 실행합니다.")
        elif choice == '4':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")

# main 함수 실행
if __name__ == "__main__":
    main()