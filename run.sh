#!/bin/bash

MODELS=("llama3.1" "llama3.2" "mistral" "phi3" "phi3:14b" "gemma2" "gemma2:27b")
TEMPERATURES=(0.2 0.4 0.6 0.8 1.0)
MAX_TOKENS=(500 1000 1500 2000)
CSV_DIR="${1}"  # Replace with your CSV directory
PROMPT_CSV="${2}"  # Replace with your prompt CSV
OUTPUT_BASE="${3}"     # Replace with your output base directory

# Create timestamp for unique output folder
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

find "$CSV_DIR" -name "*.csv" | while read csv; do
    csv_name=$(basename "$csv" .csv)
    
    for model in "${MODELS[@]}"; do
        for temp in "${TEMPERATURES[@]}"; do
            for tokens in "${MAX_TOKENS[@]}"; do
                # Create specific output directory
                output_dir="${OUTPUT_BASE}/${TIMESTAMP}/${csv_name}/${model}/temp${temp}/tokens${tokens}"
                mkdir -p "$output_dir"
                
                echo "Running metallm with:"
                echo "CSV: $csv"
                echo "Model: $model"
                echo "Temperature: $temp"
                echo "Max Tokens: $tokens"
                echo "Output: $output_dir"
                
                ../bin/metallm \
                    --csv_file_path "$csv" \
                    --question "$PROMPT_CSV" \
                    --output_folder_path "$output_dir" \
                    --model "$model" \
                    --temp "$temp" \
                    --max_tokens "$tokens"
                
                sleep 2  # Small delay between runs to prevent overload
            done
        done
    done
done
