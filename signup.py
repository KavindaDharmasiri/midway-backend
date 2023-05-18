from flask import Blueprint, request
import mysql.connector as connection
db = connection.connect(host='database-midway.cnjonpzevrxo.us-east-1.rds.amazonaws.com',user='admin', password='root1234', database= 'midway')

# Create a Blueprint instance for the routes
signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=['POST'])
def signup():
    mycursor = db.cursor()
    qury = 'create table if not exists login(name varchar(50),email varchar(50),password varchar(50))'
    mycursor.execute(qury)

    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    print("Username:", name)
    print("email:",email)
    print("Password:", password)



    qury = 'insert into login(name,email,password) value (%s,%s,%s)'
    value = (name,email,password)
    mycursor.execute(qury, value)

    db.commit()

    mycursor.close()
    db.close()

    return 'signup successful'