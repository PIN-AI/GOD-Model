import argparse
import json
import os
from openai import OpenAI
from prompt_templates import QUESTION_GENERATION_PROMPT
from logging import god_node_logger


def generate_questions(output_file: str, openai_key: str) -> None:
    """
    Generate personalized questions using OpenAI API and save to JSONL file.
    
    Args:
        output_file: Path to save the generated questions
        openai_key: OpenAI API key for authentication
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=openai_key)

    # Generate questions using chat completion
    god_node_logger.info(f"Generating questions using OpenAI API")
    response = client.chat.completions.create(
        model="o1-preview",  # OPENAI Tier 3 is required to use o3-mini. More info: https://platform.openai.com/docs/guides/rate-limits
        messages=[
            {"role": "user", "content": QUESTION_GENERATION_PROMPT}
        ]
    )
    god_node_logger.info(f"Questions generated successfully")

    # Write responses to JSONL file
    god_node_logger.info(f"Writing questions to {output_file}")
    with open(output_file, 'w') as f:
        for choice in response.choices:
            content = choice.message.content
            # Split content into lines and process each JSON object
            for line in content.split('\n'):
                if line.strip():
                    try:
                        json_obj = json.loads(line)
                        f.write(json.dumps(json_obj) + '\n')
                    except json.JSONDecodeError:
                        # Skip invalid JSON lines
                        god_node_logger.warning(f"Invalid JSON line: {line}")
                        continue
    god_node_logger.info(f"Questions written to {output_file}")
	

if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Generate personalized questions using OpenAI')
    
    parser.add_argument('-o', '--output', default='god_node_questions.jsonl',
                       help='Output file path (default: god_node_questions.jsonl)')
    parser.add_argument('-k', '--key', help='OpenAI API key')

    args = parser.parse_args()
    
    # Get API key from args or environment variable
    if args.key is None:
        args.key = os.getenv('OPENAI_API_KEY')
        if not args.key:
            raise ValueError("OPENAI_API_KEY not found")

    generate_questions(args.output, args.key)