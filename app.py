from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import pymysql

app = Flask(__name__)

db_config = {
    'host': '106.0.63.154',
    'user': 'pdc1647_Test1101',
    'password': 'jmpTest1101',
    'database': 'pdc1647_Test1101'
}

# establish connection to mysql server
# connection = pymysql.connect(**db_config)

@app.route('/dataQuery', methods=['POST'])
def post_data_query():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    elapsed_time = request.args.get("elapsed_time")
    elapsed_time_int = int(elapsed_time)

    end_time_calc = datetime.now()
    start_time_calc = end_time_calc - timedelta(milliseconds=elapsed_time_int)

    end_time_calc = end_time_calc.strftime("%H:%M:%S")
    start_time_calc = start_time_calc.strftime("%H:%M:%S")

    reporting_node = request.args.get('reporting_node')
    department = request.args.get('department')
    work_center = request.args.get('work_center')
    employee_id = request.args.get('employee_id')
    part_number = request.args.get('part_number')
    quantity = request.args.get('quantity')
    work_order = request.args.get('work_order')
    start_time = start_time_calc
    end_time = end_time_calc
    sequence_num = request.args.get('sequence_num')
    progress = request.args.get('progress')
    setup_time = request.args.get('setup_time')
    die_set = request.args.get('die_set')
    material_lot = request.args.get('material_lot')
    status_code = request.args.get('status_code')
    comments = request.args.get('comments')

    sql = "INSERT into record (reporting_node, department, work_center, employee_id, part_number, quantity, work_order, start_time, end_time, sequence_num, progress, setup_time, die_set, material_lot, status_code, comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    cursor.execute(sql, (reporting_node, department, work_center, employee_id, part_number, quantity, work_order, start_time, end_time, sequence_num, progress, setup_time, die_set, material_lot, status_code, comments))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Data inserted successfully"}), 201


@app.route('/values', methods=['GET'])
def get_data():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    sql = "SELECT * FROM record LIMIT 10"
    cursor.execute(sql)

    results = cursor.fetchall()

    for result in results:
        print(result)
    
    cursor.close()
    connection.close()

    if results:
        return 'Success'
    else:
        return 'Failed'
    
if __name__ == "__main__":
    app.run(debug=True)
