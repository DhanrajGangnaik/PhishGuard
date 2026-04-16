import json
import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'scans.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_type TEXT NOT NULL,
            content TEXT NOT NULL,
            label TEXT NOT NULL,
            score INTEGER NOT NULL,
            reasons TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        '''
    )
    conn.commit()
    conn.close()


def insert_scan(input_type: str, content: str, label: str, score: int, reasons: list):
    conn = get_connection()
    conn.execute(
        'INSERT INTO scans (input_type, content, label, score, reasons, created_at) VALUES (?, ?, ?, ?, ?, ?)',
        (input_type, content, label, score, json.dumps(reasons), datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    )
    conn.commit()
    conn.close()


def get_counts():
    conn = get_connection()
    rows = conn.execute('SELECT label, COUNT(*) AS count FROM scans GROUP BY label').fetchall()
    total = conn.execute('SELECT COUNT(*) AS total FROM scans').fetchone()['total']
    conn.close()

    counts = {'Safe': 0, 'Suspicious': 0, 'Phishing': 0, 'Total': total}
    for row in rows:
        counts[row['label']] = row['count']
    return counts


def get_recent_scans(limit: int = 10):
    conn = get_connection()
    rows = conn.execute(
        'SELECT id, input_type, content, label, score, reasons, created_at FROM scans ORDER BY id DESC LIMIT ?',
        (limit,),
    ).fetchall()
    conn.close()

    results = []
    for row in rows:
        item = dict(row)
        item['reasons'] = json.loads(item['reasons'])
        results.append(item)
    return results


def get_chart_data():
    counts = get_counts()
    return {
        'labels': ['Safe', 'Suspicious', 'Phishing'],
        'values': [counts['Safe'], counts['Suspicious'], counts['Phishing']],
    }
