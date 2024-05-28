import os
import glob
import re


def sanitize_filename(filename):
    # 파일명에 사용할 수 없는 문자를 제거
    return re.sub(r'[\\/:*?"<>|]', "", filename)


def extract_info_and_rename(file_path):
    try:
        with open(file_path, "r", encoding="cp949") as file:
            lines = file.readlines()
            print(f"{file_path} 읽기 성공. 총 {len(lines)} 줄")

            if len(lines) >= 11:
                region = lines[10].split(":")[1].strip()
                period = lines[7].strip()
                year = period.split(":")[1].strip()[2:4]
                saletype = (
                    lines[8].split(":")[1].strip().replace("(", "_").replace(")", "")
                )
                print(
                    f"추출된 정보 - 지역: {region}, 연도: {year}, 매매타입: {saletype}"
                )
            else:
                print(f"{file_path}: 파일에 11번째 줄이 없습니다.")
                return
    except Exception as e:
        print(f"{file_path}을(를) 읽는 도중 오류가 발생했습니다: {e}")
        return

    region_sanitized = sanitize_filename(region)
    saletype_sanitized = sanitize_filename(saletype)
    # 요걸 빼먹으면 안 됨.
    directory = os.path.dirname(file_path)
    old_filename = os.path.basename(file_path)
    new_filename = f"y{year}_{region_sanitized}_{saletype_sanitized}.csv"
    new_file_path = os.path.join(directory, new_filename)

    try:
        os.rename(file_path, new_file_path)
        print(f"파일명이 {old_filename}에서 {new_filename}으로 변경되었습니다.")
    except Exception as e:
        print(f"{old_filename}을(를) 변경하는 도중 오류가 발생했습니다: {e}")


def main():
    directory = "C:\\Users\\EZEN\\Desktop\\OPEN CC\\house_flat_sale\\sale_data"

    # 디렉토리 존재 여부 확인
    if not os.path.exists(directory):
        print(f"디렉토리가 존재하지 않습니다: {directory}")
        return

    # 하위 디렉토리까지 포함하여 모든 CSV 파일을 찾습니다.
    csv_files = glob.glob(os.path.join(directory, "**", "*.csv"), recursive=True)
    # recursive 꼭 해야 내가 원하는 방식으로 csv 파일 찾을 수 있음.
    print(f"찾은 CSV 파일 목록: {csv_files}")

    for csv_file in csv_files:
        print(f"처리 중인 파일: {csv_file}")
        extract_info_and_rename(csv_file)


if __name__ == "__main__":
    main()
