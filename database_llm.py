#!/usr/bin/env python3
"""
database_llm.py - Interactive natural language database query system
Runs locally, uses SSH tunnel to execute queries on ilab
Usage: python3 database_llm.py
"""

import sys
import getpass
import paramiko
from llama_cpp import Llama

# Configuration
ILAB_HOST = "ilab1.cs.rutgers.edu"
ILAB_SCRIPT_PATH = "~/database_llm_project/ilab_script.py"

def load_schema():
    """Load the database schema from file"""
    with open("schema.sql", "r") as f:
        return f.read()

def generate_sql(llm, schema, question):
    """Use LLM to generate SQL query from natural language question"""

    prompt = f"""You are a SQL expert. Given the following database schema, write a SQL SELECT query to answer the user's question.

Database Schema:
{schema}

IMPORTANT NOTES:
- The application table has numeric codes (e.g., owner_occupancy is a SMALLINT code)
- To get human-readable names, JOIN with the lookup tables (e.g., owner_occupancy table has owner_occupancy_name)
- Do NOT use placeholders like ? or parameters - write complete SQL queries with actual values
- loan_amount_000s and applicant_income_000s are already in thousands of dollars - do NOT multiply them
- For "owner occupied", join with owner_occupancy table and check owner_occupancy_name

Example for owner occupied query:
SELECT AVG(applicant_income_000s) FROM application a
JOIN owner_occupancy o ON a.owner_occupancy = o.owner_occupancy
WHERE o.owner_occupancy_name LIKE '%Owner-occupied%'

Example for loan vs income comparison:
SELECT COUNT(*) FROM application WHERE loan_amount_000s > applicant_income_000s

User Question: {question}

Write ONLY the SQL query, nothing else. Start with SELECT and do not end with semicolon.

SQL:"""

    print("  Generating SQL query...", flush=True)

    # Generate response
    output = llm(
        prompt,
        max_tokens=200,
        temperature=0.1,
        stop=[";", "\n\n"],
    )

    response_text = output['choices'][0]['text'].strip()

    # Extract SQL query (take first line that starts with SELECT)
    lines = response_text.split('\n')
    for line in lines:
        if line.strip().upper().startswith('SELECT'):
            return line.strip()

    # If no SELECT found, return the whole response
    return response_text.strip()

def execute_query_via_ssh(ssh_client, sql_query):
    """Execute SQL query on ilab via SSH"""
    try:
        # Escape single quotes in SQL query
        escaped_query = sql_query.replace("'", "'\\''")

        # Build command - DB_NAME is set so script queries aas517's database
        # User's GSSAPI credentials allow them to access it
        command = f"DB_NAME=aas517 python3 {ILAB_SCRIPT_PATH} '{escaped_query}'"

        print("  Executing query on ilab...", flush=True)

        # Execute command via SSH
        stdin, stdout, stderr = ssh_client.exec_command(command, timeout=30)

        # Get output
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if output:
            return output
        elif error:
            return f"Error:\n{error}"
        else:
            return "No output received"

    except Exception as e:
        return f"SSH Error: {e}"

def connect_ssh(username, password):
    """Connect to ilab via SSH"""
    try:
        print(f"Connecting to {ILAB_HOST}...", flush=True)

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_client.connect(
            ILAB_HOST,
            username=username,
            password=password,
            timeout=10
        )

        print("Connected successfully!\n")
        return ssh_client

    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
        return None
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def main():
    """Main interactive loop"""

    print("=" * 70)
    print("Natural Language Database Query System")
    print("=" * 70)
    print()

    # Get SSH credentials
    print("Enter your ilab credentials:")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    print()

    # Connect to ilab
    ssh_client = connect_ssh(username, password)
    if not ssh_client:
        sys.exit(1)

    # Load LLM
    print("Loading LLM model (this may take 30-60 seconds)...")
    try:
        llm = Llama(
            model_path="./models/phi-3-mini.gguf",
            n_ctx=2048,
            n_threads=4,
            verbose=False
        )
        print("Model loaded successfully!\n")
    except Exception as e:
        print(f"Error loading model: {e}")
        ssh_client.close()
        sys.exit(1)

    # Load schema
    schema = load_schema()

    print("=" * 70)
    print("Ask questions about the mortgage database in plain English.")
    print("Type 'exit' to quit.")
    print("=" * 70)
    print()

    # Interactive loop
    try:
        while True:
            # Get user question
            question = input("Your question: ").strip()

            # Check for exit
            if question.lower() == "exit":
                print("\nGoodbye!")
                break

            if not question:
                continue

            print()

            # Generate SQL
            sql_query = generate_sql(llm, schema, question)
            print(f"  Generated SQL: {sql_query}")
            print()

            # Execute query
            result = execute_query_via_ssh(ssh_client, sql_query)
            print(result)
            print()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")

    finally:
        ssh_client.close()
        print("Connection closed. Goodbye!")

if __name__ == "__main__":
    main()
