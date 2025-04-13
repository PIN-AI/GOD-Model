
"""

Notes:

Technique: Dynamic Contextual Synthesis 






"""










import argparse
import json
import os
from typing import List, Dict, Any
import torch
from openai import OpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

class OpenAIQuestionGenerator:
    """Class for generating questions using OpenAI models based on vector store data."""
    
    def __init__(self, api_key, vector_store_path, model="gpt-4o"):
        """Initialize the question generator with API key and vector store."""
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.vector_store = self.load_vector_store(vector_store_path)
    
    def load_vector_store(self, vector_store_path: str) -> FAISS:
        """Load a FAISS vector store from disk."""
        print(f"Loading vector store from {vector_store_path}")
        model_name = "BAAI/bge-small-en-v1.5"
        model_kwargs = {'device': "cuda" if torch.cuda.is_available() else "cpu"}
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs
        )
        
        if os.path.exists(vector_store_path):
            return FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
        else:
            raise FileNotFoundError(f"Vector store not found at {vector_store_path}")
        
    def generate_questions(self, data_type: str, num_questions: int = 5, depth_level: str = "medium") -> List[str]:
        """Generate contextual questions based on user data."""
        context_docs = []
        
        
        # KEY WORD ADDITION 
        
        
        if data_type == "steam":
            context_docs.extend(self.vector_store.similarity_search("user gaming profile", k=5))
            context_docs.extend(self.vector_store.similarity_search("top games", k=3))
            context_docs.extend(self.vector_store.similarity_search("game categories", k=3))
            
        elif data_type == "amazon":
            context_docs.extend(self.vector_store.similarity_search("purchase history summary", k=3))
            context_docs.extend(self.vector_store.similarity_search("frequent purchases", k=3))
            context_docs.extend(self.vector_store.similarity_search("expensive purchases", k=3))
            context_docs.extend(self.vector_store.similarity_search("purchase categories", k=3))
            
        elif data_type == "twitter":
            context_docs.extend(self.vector_store.similarity_search("tweet content", k=5))
            context_docs.extend(self.vector_store.similarity_search("tweet topics", k=3))
            context_docs.extend(self.vector_store.similarity_search("twitter activity", k=3))
            
        elif data_type == "crypto":
            context_docs.extend(self.vector_store.similarity_search("wallet holdings", k=3))
            context_docs.extend(self.vector_store.similarity_search("crypto portfolio", k=3))
            context_docs.extend(self.vector_store.similarity_search("defi activity", k=3))
            
        elif data_type == "combined":
            context_docs.extend(self.vector_store.similarity_search("user profile overview", k=3))
            context_docs.extend(self.vector_store.similarity_search("gaming behavior", k=2))
            context_docs.extend(self.vector_store.similarity_search("shopping habits", k=2))
            context_docs.extend(self.vector_store.similarity_search("social media activity", k=2))
            context_docs.extend(self.vector_store.similarity_search("financial behavior", k=2))
        
        seen_contents = set()
        unique_docs = []
        for doc in context_docs:
            if doc.page_content not in seen_contents:
                seen_contents.add(doc.page_content)
                unique_docs.append(doc)
        
        context = "\n\n".join([doc.page_content for doc in unique_docs])
        
        depth_instructions = {
            "shallow": "Ask basic factual questions about the user's behavior and preferences in this domain.",
            "medium": "Ask thoughtful questions that explore motivations, patterns, and relationships between different aspects of the user's behavior in this domain.",
            "deep": "Ask profound questions that explore values, identity, emotional connections, and how this domain relates to the user's life philosophy and worldview."
        }
        
        data_prompts = {
            "steam": {
                "title": "STEAM GAMING PROFILE",
                "instructions": "Generate questions about gaming habits, preferences, and behavior patterns."
            },
            "amazon": {
                "title": "AMAZON PURCHASE HISTORY",
                "instructions": "Generate questions about shopping behavior, product preferences, and spending patterns."
            },
            "twitter": {
                "title": "TWITTER/X SOCIAL MEDIA ACTIVITY",
                "instructions": "Generate questions about social media expression, interests, and engagement patterns."
            },
            "crypto": {
                "title": "CRYPTOCURRENCY WALLET & INVESTMENTS",
                "instructions": "Generate questions about investment strategy, risk tolerance, and financial decision-making."
            },
            "combined": {
                "title": "HOLISTIC USER PROFILE",
                "instructions": "Generate questions that explore connections between different aspects of the user's life (gaming, shopping, social media, finances)."
            }
        }
        
        ############
        
            ## DATA PROMPT + PROMPT + DEPTH INSTRUCTIONS 
        
        ############
        
        
        
        prompt = f"""
        You are an AI designed to understand a human user deeply through thoughtful questions.
        
        {data_prompts[data_type]["title"]} DATA:
        {context}
        
        TASK: Generate {num_questions} questions that:
        1. {depth_instructions[depth_level]}
        2. Test Knowledge about Data Present in RAG 
        2. Are specific to this user's unique profile in the {data_type} domain
        3. Will reveal deeper patterns in their behavior and preferences
        4. Avoid making assumptions about the user
        5. Are varied in their approach and focus

        
        Return ONLY the questions, one per line, numbered 1-{num_questions}.
        """
        
        print(f"\nGenerating {depth_level} questions for {data_type} data using OpenAI {self.model}...")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert at generating insightful questions that reveal deeper patterns of human behavior and preferences."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        generated_text = response.choices[0].message.content
        
        questions = []
        for line in generated_text.strip().split('\n'):
            line = line.strip()
            if line and ('?' in line):
                if line[0].isdigit() and '.' in line[:3]:
                    line = line[line.find('.')+1:].strip()
                questions.append(line)
                
        if len(questions) > num_questions:
            questions = questions[:num_questions]
            
        return questions

def main():
    parser = argparse.ArgumentParser(description="Enhanced Personal AI Question Generator")
    parser.add_argument("--vector_store_dir", type=str, default="./vector_stores",
                        help="Directory containing vector stores")
    parser.add_argument("--data_type", type=str,
                        choices=["steam", "amazon", "twitter", "crypto", "combined", "all"],
                        default="all",
                        help="Type of data to generate questions for")
    parser.add_argument("--questions", type=int, default=5,
                        help="Number of questions to generate in each round")
    parser.add_argument("--openai_key", type=str, default="",
                        help="OpenAI API key (or set OPENAI_API_KEY env variable)")
    parser.add_argument("--model", type=str, default="gpt-4o",
                        help="OpenAI model to use (default: gpt-4o)")
    parser.add_argument("--output_file", type=str, default="",
                        help="Path to save generated questions (optional)")
    
    args = parser.parse_args()
    
    api_key = args.openai_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OpenAI API key is required. Set it with --openai_key or OPENAI_API_KEY environment variable.")
        return
    data_types = []
    if args.data_type == "all":
        data_types = ["steam", "amazon", "twitter", "crypto", "combined"]
    else:
        data_types = [args.data_type]
    
    all_questions = {}
    for data_type in data_types:
        vector_store_path = os.path.join(args.vector_store_dir, data_type)
        
        if not os.path.exists(vector_store_path):
            print(f"Warning: Vector store for {data_type} not found at {vector_store_path}")
            continue
        
        try:
            question_generator = OpenAIQuestionGenerator(
                api_key=api_key,
                vector_store_path=vector_store_path,
                model=args.model
            )
            
            depth_options = {
                "shallow": "Basic factual questions",
                "medium": "Thoughtful questions about motivations and patterns", 
                "deep": "Profound questions about values and identity"
            }
            
            data_type_questions = {}
            
            for depth_level, description in depth_options.items():
                print(f"\n--- GENERATING {depth_level.upper()} QUESTIONS FOR {data_type.upper()} ---")
                try:
                    questions = question_generator.generate_questions(
                        data_type=data_type,
                        num_questions=args.questions, 
                        depth_level=depth_level
                    )
                    
                    data_type_questions[depth_level] = questions
                    
                    print(f"\n{depth_level.capitalize()} Questions ({description}):")
                    for i, question in enumerate(questions):
                        print(f"{i+1}. {question}")
                    
                except Exception as e:
                    print(f"Error generating {depth_level} questions for {data_type}: {e}")
            
            all_questions[data_type] = data_type_questions
            print("\n" + "="*50)
            
        except Exception as e:
            print(f"Error processing {data_type} data: {e}")
    if args.output_file and all_questions:
        try:
            with open(args.output_file, 'w') as f:
                json.dump(all_questions, f, indent=2)
            print(f"Questions saved to {args.output_file}")
        except Exception as e:
            print(f"Error saving questions to file: {e}")
    
    print("\nQuestion generation complete.")

if __name__ == "__main__":
    main()