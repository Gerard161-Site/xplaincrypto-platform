#!/bin/bash

# Setup script for Automatos AI Testing Repository
# Run this script to transfer files from local workspace to server

echo "🚀 Setting up Automatos AI Testing Repository..."

# Define server details
SERVER="root@206.81.0.227"
REMOTE_DIR="/root/automatos-testing"
SSH_KEY="~/.ssh/id_rsa"

echo "📁 Transferring files to server..."

# Copy all repository files
scp -i $SSH_KEY README.md $SERVER:$REMOTE_DIR/
scp -i $SSH_KEY requirements.txt $SERVER:$REMOTE_DIR/
scp -i $SSH_KEY .gitignore $SERVER:$REMOTE_DIR/
scp -i $SSH_KEY LICENSE $SERVER:$REMOTE_DIR/
scp -i $SSH_KEY CONTRIBUTING.md $SERVER:$REMOTE_DIR/

echo "📋 Setting up git repository..."

# Setup git on server
ssh -i $SSH_KEY $SERVER "cd $REMOTE_DIR && \
    git init && \
    git add . && \
    git commit -m 'Initial commit: Automatos AI testing suite' && \
    git remote add origin git@github.com:AutomatosAI/automatos-testing.git && \
    git push -u origin main"

echo "✅ Repository setup complete!"
echo "🌐 Your repo is now live at: https://github.com/AutomatosAI/automatos-testing"
echo ""
echo "🧪 To run tests:"
echo "   cd $REMOTE_DIR/testing_suites/comprehensive_5phase"
echo "   python3 run_all_tests.py"