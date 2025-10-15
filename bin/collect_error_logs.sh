#!/bin/bash

LOG_DIR="logs/collected_logs"
mkdir -p "$LOG_DIR"

find . -name "*.log" -exec cp {} "$LOG_DIR" \;

echo "Error logs collected in $LOG_DIR"
