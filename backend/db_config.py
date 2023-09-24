DB_CONFIG = {
    'host': 'localhost',
    'port': '3306',
    'database': 'student',
    'user': 'root',
    'password': ''
}

DB_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"