from flask import Flask, request, render_template, jsonify
import pymysql
import re

app = Flask(__name__)


# 데이터베이스 연결
def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="root1234",
        db="house_flat_sale",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


# 사용자 입력에서 필요한 정보 추출하는 함수
def extract_info(user_input):
    # 사용자 입력에서 지역과 년도 정보 추출하기
    location_pattern = r"(\d{2,4})년\s*([가-힣\s]+)"
    match = re.search(location_pattern, user_input)
    if match:
        year = match.group(1)  # 년도 정보
        location = match.group(2).strip()  # 지역 정보
        return location, year
    else:
        return None, None


# 사용자 입력에 따른 응답 가져오기
def get_transaction_data(location, year):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # SQL 문 생성
            sql = f"""
            SELECT 거래금액 
            FROM 국토교통부_단독다가구_매매 
            WHERE 시군구 LIKE "%{location}%" 
            AND 계약년월 LIKE "20{year}%"
            ORDER BY 계약년월 DESC
            """
            # SQL 문 실행
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["user_message"]
    location, year = extract_info(user_message)
    if location and year:
        transaction_data = get_transaction_data(location, year)
        return jsonify(transaction_data)
    else:
        return jsonify([])


if __name__ == "__main__":
    app.run(debug=True)
