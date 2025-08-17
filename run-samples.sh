#!/bin/bash

# Agentic Planner CLI - Sample Demonstrations
# Run this script to see all examples with clear separation

echo "========================================================================"
echo "AGENTIC PLANNER CLI - SAMPLE DEMONSTRATIONS"
echo "========================================================================"
echo

# Helper function to run with clear separation
run_sample() {
    echo "▶ RUNNING: $1"
    echo "------------------------------------------------------------------------"
    eval "$1"
    echo
    echo "------------------------------------------------------------------------"
    echo "✓ COMPLETED"
    echo
    read -p "Press Enter to continue to next sample..."
    echo
}

# Sample 1: Basic conversational query
run_sample 'docker run --rm agentic-planner-cli "explain quantum computing to me"'

# Sample 2: Educational request
run_sample 'docker run --rm agentic-planner-cli "help me understand machine learning"'

# Sample 3: Knowledge request
run_sample 'docker run --rm agentic-planner-cli "what should I know about blockchain"'

# Sample 4: Explain mode showing AI reasoning
echo "▶ RUNNING: docker run --rm agentic-planner-cli \"teach me about neural networks\" --explain"
echo "   (This shows how the AI decomposes your goal into steps)"
echo "------------------------------------------------------------------------"
docker run --rm agentic-planner-cli "teach me about neural networks" --explain
echo
echo "------------------------------------------------------------------------"
echo "✓ COMPLETED"
echo
read -p "Press Enter to continue to next sample..."
echo

# Sample 5: Lite model profile
echo "▶ RUNNING: docker run --rm agentic-planner-cli \"what should I know about blockchain\" --model-profile lite"
echo "   (This uses a lighter resource profile for optimized inference)"
echo "------------------------------------------------------------------------"
docker run --rm agentic-planner-cli "what should I know about blockchain" --model-profile lite
echo
echo "------------------------------------------------------------------------"
echo "✓ COMPLETED"
echo

echo "========================================================================"
echo "ALL SAMPLES COMPLETED"
echo "========================================================================"
echo "Key features demonstrated:"
echo "• Conversational goal input"
echo "• Automatic goal decomposition"
echo "• Web search and summarization"
echo "• AI reasoning visibility (--explain)"
echo "• Resource optimization (--model-profile lite)"
echo "========================================================================"