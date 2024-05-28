import pymysql
import pandas as pd
import os


def create_table_국토교통부_단독다가구_매매():

    conn, cur = None, None

    # 테이블 생성 sql
    sql1 = """create table if not exists 국토교통부_단독다가구_매매 (
        transaction_id INT AUTO_INCREMENT PRIMARY KEY,
        시군구 VARCHAR(255),
        번지 VARCHAR(255),
        주택유형 VARCHAR(255),
        도로조건 VARCHAR(255),
        연면적 FLOAT,
        대지면적 INT,
        계약년월 INT,
        계약일 INT,
        거래금액 INT,
        매수 VARCHAR(255),
        매도 VARCHAR(255),
        건축년도 INT,
        도로명 VARCHAR(255),
        해제사유발생일 VARCHAR(255),
        거래유형 VARCHAR(255),
        중개사소재지 VARCHAR(255)
    );"""

    try:

        conn = pymysql.connect(
            host="localhost",
            user="user",
            password="user1234",
            db="house_flat_sale",
            charset="utf8",
            port=3306,
        )
        cur = conn.cursor()

        # 각각 sql문마다 execute을 따로 실행해줘야 제대로 작동한다.
        # CREATE는 DDL 이라서 sql문 실행 후 auto commit으로 적용되므로 추가적인 commit() 실행이 필요 없다.
        cur.execute(sql1)

        print("테이블 생성 완료.")

    except Exception as e:
        print("테이블 생성 실패! \n Error:", e)

    finally:  # 관습적으로 finally문에 commit,close를 실행하는 코드를 작성해둠.
        conn.commit()
        cur.close()
        conn.close()


def get_dataframe_sale_data():
    # [21년도, 22년도, 23년도, 24년도] 폴더명
    dir_list = os.listdir()
    # 단독다가구매매 == ./ (현재폴더)
    origin_path = os.getcwd()

    # 폴더명, 파일명을 하드코딩해서 이용하는 것을 지양하는 방향으로 코드를 작성했습니다.
    # 폴더안에 필요한 폴더, 파일만 있어서 굳이 .endswith() 등 파일 분류하는 코드 작성은 하지 않았습니다.

    cnt = 0
    df1 = None

    for i in range(4):
        # ./21년도 폴더 안으로 이동
        os.chdir(os.getcwd() + "\\" + dir_list[i])
        # [y21_강원특별자치도_연립다세대_전월세.csv, ... , y21_충청북도_연립다세대_전월세.csv] 파일명
        csv_list = os.listdir()

        df2 = None

        for csv_file in csv_list:
            file_path = os.getcwd() + "\\" + csv_file
            # ./21년도/y21_강원특별자치도_연립다세대_전월세.csv
            print(file_path)

            df3 = pd.read_csv(
                file_path,
                skiprows=15,
                encoding="cp949",
                index_col=["NO"],
                low_memory=False,
            )
            print(df3)
            cnt += 1
            print(cnt)

            if df2 is None:
                df2 = df3.copy()
                continue
            # 21년도 안의 파일을 다 합침.
            df2 = pd.concat([df2, df3])
        # 연립다세대전월세 == ./ 이 폴더로 이동.
        os.chdir(origin_path)

        if df1 is None:
            df1 = df2.copy()
            continue
        # 연립다세대전월세 폴더 안에의 년도별로 모은 데이터 4년 분량을 다 합침.
        df1 = pd.concat([df1, df2])

    print(df1)

    return df1


if __name__ == "__main__":
    create_table_국토교통부_단독다가구_매매()
    # df = get_dataframe_국토교통부_단독다가구_매매()
    # insert_data_국토교통부_단독다가구_매매(df)
