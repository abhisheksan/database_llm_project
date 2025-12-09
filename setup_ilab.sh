#!/bin/bash
# Setup script for ilab - sets environment variables for database access

echo "Setting up database credentials for ilab_script.py"
echo ""
echo "Enter database credentials:"
read -p "Database name [aas517]: " db_name
db_name=${db_name:-aas517}

read -p "Database user [aas517]: " db_user
db_user=${db_user:-aas517}

read -sp "Database password: " db_password
echo ""

# Export environment variables
export DB_NAME="$db_name"
export DB_USER="$db_user"
export DB_PASSWORD="$db_password"

echo ""
echo "Environment variables set. You can now run:"
echo "  python3 ilab_script.py 'SELECT 1'"
echo ""
echo "These will only persist in this shell session."
