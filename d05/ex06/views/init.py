from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.views import View
import psycopg2

TABLE_NAME = "ex06_movies"

def get_connection():
    return psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT'],
    )

class Init(View):
    def get(self, request: HttpRequest):
        conn = None
        try:
            conn = get_connection()
            DROP_TABLE = f"DROP TABLE IF EXISTS {TABLE_NAME};"
            CREATE_TABLE = f"""
                CREATE TABLE {TABLE_NAME} (
                    episode_nb INT PRIMARY KEY,
                    title VARCHAR(64) UNIQUE NOT NULL,
                    opening_crawl TEXT,
                    director VARCHAR(32) NOT NULL,
                    producer VARCHAR(128) NOT NULL,
                    release_date DATE NOT NULL,
                    created TIMESTAMPTZ DEFAULT now(),
                    updated TIMESTAMPTZ DEFAULT now()
                );
            """
            CREATE_FUNCTION = """
                CREATE OR REPLACE FUNCTION update_changetimestamp_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated = now();
                    NEW.created = OLD.created;
                    RETURN NEW;
                END;
                $$ LANGUAGE 'plpgsql';
            """
            CREATE_TRIGGER = f"""
                CREATE TRIGGER update_films_changetimestamp
                BEFORE UPDATE ON {TABLE_NAME}
                FOR EACH ROW EXECUTE PROCEDURE update_changetimestamp_column();
            """
            
            with conn.cursor() as curs:
                curs.execute(DROP_TABLE)
                curs.execute(CREATE_TABLE)
                curs.execute(CREATE_FUNCTION)
                curs.execute(CREATE_TRIGGER)
            conn.commit()
            return HttpResponse("OK like ex00 app specifications!")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()
