import os, sys, pyodbc, platform, glob, re, logging

class EBSDBAuth:
    def __init__(self, server='', database='', db_uid=None, db_pwd=None, driver=None, queries_location='queries'):  
        self.logger =   logging.getLogger('Database')
        self.driver = driver or self._get_driver()
        self.get_environ_method = self._determine_environment()
        self.sql_path = queries_location
        self.all_queries = self._load_sql_queries()
        self._load_credentials(server, database, db_uid, db_pwd)

    def _determine_environment(self):
        containerised = os.environ.get('RUNNING_IN_DOCKER', False)

        if containerised:
            return os.environ.get

        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv

    def _load_credentials(self, server, database, db_uid, db_pwd):
        # Always prefer supplied credentials, otherwise try .env
        self.db_uid = db_uid or self.get_environ_method("DB_UID") 
        self.db_pwd = db_pwd or self.get_environ_method("DB_PWD")
        self.database = database or self.get_environ_method("DB_DATABASE")
        self.server = server or self.get_environ_method("DB_SERVER")

        if not self.db_uid:
            self.logger.error("DB_UID not supplied or found in environment variables (db_uid='NAME' or in .env 'DB_UID=NAME')")
            sys.exit(1)
        elif not self.db_pwd:
            self.logger.error("DB_PWD not supplied or found in environment variables (db_pwd='password' or in .env 'DB_PWD=password')")
            sys.exit(1)
        elif not self.database:
            self.logger.error("Database name not supplied or found in environment variables (database='NAME' or in .env 'DB_DATABASE=NAME')")
            sys.exit(1)
        elif not self.server:
            self.logger.error("Server not supplied or found in environment variables (server='NAME' or in .env 'DB_SERVER=NAME')")
            sys.exit(1)

    def _get_driver(self):
        # Bit more dynamic way to get Linux drivers, should be more resistant to any version changes or environment changes than hardcoding it.
        if platform.system() == 'Linux':
            possible_paths = [
                "/opt/microsoft/msodbcsql*/lib64/libmsodbcsql-*.so.*",
                "/usr/lib64/libmsodbcsql-*.so.*",
                "/usr/local/lib64/libmsodbcsql-*.so.*"
            ]
            
            for path in possible_paths:
                matches = glob.glob(path)
                if matches:
                    return sorted(matches)[-1]
                
            raise FileNotFoundError("No suitable ODBC driver for SQL Server found. Please install the Microsoft ODBC driver for SQL Server.")
        
        elif platform.system() == 'Windows':
            # 'SQL Server' driver is very old and can have issue with things like parameters.  Try and find a better driver first, SQL management comes with one.
            drivers = pyodbc.drivers()
            sql_server_drivers = [driver for driver in drivers if 'sql server' in driver.lower()]

            version_drivers = [driver for driver in sql_server_drivers if self._get_driver_version(driver) > 0]
            
            if version_drivers:
                return max(version_drivers, key=self._get_driver_version)
            elif sql_server_drivers:
                return 'SQL Server'
            else:
                raise ValueError("No SQL Server drivers found")
            
    def _get_driver_version(self, driver):
        match = re.search(r'(\d+)(?=\s+for)', driver)
        return int(match.group(1)) if match else 0
        
    def authenticate(self):
        connection_string = f'Driver={self.driver};Server={self.server};Encrypt=no;Database={self.database};UID={self.db_uid};PWD={self.db_pwd}'
        try:
            cnxn = pyodbc.connect(connection_string)
            self.logger.info("Database authenticated successfully")
            return cnxn
        except pyodbc.Error as e:
            self.logger.error(f"Database connection failed: {e}")
            return None
        
    def execute_query(self, query_name, raw_sql=None, params=None):
        sql = ''
        try:
            if query_name is not None:
                sql = self.get_query(query_name)
            elif raw_sql is not None:
                sql = raw_sql
            else:
                raise Exception
            if sql == None:
                raise ValueError 
        except Exception as e:
            self.logger.exception(f"query_name and raw_sql parameters appear to be empty - execute_query has no sql to execute - {e}")
            return {}  
        except ValueError as e:
            self.logger.exception(f"SQL query passed to execute_query is None - Was the query name supplied correct? - {e}")
            return {}  

        cnxn = self.authenticate()
        try:
            with cnxn.cursor() as cursor:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.exception(f"Exception in query execution: {e}")
            return {}
        finally:
            cnxn.close()        

    def _load_sql_queries(self):
        queries = {}
        for filename in os.listdir(self.sql_path):
            if filename.endswith('.sql'):
                file_path = os.path.join(self.sql_path, filename)
                query_name = os.path.splitext(filename)[0]
                with open(file_path, 'r') as file:
                    queries[query_name] = file.read()
        self.logger.info(f"Loaded queries - {queries.keys()}")
        return queries

    def get_query(self, query_name):
        return self.all_queries.get(query_name)