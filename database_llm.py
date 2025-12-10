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

    # Extract minimal schema info from the actual schema file
    tables_info = []
    current_table = None

    for line in schema.split('\n'):
        if 'CREATE TABLE' in line:
            table_name = line.split('CREATE TABLE')[1].split('(')[0].strip()
            current_table = table_name
            tables_info.append(f"{table_name}:")
        elif current_table and any(dtype in line for dtype in ['INTEGER', 'TEXT', 'SMALLINT', 'DECIMAL']):
            col = line.strip().split()[0].strip().strip(',')
            if col and not col.startswith('--') and col.lower() not in ['primary', 'foreign', 'references', 'not', 'unique']:
                tables_info.append(f"  {col}")
        elif ');' in line:
            current_table = None

    # Take only first 80 lines to keep it small
    schema_summary = '\n'.join(tables_info[:80])

    # Use Phi-3 instruct format with example
    prompt = f"""<|system|>
You are a SQL expert. Convert questions to PostgreSQL SELECT queries.

Schema:
{schema_summary}

Key relationships:
- application.loan_type joins to loan_type.loan_type (both SMALLINT)
- application.property_type joins to property_type.property_type (both SMALLINT)
- application.owner_occupancy joins to owner_occupancy.owner_occupancy (both SMALLINT)
- application.denial_reason_1 joins to denial_reason.denial_reason_code (both SMALLINT)
- application.agency_code joins to agency.agency_code (both SMALLINT)
- application.action_taken joins to action_taken.action_taken (both SMALLINT)
- application.state_code joins to state.state_code (both SMALLINT)
- application.county_code joins to county.county_code (both INTEGER)

Important rules:
- loan_amount_000s and applicant_income_000s are in thousands (e.g., 200 = $200,000)
- Lookup tables: code columns are SMALLINT/INTEGER, _name columns are TEXT
- NEVER use subqueries
- To compare columns in same table: use simple WHERE, no JOIN
- To filter by _name: JOIN lookup table on code, then WHERE on _name

Examples:
Q: loan greater than income count
A: SELECT COUNT(*) FROM application WHERE loan_amount_000s>applicant_income_000s

Q: average income owner occupied
A: SELECT AVG(a.applicant_income_000s) FROM application a JOIN owner_occupancy o ON a.owner_occupancy=o.owner_occupancy WHERE o.owner_occupancy_name LIKE '%Owner%'

Q: most common denial reason
A: SELECT d.denial_reason_name,COUNT(*) FROM application a JOIN denial_reason d ON a.denial_reason_1=d.denial_reason_code GROUP BY d.denial_reason_name ORDER BY COUNT(*) DESC LIMIT 1<|end|>
<|user|>
{question}<|end|>
<|assistant|>
SELECT"""

    print("  Generating SQL query...", flush=True)
    print(f"  [DEBUG] Prompt length: {len(prompt)} chars", flush=True)

    # Generate response
    output = llm(
        prompt,
        max_tokens=200,
        temperature=0.2,
        stop=["<|end|>", ";", "===", "reply:", "To find", "This query", "The above"],
    )

    response_text = output['choices'][0]['text'].strip()

    # Debug output
    print(f"  [DEBUG] Raw: '{response_text}'", flush=True)

    if not response_text:
        print("  [WARNING] Empty response", flush=True)
        return "SELECT COUNT(*) FROM application"

    # Clean up response - remove any trailing explanations
    # Split on common separators
    for separator in ['\n\n', '===', 'reply:', 'To find', 'This query', 'The above', 'Note:']:
        if separator in response_text:
            response_text = response_text.split(separator)[0].strip()

    # Clean up response
    if not response_text.upper().startswith('SELECT'):
        response_text = 'SELECT ' + response_text

    # Add semicolon back if needed for execution
    if not response_text.endswith(';'):
        response_text = response_text + ';'

    # Join multi-line to single line
    response_text = ' '.join(response_text.split())

    # Remove the semicolon we just added (SSH script doesn't need it)
    if response_text.endswith(';'):
        response_text = response_text[:-1].strip()

    return response_text if response_text else "SELECT COUNT(*) FROM application"

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

            # Check for exit - must be exact string "exit"
            if question == "exit":
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
