#!/usr/bin/env python3
# DATE: 11/03/2025
# SCRIPT: PERSONAL AI PIPELINE
# DESCRIPTION: Orchestrates the entire Personal AI data processing and question generation pipeline

import argparse
import os
import subprocess
import json
import time
from datetime import datetime

def run_vector_db_creation(args_dict):
    """Run the vector database creation script with the provided arguments."""
    print("\n" + "="*80)
    print("STAGE 1: CREATING VECTOR DATABASES")
    print("="*80)
    cmd = ["python", "src/vector_db_creator.py"]
    for key, value in args_dict.items():
        if isinstance(value, list):
            cmd.append(f"--{key}")
            cmd.extend(value)
        elif value is not None:
            cmd.append(f"--{key}")
            cmd.append(str(value))
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("\nOutput:")
    print(result.stdout)
    
    if result.returncode != 0:
        print("\nError:")
        print(result.stderr)
        print(f"Vector database creation failed with exit code {result.returncode}")
        return False
    
    return True

def run_question_generation(args_dict):
    """Run the question generation script with the provided arguments."""
    print("\n" + "="*80)
    print("STAGE 2: GENERATING QUESTIONS")
    print("="*80)
    
    cmd = ["python", "src/enhanced_question_generator.py"]
    for key, value in args_dict.items():
        if value is not None:
            cmd.append(f"--{key}")
            cmd.append(str(value))
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print("\nOutput:")
    print(result.stdout)
    
    if result.returncode != 0:
        print("\nError:")
        print(result.stderr)
        print(f"Question generation failed with exit code {result.returncode}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Personal AI Pipeline - Process user data and generate intricate questions")
    parser.add_argument("--output_dir", type=str, default="./output",
                        help="Directory to save all outputs")
    parser.add_argument("--openai_key", type=str, default="",
                        help="OpenAI API key (or set OPENAI_API_KEY env variable)")
    parser.add_argument("--device", type=str, choices=['auto', 'cuda', 'cpu'], default='auto',
                        help="Compute device to use for embeddings")
    parser.add_argument("--model", type=str, default="gpt-4o",
                        help="OpenAI model to use for question generation")
    parser.add_argument("--steam_file", type=str, default="steam.json",
                        help="Path to Steam JSON data file")
    parser.add_argument("--amazon_file", type=str, default="amazon_shopping_history.txt",
                        help="Path to Amazon shopping history file")
    parser.add_argument("--twitter_file", type=str, default="tweets.txt",
                        help="Path to Twitter/X posts file")
    parser.add_argument("--crypto_file", type=str, default="wallet_information.txt",
                        help="Path to crypto wallet information file")
    parser.add_argument("--datasets", type=str, nargs='+', 
                        choices=['all', 'steam', 'amazon', 'twitter', 'crypto'], default=['all'],
                        help="Datasets to process (default: all)")
    parser.add_argument("--questions", type=int, default=5,
                        help="Number of questions to generate in each category")
    parser.add_argument("--skip_vector_creation", action="store_true",
                        help="Skip vector database creation and use existing ones")
    parser.add_argument("--skip_question_generation", action="store_true",
                        help="Skip question generation")
    
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    vector_store_dir = os.path.join(args.output_dir, "vector_stores")
    os.makedirs(vector_store_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    questions_file = os.path.join(args.output_dir, f"questions_{timestamp}.json")
    if not args.skip_vector_creation:
        vector_db_args = {
            "output_dir": vector_store_dir,
            "steam_file": args.steam_file,
            "amazon_file": args.amazon_file,
            "twitter_file": args.twitter_file,
            "crypto_file": args.crypto_file,
            "device": args.device,
            "datasets": args.datasets
        }
        success = run_vector_db_creation(vector_db_args)
        if not success:
            print("Vector database creation failed. Exiting pipeline.")
            return
    else:
        print("\nSkipping vector database creation as requested.")
    
    if not args.skip_question_generation:
        if not args.skip_vector_creation:
            print("\nWaiting for vector stores to be fully saved...")
            time.sleep(2)
        
        question_gen_args = {
            "vector_store_dir": vector_store_dir,
            "data_type": "all",  
            "questions": args.questions,
            "openai_key": args.openai_key,
            "model": args.model,
            "output_file": questions_file
        }
        success = run_question_generation(question_gen_args)
        if not success:
            print("Question generation failed.")
        else:
            print(f"\nAll questions have been saved to {questions_file}")
    else:
        print("\nSkipping question generation as requested.")
    print("\n" + "="*80)
    print("PERSONAL AI PIPELINE COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()