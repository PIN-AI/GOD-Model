import argparse
import json
import os
import logging
from pathlib import Path
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def read_category_prompt(category: str) -> str:
    """
    Read the prompt template for a specific category.
    
    Args:
        category: Category name (e.g., 'social', 'productivity')
    
    Returns:
        str: The prompt template for the category
    """
    prompt_file = Path(f"question_generation/{category}_prompts.txt")
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found for category: {category}")
    
    with open(prompt_file, 'r') as f:
        return f.read()

def generate_questions_for_category(category: str, client: OpenAI) -> dict:
    """
    Generate questions for a specific category using OpenAI API.
    
    Args:
        category: Category name (e.g., 'social', 'productivity')
        client: OpenAI client instance
    
    Returns:
        dict: Generated questions in JSON format
    """
    prompt = read_category_prompt(category)
    
    logger.info(f"Generating questions for category: {category}")
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract JSON from response
    content = response.choices[0].message.content
    try:
        # Find JSON object in the response
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON object found in response")
        
        json_str = content[json_start:json_end]
        return json.loads(json_str)
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Failed to parse JSON for category {category}: {str(e)}")
        raise

def generate_all_questions(output_dir: str, openai_key: str) -> None:
    """
    Generate questions for all categories and save to JSON files.
    
    Args:
        output_dir: Directory to save the generated questions
        openai_key: OpenAI API key for authentication
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=openai_key)
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Categories to process
    categories = ['social', 'productivity', 'daily_life', 'shopping', 'web3', 'finance']
    
    # Process each category
    for category in categories:
        try:
            questions = generate_questions_for_category(category, client)
            
            # Save to category-specific file
            output_file = output_path / f"{category}_questions.json"
            with open(output_file, 'w') as f:
                json.dump(questions, f, indent=2)
            
            logger.info(f"Questions for {category} saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to generate questions for {category}: {str(e)}")
            continue

if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Generate personalized questions using OpenAI')
    
    parser.add_argument('-o', '--output', default='generated_questions',
                       help='Output directory path (default: generated_questions)')
    parser.add_argument('-k', '--key', help='OpenAI API key')

    args = parser.parse_args()
    
    # Get API key from args or environment variable
    if args.key is None:
        args.key = os.getenv('OPENAI_API_KEY')
        if not args.key:
            raise ValueError("OPENAI_API_KEY not found")

    # Generate questions for all categories
    generate_all_questions(args.output, args.key)