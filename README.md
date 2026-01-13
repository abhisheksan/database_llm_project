# Natural Language Database Query System

A natural language interface for querying PostgreSQL databases using local LLM technology. This project demonstrates advanced prompt engineering, secure remote database access, and practical application of small language models for SQL generation.

## Overview

This system bridges the gap between natural language and structured database queries by leveraging Microsoft's Phi-3 mini LLM. Users can ask questions in plain English, which are intelligently converted to SQL queries and executed against a PostgreSQL mortgage loan database containing real-world lending data.

**Key Features:**
- **Local LLM Processing**: Runs Phi-3 mini locally for privacy and low-latency inference
- **Intelligent SQL Generation**: Advanced prompt engineering with few-shot learning examples
- **Secure Remote Execution**: SSH tunnel with GSSAPI authentication for database access
- **Interactive CLI**: Real-time query generation and results display
- **Optimized Context Management**: Efficient schema summarization to fit within 2048-token context window

## Technical Stack

**Language Model:**
- Microsoft Phi-3 mini (4K context, 4-bit quantized GGUF format)
- llama-cpp-python for efficient CPU inference

**Backend:**
- Python 3.x
- PostgreSQL database with mortgage lending data
- psycopg2 for database connectivity
- Paramiko for SSH tunneling

**Security:**
- GSSAPI/Kerberos authentication
- Secure password handling with getpass
- Query validation (SELECT-only execution)

## Architecture

```
┌─────────────────────────────────────┐
│   User Input (Natural Language)    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Phi-3 Mini LLM (Local Inference)   │
│  - Schema-aware prompt engineering  │
│  - Few-shot learning examples       │
│  - Stop token optimization          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     Generated SQL Query             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  SSH Tunnel (Paramiko)              │
│  - Secure authentication            │
│  - Remote command execution         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  PostgreSQL Database (Remote)       │
│  - GSSAPI authentication            │
│  - Query execution & results        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Formatted Results Display         │
└─────────────────────────────────────┘
```

## Installation

### Prerequisites
- Python 3.7+
- SSH access to remote database server
- ~4GB RAM for LLM inference

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/database-nlp-query.git
cd database-nlp-query
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install llama-cpp-python paramiko psycopg2-binary
```

3. **Download the LLM model**
```bash
mkdir -p models
curl -L -o models/phi-3-mini.gguf \
  "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
```

4. **Configure database connection**
Edit `database_llm.py` to set your remote server details (default: ilab1.cs.rutgers.edu)

## Usage

Run the interactive query system:

```bash
python3 database_llm.py
```

You'll be prompted for SSH credentials, then you can ask questions in plain English:

**Example Queries:**
```
Your question: How many loan applications are in the database?
Generated SQL: SELECT COUNT(*) FROM application

Your question: What is the average income for owner-occupied properties?
Generated SQL: SELECT AVG(a.applicant_income_000s) FROM application a
               JOIN owner_occupancy o ON a.owner_occupancy=o.owner_occupancy
               WHERE o.owner_occupancy_name ILIKE '%owner%'

Your question: How many applications were denied?
Generated SQL: SELECT COUNT(*) FROM application a
               JOIN action_taken t ON a.action_taken=t.action_taken
               WHERE t.action_taken_name ILIKE '%denied%'
```

Type `exit` to quit.

## Prompt Engineering Techniques

This project employs several advanced techniques for reliable SQL generation:

1. **Schema Compression**: Dynamically extracts and summarizes table structures to fit within token limits
2. **Few-Shot Learning**: Provides concrete query examples in the prompt
3. **Explicit Relationship Mapping**: Documents all foreign key relationships with data types
4. **Stop Token Optimization**: Uses semicolons and keywords to prevent hallucinated explanations
5. **Phi-3 Instruct Format**: Leverages model-specific special tokens (`<|system|>`, `<|user|>`, `<|assistant|>`, `<|end|>`)

## Technical Implementation Details

### Challenges Solved

- **Token Budget Management**: Reduced schema from full DDL to minimal table/column listing
- **Clean SQL Output**: Implemented multi-stage response parsing to remove LLM explanations
- **Type-Safe Joins**: Explicitly documented numeric join keys to prevent text-based join errors
- **Secure Authentication**: Integrated GSSAPI for passwordless database access
- **Error Handling**: Comprehensive validation and fallback mechanisms

### Key Insights

- LLM output quality is highly sensitive to prompt structure and special tokens
- Stop tokens are critical for preventing unwanted model verbosity
- Explicit foreign key documentation significantly improves JOIN accuracy
- Schema summarization is essential for working within context window constraints

## Project Structure

```
database_llm_project/
├── database_llm.py          # Main client application (local LLM + SSH)
├── ilab_script.py           # Remote query execution script
├── schema.sql               # Database schema definition
├── create_application.sql   # Table creation script
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── SETUP_INSTRUCTIONS.md    # Detailed setup guide
├── LICENSE                  # MIT License
├── .gitignore              # Git ignore rules
└── models/
    └── phi-3-mini.gguf      # LLM model (downloaded separately)
```

## Database Schema

The system queries a mortgage loan database with the following structure:
- **application**: Main table with loan applications (~500K rows)
- **Lookup tables**: agency, action_taken, loan_type, property_type, owner_occupancy, denial_reason, state, county

All relationships use numeric foreign keys for efficient joins.

## Future Enhancements

Potential improvements and extensions:

- **Multi-Database Support**: Adapt schema loading for different database types (MySQL, SQLite, etc.)
- **Query Caching**: Implement LRU cache for frequently asked questions
- **Web Interface**: Build a Flask/FastAPI frontend with chat-like UI
- **Fine-tuning**: Custom model fine-tuning on domain-specific SQL patterns
- **Streaming Results**: Support for large result sets with pagination
- **Query Explanations**: Add natural language explanations of generated SQL
- **Visual Analytics**: Automatic chart generation for numerical results

## Performance Metrics

Typical performance characteristics on a modern laptop:

- **Model Loading**: 30-60 seconds (one-time cost)
- **SQL Generation**: 2-5 seconds per query
- **Database Execution**: 0.1-3 seconds depending on complexity
- **Total Response Time**: 3-8 seconds end-to-end
- **Memory Usage**: ~3.5GB (primarily LLM model)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Microsoft Phi-3**: For providing an efficient, high-quality small language model
- **llama.cpp**: For enabling efficient CPU inference of quantized models
- **PostgreSQL**: For robust, reliable database management
- **Home Mortgage Disclosure Act (HMDA)**: For providing the public mortgage lending dataset
