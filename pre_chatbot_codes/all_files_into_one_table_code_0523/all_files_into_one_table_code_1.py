import os
import pandas as pd
import pymysql
import time


class LOAD_CSV:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host="127.0.0.1",
                user="root",
                password="root1234",
                db="house_flat_sale",
                charset="utf8",
            )
            self.cur = self.conn.cursor()
            print("Database connection successful")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def process_files(self, directory):
        table_name = "국토교통부_단독다가구_매매"

        try:
            # 테이블 생성
            self.db_create(table_name)
            print(f"db_create {table_name} complete")
        except Exception as e:
            print(f"Error creating table: {e}")
            return

        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith(".csv"):
                    filepath = os.path.join(root, filename)
                    print(f"Reading file: {filepath}")

                    try:
                        # CSV 파일을 데이터프레임으로 읽기
                        df = pd.read_csv(filepath, encoding="cp949", skiprows=15)
                        print(f"File {filename} read into dataframe")

                        # NaN 값을 0으로 대체
                        df.fillna(0, inplace=True)
                        print("NaN values filled")

                        # '거래금액(만원)' 컬럼을 정수형으로 변환
                        df["거래금액(만원)"] = (
                            df["거래금액(만원)"].str.replace(",", "").astype(int)
                        )
                        print("'거래금액(만원)' column cleaned and converted to int")

                        # 데이터 삽입
                        self.db_insert(table_name, df)
                        print(f"Data from {filename} inserted into {table_name}")

                        # 변경사항 커밋
                        self.conn.commit()
                        print(f"Data from {filename} committed to the database")
                    except Exception as e:
                        print(f"Error processing file {filename}: {e}")
                        continue

        # 연결 종료
        self.conn.close()
        print("Database connection closed")

    def db_create(self, table):
        self.cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table} (
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
            );
        """
        )

    def db_insert(self, table, df):
        for index, row in df.iterrows():
            self.cur.execute(
                f"""
                INSERT INTO {table} (
                    시군구,
                    번지,
                    주택유형,
                    도로조건,
                    연면적,
                    대지면적,
                    계약년월,
                    계약일,
                    거래금액,
                    매수,
                    매도,
                    건축년도,
                    도로명,
                    해제사유발생일,
                    거래유형,
                    중개사소재지
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    row["시군구"],
                    row["번지"],
                    row["주택유형"],
                    row["도로조건"],
                    row["연면적(㎡)"],
                    row["대지면적(㎡)"],
                    row["계약년월"],
                    row["계약일"],
                    row["거래금액(만원)"],
                    row["매수"],
                    row["매도"],
                    row["건축년도"],
                    row["도로명"],
                    row["해제사유발생일"],
                    row["거래유형"],
                    row["중개사소재지"],
                ),
            )

    def db_insert_itertuples(self, table, df):
        for row in df.itertuples():
            self.cur.execute(
                f"""
                INSERT INTO {table} (
                    시군구,
                    번지,
                    주택유형,
                    도로조건,
                    연면적,
                    대지면적,
                    계약년월,
                    계약일,
                    거래금액,
                    매수,
                    매도,
                    건축년도,
                    도로명,
                    해제사유발생일,
                    거래유형,
                    중개사소재지
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    row["시군구"],
                    row["번지"],
                    row["주택유형"],
                    row["도로조건"],
                    row["연면적(㎡)"],
                    row["대지면적(㎡)"],
                    row["계약년월"],
                    row["계약일"],
                    row["거래금액(만원)"],
                    row["매수"],
                    row["매도"],
                    row["건축년도"],
                    row["도로명"],
                    row["해제사유발생일"],
                    row["거래유형"],
                    row["중개사소재지"],
                ),
            )


if __name__ == "__main__":
    start = time.time()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(
        BASE_DIR, "C:\\Users\\EZEN\\Desktop\\OPENCC\\house_flat_sale\\sale_data"
    )
    print(f"Processing directory: {directory}")

    LC = LOAD_CSV()
    LC.process_files(directory)

    end = time.time()
    print("end")
    total = end - start
    print(f"{int(total)//60:02}:{int(total)%60:02}{str(total-int(total))[1:]}")
