# import psycopg2
# from psycopg2.extras import RealDictCursor
# import json

# class Database:
#     def __init__(self,  para):
#         uri = f"postgresql://{para['user']}:{para['password']}@{para['host']}:{para['port']}/{para['database']}"
#         self.conn = psycopg2.connect(dsn=uri)
#         self.cur = self.conn.cursor()
#         if self.conn:
#             print("Connection is Successful")
#         else:
#             print("Connection Failed")

#     def execute_query(self, query):
#         cur = self.conn.cursor()
#         cur.execute(query)
#         rows = cur.fetchall()
#         columns = [desc[0] for desc in cur.description]
#         cur.close()
#         return rows, columns
    
#     def get_user_api_key(self,user_id):
#         try:
#             result =  self.cur.execute("SELECT api_key FROM users WHERE user_id = %s", (user_id,)).fetchone()
#             return result[0] if result else None
#         except Exception as e:
#             print(f"Error fetching API key: {e}")
#             return None

#     def create_user(self,user_id, api_key):
#         try:
#             with self.conn.cursor() as cur:
#                 cur.execute("INSERT INTO users (user_id, api_key) VALUES (%s, %s)", (user_id, api_key))
#                 self.conn.commit()
#                 return True
#         except Exception as e:
#             print(f"Error creating user: {e}")
#             return False

#     def update_user_tokens(self, user_id, access_token, request_token, public_token):
#         try:
#             with self.conn.cursor() as cur:
#                 cur.execute("""
#                     UPDATE users SET access_token = %s, request_token = %s, public_token = %s
#                     WHERE user_id = %s
#                 """, (access_token, request_token, public_token, user_id))
#                 self.conn.commit()
#                 return True
#         except Exception as e:
#             print(f"Error updating user tokens: {e}")
#             return False
        
#     def log_gtttransaction(self, user_id, trigger_type,
#                 tradingsymbol,
#                 exchange,
#                 trigger_values,
#                 last_price,
#                 orders,trigger_id):
#         try:
#             with self.conn.cursor() as cur:
#                 cur.execute("""
#                     INSERT INTO gttorders (user_id, trigger_type,
#                 tradingsymbol,
#                 exchange,
#                 trigger_values,
#                 last_price,
#                 orders,
#                 trigger_id)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#                 """, (user_id,  trigger_type,
#                         tradingsymbol,
#                         exchange,
#                         trigger_values,
#                         last_price,
#                         orders,
#                         trigger_id))
#                 self.conn.commit()
#         except Exception as e:
#             print(f"Error logging transaction: {e}")
#             return False
#         return True
        
#     def log_transaction(self, user_id, variety, exchange, tradingsymbol, transaction_type, quantity, product, order_type, price=None, validity=None, validity_ttl=None, disclosed_quantity=None, trigger_price=None, iceberg_legs=None, iceberg_quantity=None, auction_number=None, tag=None,order_id=None):
#         try:
#             with self.conn.cursor() as cur:
#                 cur.execute("""
#                     INSERT INTO transactions (user_id, variety, exchange, tradingsymbol, transaction_type, quantity, product, order_type, price, validity, validity_ttl, disclosed_quantity, trigger_price, iceberg_legs, iceberg_quantity, auction_number, tag, order_id)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 """, (user_id, variety, exchange, tradingsymbol, transaction_type, quantity, product, order_type, price, validity, validity_ttl, disclosed_quantity, trigger_price, iceberg_legs, iceberg_quantity, auction_number, tag, order_id))
#                 self.conn.commit()
#         except Exception as e:
#             print(f"Error logging transaction: {e}")
#             return False
#         return True
    
#     def update_transaction(self, order_id, **fields):
#         print(fields)
#         if not fields:
#             return False
#         try:
#             set_clause = ", ".join(f"{key} = %s" for key in fields)
#             values = list(fields.values()) + [order_id]
#             query = f"UPDATE transactions SET {set_clause} WHERE order_id = %s"
#             with self.conn.cursor() as cur:
#                 cur.execute(query, values)
#                 self.conn.commit()
#         except Exception as e:
#             print(f"Error updating transaction: {e}")
#             return False
#         return True
    
#     def update_gtttransaction(self, trigger_id, **fields):
#         # print("fgfdh",trigger_id,fields)
#         if not fields:
#             return False
#         try:
#             set_clause = ", ".join(f"{key} = %s" for key in fields)
#             values = list(fields.values()) + [trigger_id]
#             query = f"UPDATE gttorders SET {set_clause} WHERE trigger_id = %s"
#             with self.conn.cursor() as cur:
#                 cur.execute(query, values)
#                 self.conn.commit()
#         except Exception as e:
#             print(f"Error updating transaction: {e}")
#             return False
#         return True

        
#     def connection_termination(self):
#         self.conn.close()




# # # Helper function to get user details from the database
# # def get_user(user_id):
# #     conn = get_db_connection()
# #     cursor = conn.cursor(cursor_factory=RealDictCursor)
# #     cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
# #     user = cursor.fetchone()
# #     conn.close()
# #     return user

# # def api_token(user_id):
# #     conn = get_db_connection()
# #     cursor = conn.cursor(cursor_factory=RealDictCursor)
# #     cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
# #     user = cursor.fetchone()
# #     conn.close()
# #     return user

# # # Helper function to update user details in the database
# # def update_user(user_id, access_token=None, public_token=None, api_key=None):
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #     if access_token and public_token:
# #         cursor.execute("""
# #             UPDATE users
# #             SET access_token = %s, public_token = %s
# #             WHERE user_id = %s
# #         """, (access_token, public_token, user_id))
# #     elif api_key:
# #         cursor.execute("""
# #             INSERT INTO users (user_id, api_key)
# #             VALUES (%s, %s)
# #             ON CONFLICT (user_id) DO UPDATE SET api_key = EXCLUDED.api_key
# #         """, (user_id, api_key))
# #     conn.commit()
# #     conn.close()

# # # Helper function to log transactions
# # def log_transaction(user_id, transaction_type, details):
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #     cursor.execute("""
# #         INSERT INTO transactions (user_id, transaction_type, details)
# #         VALUES (%s, %s, %s)
# #     """, (user_id, transaction_type, details))
# #     conn.commit()
# #     conn.close()
    

import psycopg2
from psycopg2.extras import RealDictCursor
import json

class Database:
    def __init__(self, para):
        self.para = para
        self.create_database_if_not_exists()
        self.conn = self.connect_to_db()
        self.cur = self.conn.cursor()
        if self.conn:
            print("Connection is Successful")
            self.create_tables_if_not_exist()
        else:
            print("Connection Failed")

    def connect_to_db(self):
        uri = f"postgresql://{self.para['user']}:{self.para['password']}@{self.para['host']}:{self.para['port']}/{self.para['database']}"
        return psycopg2.connect(dsn=uri)

    def create_database_if_not_exists(self):
        try:
            # Connect to the default database
            uri = f"postgresql://{self.para['user']}:{self.para['password']}@{self.para['host']}:{self.para['port']}/{self.para['database']}"
            conn = psycopg2.connect(dsn=uri)
            conn.autocommit = True
            cur = conn.cursor()

            # Check if the database exists
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.para['database']}'")
            exists = cur.fetchone()
            if not exists:
                # Create the database
                cur.execute(f"CREATE DATABASE {self.para['database']}")
                print(f"Database {self.para['database']} created successfully.")
                cur.close()
                conn.close()
            else:
                print("Database alredy Exists")
                cur.close()
                conn.close()
            
        except Exception as e:
            print(f"Error creating database: {e}")

    def create_tables_if_not_exist(self):
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) UNIQUE NOT NULL,
            api_key CHAR(255) NOT NULL,
            access_token VARCHAR(255),
            request_token VARCHAR(255),
            public_token VARCHAR(255)
        );
        """

        create_transactions_table = """
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            variety VARCHAR(255) NOT NULL,
            exchange VARCHAR(255) NOT NULL,
            tradingsymbol VARCHAR(255) NOT NULL,
            transaction_type VARCHAR(255) NOT NULL,
            quantity VARCHAR(255) NOT NULL,
            product VARCHAR(255) NOT NULL,
            order_type VARCHAR(255) NOT NULL,
            price VARCHAR(255),
            validity VARCHAR(255),
            validity_ttl VARCHAR(255),
            disclosed_quantity VARCHAR(255),
            trigger_price VARCHAR(255),
            iceberg_legs VARCHAR(255),
            iceberg_quantity VARCHAR(255),
            auction_number VARCHAR(255),
            tag VARCHAR(255),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            order_id VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );
        """

        create_gttorders_table = """
        CREATE TABLE IF NOT EXISTS gttorders (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            trigger_type VARCHAR(255),
            tradingsymbol VARCHAR(255),
            exchange VARCHAR(255),
            trigger_values VARCHAR(255),
            last_price VARCHAR(255),
            orders VARCHAR(255),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            trigger_id VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );
        """

        try:
            with self.conn.cursor() as cur:
                cur.execute(create_users_table)
                cur.execute(create_transactions_table)
                cur.execute(create_gttorders_table)
                self.conn.commit()
                print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")

    # Other methods remain the same

    def execute_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        cur.close()
        return rows, columns

    def get_user_api_key(self, user_id):
        try:
            result = self.cur.execute("SELECT api_key FROM users WHERE user_id = %s", (user_id,)).fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error fetching API key: {e}")
            return None

    def create_user(self, user_id, api_key):
        try:
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO users (user_id, api_key) VALUES (%s, %s)", (user_id, api_key))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def update_user_tokens(self, user_id, access_token, request_token, public_token):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    UPDATE users SET access_token = %s, request_token = %s, public_token = %s
                    WHERE user_id = %s
                """, (access_token, request_token, public_token, user_id))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error updating user tokens: {e}")
            return False

    def log_gtttransaction(self, user_id, trigger_type, tradingsymbol, exchange, trigger_values, last_price, orders, trigger_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO gttorders (user_id, trigger_type, tradingsymbol, exchange, trigger_values, last_price, orders, trigger_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, trigger_type, tradingsymbol, exchange, trigger_values, last_price, str(orders), trigger_id))
                self.conn.commit()
        except Exception as e:
            print(f"Error logging transaction: {e}")
            return False
        return True

    def log_transaction(self, user_id, variety, exchange, tradingsymbol, transaction_type, quantity, product, order_type, price=None, validity=None, validity_ttl=None, disclosed_quantity=None, trigger_price=None, iceberg_legs=None, iceberg_quantity=None, auction_number=None, tag=None, order_id=None):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO transactions (user_id, variety, exchange, tradingsymbol, transaction_type, quantity, product, order_type, price, validity, validity_ttl, disclosed_quantity, trigger_price, iceberg_legs, iceberg_quantity, auction_number, tag, order_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, variety, exchange, tradingsymbol, transaction_type, quantity, product, order_type, price, validity, validity_ttl, disclosed_quantity, trigger_price, iceberg_legs, iceberg_quantity, auction_number, tag, order_id))
                self.conn.commit()
        except Exception as e:
            print(f"Error logging transaction: {e}")
            return False
        return True

    def update_transaction(self, order_id, **fields):
        if not fields:
            return False
        try:
            set_clause = ", ".join(f"{key} = %s" for key in fields)
            values = list(fields.values()) + [order_id]
            query = f"UPDATE transactions SET {set_clause} WHERE order_id = %s"
            with self.conn.cursor() as cur:
                cur.execute(query, values)
                self.conn.commit()
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False
        return True

    def update_gtttransaction(self, trigger_id, **fields):
        if not fields:
            return False
        try:
            set_clause = ", ".join(f"{key} = %s" for key in fields)
            values = list(fields.values()) + [trigger_id]
            query = f"UPDATE gttorders SET {set_clause} WHERE trigger_id = %s"
            with self.conn.cursor() as cur:
                cur.execute(query, values)
                self.conn.commit()
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False
        return True

    def connection_termination(self):
        self.conn.close()


