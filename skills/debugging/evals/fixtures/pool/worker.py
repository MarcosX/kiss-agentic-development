from db import ConnectionPool

pool = ConnectionPool(max_conns=3)


def process_job(job_id):
    conn = pool.acquire()
    return conn
