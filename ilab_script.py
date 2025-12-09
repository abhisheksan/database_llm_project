#!/usr/bin/env python3
"""
ilab_script.py - Executes SQL SELECT queries on the mortgage database
Usage: python3 ilab_script.py 'SELECT query here'
"""

import sys
import psycopg2
from psycopg2 import sql

def execute_query(query):
    """Execute SQL query and return results as formatted table"""

    # Database connection parameters
    import os
    import getpass

    DB_HOST = "postgres.cs.rutgers.edu"
    DB_NAME = os.environ.get('DB_NAME', 'aas517')
    # Use current system user if not specified
    DB_USER = os.environ.get('DB_USER', getpass.getuser())
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')

    try:
        # Connect to database
        print(f"Connecting to database {DB_NAME} as {DB_USER}...", file=sys.stderr)

        # Try GSSAPI first (passwordless), then fall back to password if provided
        if DB_PASSWORD:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
        else:
            # GSSAPI authentication (no password needed on ilab)
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER
            )

        # Create cursor
        cur = conn.cursor()

        # Set search path to include your schema
        cur.execute("SET search_path TO aas517, public;")

        # Execute query
        print(f"Executing query...", file=sys.stderr)
        cur.execute(query)

        # Fetch results
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        # Print table header
        header = " | ".join(colnames)
        separator = "-" * len(header)
        print(separator)
        print(header)
        print(separator)

        # Print rows
        if rows:
            for row in rows:
                print(" | ".join(str(val) if val is not None else "NULL" for val in row))
        else:
            print("(No rows returned)")

        print(separator)
        print(f"\nTotal rows: {len(rows)}", file=sys.stderr)

        # Close connection
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Database error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error executing query: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ilab_script.py 'SELECT query'", file=sys.stderr)
        print("Example: python3 ilab_script.py 'SELECT COUNT(*) FROM application'", file=sys.stderr)
        sys.exit(1)

    query = sys.argv[1]

    # Basic validation - only allow SELECT queries
    if not query.strip().upper().startswith('SELECT'):
        print("Error: Only SELECT queries are allowed", file=sys.stderr)
        sys.exit(1)

    execute_query(query)
