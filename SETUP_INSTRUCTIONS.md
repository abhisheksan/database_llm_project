# Setup Instructions

## For Person 1 (aas517) - Already Done ✓
- ilab_script.py on ilab
- Database with mortgage data
- Granted access to mjm857

## For Person 2 (mjm857) - Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/database_llm_project.git
cd database_llm_project
```

### 2. Install Python packages
```bash
pip3 install llama-cpp-python paramiko psycopg2-binary
```

### 3. Download LLM model
```bash
mkdir -p models
cd models
curl -L -o phi-3-mini.gguf "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
cd ..
```

### 4. Run the program
```bash
python3 database_llm.py
```

When prompted:
- **Username**: Your ilab username (e.g., mjm857)
- **Password**: Your ilab password

The program will:
1. Connect to ilab via SSH
2. Load the LLM model locally
3. Let you ask questions in plain English
4. Generate SQL queries using the LLM
5. Execute queries on ilab and display results

### 5. Test queries
Try these:
- "How many applications are in the database?"
- "How many mortgages have a loan value greater than the applicant income?"
- "What is the average income of owner occupied applications?"

Type `exit` to quit.

## How It Works

```
Your Computer:
  - Runs database_llm.py
  - Runs LLM (generates SQL)
  - SSH tunnel to ilab
    ↓
ilab:
  - Runs ilab_script.py
  - GSSAPI auth (your ilab credentials)
  - Queries aas517's database
    ↓
Results displayed on your computer
```

## Troubleshooting

**"No module named llama_cpp"**
- Run: `pip3 install llama-cpp-python`

**"Model path does not exist"**
- Make sure you downloaded the model to `./models/phi-3-mini.gguf`

**SSH connection fails**
- Check your ilab username/password
- Make sure you can SSH manually: `ssh your_netid@ilab1.cs.rutgers.edu`

**Database errors**
- You should have been granted access to aas517's database
- Your GSSAPI credentials (from ilab login) allow database access
