import os
import time
import pandas as pd
import pymysql

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class LOAD_CSV():
    def __init__(self):

        self.main()

    def main(self):
        start = time.time()
        print('start')

        # CSV 파일이 들어있는 디렉토리 경로
        directory = BASE_DIR + '/data/국토교통부_전국아파트매매'

        # pymysql을 사용하여 MariaDB에 연결
        self.conn = pymysql.connect(host='127.0.0.1', user='user', password='user1234', db='opencc_1', charset='utf8')
        # 커서 생성
        self.cur = self.conn.cursor()
        print('conn, cursor complete')

        # 디렉토리 내 모든 CSV 파일 가져오기
        for foldername in os.listdir(directory):
            print(foldername)
            folder_path = os.path.join(directory, foldername)
            if os.path.isdir(folder_path):
                for filename in os.listdir(folder_path):
                    print(foldername, filename)
                    if filename.endswith(".csv"):
                        r_filename = os.path.splitext(filename)[0]
                        filepath = os.path.join(folder_path, filename)
                        print(f"Reading file: {filename}")
                        
                        # CSV 파일을 데이터프레임으로 읽기
                        df = pd.read_csv(filepath, encoding='cp949', skiprows=15)

                        df['거래금액(만원)'] = df['거래금액(만원)'].str.replace(',','').apply(int)
                        print(f'df read int {filename} complete')
                        
                        self.db_create(r_filename)
                        print(f'db_create {r_filename} complete')

                        self.db_insert(r_filename, df)
                        print(f'db_insert {r_filename} complete')

        # 변경사항 커밋
        self.conn.commit()

        # 연결 종료
        self.conn.close()

        end = time.time()
        print('end')
        total = end - start
        print(f'{int(total)//60:02}:{int(total)%6:02}{str(total-int(total))[1:]}')

    def db_create(self, table):
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                시군구 VARCHAR(255),
                번지 VARCHAR(255),
                본번 INT,
                부번 INT,
                단지명 VARCHAR(255),
                전용면적 FLOAT,
                계약년월 INT,
                계약일 INT,
                거래금액 INT,
                동 VARCHAR(255),
                층 INT,
                매수자 VARCHAR(255),
                매도자 VARCHAR(255),
                건축년도 INT,
                도로명 VARCHAR(255),
                해제사유발생일 VARCHAR(255),
                거래유형 VARCHAR(255),
                중개사소재지 VARCHAR(255),
                등기일자 VARCHAR(255)
            );
            """)

    def db_insert(self, table, df):

        for index, row in df.iterrows():
            self.cur.execute(f"""
                INSERT INTO {table} (""" + """
                    시군구,
                    번지,
                    본번,
                    부번,
                    단지명,
                    전용면적,
                    계약년월,
                    계약일,
                    거래금액,
                    동,
                    층,
                    매수자,
                    매도자,
                    건축년도,
                    도로명,
                    해제사유발생일,
                    거래유형,
                    중개사소재지,
                    등기일자
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['시군구'],
                row['번지'],
                row['본번'],
                row['부번'],
                row['단지명'],
                row['전용면적(㎡)'],
                row['계약년월'],
                row['계약일'],
                row['거래금액(만원)'],
                row['동'],
                row['층'],
                row['매수자'],
                row['매도자'],
                row['건축년도'],
                row['도로명'],
                row['해제사유발생일'],
                row['거래유형'],
                row['중개사소재지'],
                row['등기일자']
            ))



if __name__ == '__main__':
    LC = LOAD_CSV()
