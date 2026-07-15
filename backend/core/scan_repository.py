import json
from core.database import get_connection


def save_scan(result):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO scans(target, status, analysis, result_json)
        VALUES (?, ?, ?, ?)
        """,
        (
            result["target"],
            result["status"],
            result["analysis"],
            json.dumps(result)
        )
    )

    conn.commit()
    conn.close()


def get_all_scans():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT id,target,status,created_at
    FROM scans
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows



def get_scan_by_id(scan_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT result_json
        FROM scans
        WHERE id=?
    """, (scan_id,))

    row = cursor.fetchone()

    conn.close()

    # if not row:
    #     return None

    # return json.loads(row[0])
    if not row or row[0] is None:
     return None

    return json.loads(row[0])