from core.database import get_connection


def save_scan(result):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO scans(target, status, analysis)
        VALUES (?, ?, ?)
        """,
        (
            result["target"],
            result["status"],
            result["analysis"]
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