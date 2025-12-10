# Database LLM Project - Project 2

Natural language interface for querying mortgage loan database using a local LLM.

## Team Members
- **aas517**: Database setup on ilab, ilab_script.py development, schema creation, database access management, documentation
- **mjm857**: Local LLM setup, prompt engineering, SSH tunnel integration, video demonstration
- **ds2072**: Testing and query validation
- **asj99**: Testing and error handling verification


## Contributions
- **aas517**: Created and deployed ilab_script.py on ilab server, set up PostgreSQL database with mortgage data from Project 1, granted database access to team members, configured GSSAPI authentication, created schema.sql file for LLM, wrote README and setup documentation, compiled chat transcripts
- **mjm857**: Set up local LLM (Phi-3 mini), implemented database_llm.py with SSH tunnel using paramiko, developed prompt engineering with Phi-3 instruct format, tested and debugged SQL generation, recorded video demonstration of working queries
- **ds2072**: Assisted with testing the complete system against the three required test queries (loan > income, owner occupied average, denial reasons), helped validate SQL query correctness, provided feedback on prompt improvements
- **asj99**: Helped test error handling for malformed queries and connection failures, verified the authentication flow works correctly, assisted with troubleshooting GSSAPI connection issues during development

## What We Found Challenging
- Getting the LLM to generate valid SQL queries without extra explanatory text
- Managing the 2048 token context window - had to create very concise schema summaries
- Configuring the Phi-3 instruct format correctly with proper special tokens
- Debugging JOIN syntax errors - LLM initially tried to join on TEXT columns instead of code columns
- Setting up GSSAPI authentication for passwordless database access on ilab
- Handling SSH tunnel security with getpass for password input

## What We Found Interesting
- How sensitive LLMs are to prompt format - using Phi-3's special tokens (`<|system|>`, `<|user|>`, `<|assistant|>`) made a huge difference
- The importance of explicit foreign key relationship documentation in the prompt
- How stop tokens affect LLM output - semicolon as a stop token prevented the model from adding explanations
- GSSAPI authentication allowing seamless database access without password prompts on ilab
- The trade-off between schema detail and context window limits

## Did You Do the Extra Credit?
No, we did not implement the stdin version for extra credit.

## Files Included
- `database_llm.py` - Main program that runs locally with LLM
- `ilab_script.py` - Script that runs on ilab to execute SQL queries
- `schema.sql` - Database schema fed to the LLM
- `SETUP_INSTRUCTIONS.md` - Detailed setup guide for team members
- Video demonstration showing successful queries (link in submission)
