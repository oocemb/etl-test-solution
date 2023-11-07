from contextlib import contextmanager
from typing import Any

import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection

from settings import logger, PG_DSL


@contextmanager
def open_postgres(dsl: dict[str:Any] = PG_DSL) -> _connection:
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try:
        logger.info("Creating connection to Postgres")
        yield conn
    finally:
        logger.info("Closing connection to Postgres")
        conn.commit()
        conn.close()


def get_report_data() -> list[list]:
    with open_postgres() as pg_conn:
        pg_curs = pg_conn.cursor()
        pg_curs.execute("""select subject, sum(count_doses_sum), round(avg(overdue_day))
                        from overdue
                        group by subject
                        order by subject;""")
        return pg_curs.fetchall()
