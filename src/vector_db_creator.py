#!/usr/bin/env python3
# DATE: 11/03/2025
# SCRIPT: PERSONAL AI VECTOR DATABASE CREATOR
# INFERENCE MODEL: Hugging Face Embeddings

import argparse
import json
import os
import csv
import pandas as pd
from typing import List, Dict, Any, Optional
import torch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

def load_steam_data(file_path: str) -> List[Document]:
    """Load and process Steam user data into Document objects."""
    print(f"Loading Steam data from {file_path}")
    with open(file_path, 'r') as f:
        data = json.load(f)
    documents = []
    if 'BasicInfo' in data:
        user_info = f"Steam User ID: {data['BasicInfo']['steamid']}, Username: {data['BasicInfo']['personaname']}, Profile URL: {data['BasicInfo']['profileurl']}"
        documents.append(Document(page_content=user_info, metadata={"source": "user_info", "data_type": "steam"}))
    if 'OwnedGames' in data:
        game_count = data['OwnedGames']['game_count']
        games_info = f"The user owns {game_count} games on Steam."
        documents.append(Document(page_content=games_info, metadata={"source": "games_summary", "data_type": "steam"}))
        total_playtime = sum(game['playtime_forever'] for game in data['OwnedGames']['games'])
        playtime_info = f"The user has spent a total of {total_playtime} minutes (approximately {total_playtime/60:.2f} hours) playing games on Steam."
        documents.append(Document(page_content=playtime_info, metadata={"source": "playtime_summary", "data_type": "steam"}))
        sorted_games = sorted(data['OwnedGames']['games'], key=lambda x: x['playtime_forever'], reverse=True)
        top_games = sorted_games[:15]  
        for i, game in enumerate(top_games):
            game_info = f"Game Rank {i+1}: {game['name']} - Played for {game['playtime_forever']} minutes (approximately {game['playtime_forever']/60:.2f} hours)"
            documents.append(Document(page_content=game_info, metadata={"source": "top_game", "rank": i+1, "game_id": game['appid'], "data_type": "steam"}))
        category_games = {}
        for game in data['OwnedGames']['games']:
            if 'categories' in game:
                for category in game['categories']:
                    cat_desc = category['description']
                    if cat_desc not in category_games:
                        category_games[cat_desc] = []
                    category_games[cat_desc].append(game['name'])
        
        for category, games in category_games.items():
            category_info = f"Category: {category} - Games: {', '.join(games[:20])}"
            if len(games) > 20:
                category_info += f" and {len(games) - 20} more."
            documents.append(Document(page_content=category_info, metadata={"source": "category", "category": category, "data_type": "steam"}))
        
        for game in [g for g in data['OwnedGames']['games'] if g['playtime_forever'] > 600]:
            game_details = f"Game: {game['name']} (App ID: {game['appid']})\n"
            game_details += f"Playtime: {game['playtime_forever']} minutes (approximately {game['playtime_forever']/60:.2f} hours)\n"
            
            if 'categories' in game:
                categories = [cat['description'] for cat in game['categories']]
                game_details += f"Categories: {', '.join(categories)}"
            
            documents.append(Document(page_content=game_details, metadata={"source": "game_details", "game_id": game['appid'], "game_name": game['name'], "data_type": "steam"}))
    
    return documents

def load_amazon_data(file_path: str) -> List[Document]:
    """Load and process Amazon purchase history into Document objects."""
    print(f"Loading Amazon purchase history from {file_path}")
    documents = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        import io
        df = pd.read_csv(io.StringIO(content))
        num_orders = df['Order ID'].nunique()
        num_products = len(df)
        date_range = f"{df['Order Date'].min()} to {df['Order Date'].max()}"
        
        summary = f"Amazon purchase history contains {num_orders} orders with {num_products} products purchased from {date_range}."
        documents.append(Document(page_content=summary, metadata={"source": "amazon_summary", "data_type": "amazon"}))
        product_counts = df['Product Name'].value_counts()
        for product, count in product_counts.items():
            if count > 1 and isinstance(product, str):
                repeat_info = f"Purchased '{product}' {count} times."
                documents.append(Document(page_content=repeat_info, metadata={"source": "repeat_purchase", "product": product, "data_type": "amazon"}))
        
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        recent_purchases = df.sort_values('Order Date', ascending=False).head(10)
        for _, row in recent_purchases.iterrows():
            if isinstance(row['Product Name'], str):
                purchase_info = f"Recently purchased '{row['Product Name']}' on {row['Order Date']}."
                documents.append(Document(page_content=purchase_info, metadata={"source": "recent_purchase", "date": str(row['Order Date']), "data_type": "amazon"}))
        
        if 'Unit Price' in df.columns:
            df['Unit Price'] = pd.to_numeric(df['Unit Price'], errors='coerce')
            expensive_items = df[df['Unit Price'] > 100]
            for _, row in expensive_items.iterrows():
                if isinstance(row['Product Name'], str):
                    expensive_info = f"Made a high-value purchase of '{row['Product Name']}' for ${row['Unit Price']} on {row['Order Date']}."
                    documents.append(Document(page_content=expensive_info, metadata={"source": "expensive_purchase", "price": row['Unit Price'], "data_type": "amazon"}))
        
        categories = []
        for product in df['Product Name']:
            if isinstance(product, str):
                if "book" in product.lower():
                    categories.append("Books")
                elif any(term in product.lower() for term in ["phone", "iphone", "android", "case", "screen protector"]):
                    categories.append("Electronics & Phone Accessories")
                elif any(term in product.lower() for term in ["kitchen", "food", "coffee", "tea"]):
                    categories.append("Kitchen & Food")
                elif any(term in product.lower() for term in ["clean", "cleaner", "soap", "detergent"]):
                    categories.append("Cleaning Supplies")
                else:
                    categories.append("Other")
        
        category_counts = pd.Series(categories).value_counts()
        for category, count in category_counts.items():
            if count > 3:  
                category_info = f"Made {count} purchases in the '{category}' category."
                documents.append(Document(page_content=category_info, metadata={"source": "category_pattern", "category": category, "data_type": "amazon"}))
        for _, row in df.iterrows():
            if isinstance(row['Product Name'], str):
                order_info = f"Order: {row['Order ID']} - Purchased '{row['Product Name']}'"
                if 'Unit Price' in row and pd.notna(row['Unit Price']):
                    order_info += f" for ${row['Unit Price']}"
                if 'Order Date' in row and pd.notna(row['Order Date']):
                    order_info += f" on {row['Order Date']}"
                
                documents.append(Document(page_content=order_info, metadata={"source": "order_detail", "order_id": row['Order ID'], "data_type": "amazon"}))
        
    except Exception as e:
        print(f"Error processing Amazon data: {e}")
        documents.append(Document(page_content=f"Error processing Amazon data: {str(e)}", metadata={"source": "error", "data_type": "amazon"}))
    
    return documents

def load_twitter_data(file_path: str) -> List[Document]:
    """Load and process Twitter/X posts into Document objects."""
    print(f"Loading Twitter/X data from {file_path}")
    documents = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        tweets = []
        for line in content.split('\n'):
            if '"full_text" :' in line:
                tweet_text = line.split('"full_text" : "')[1].rstrip('",')
                tweets.append(tweet_text)
        
        summary = f"Twitter activity contains {len(tweets)} tweets/posts."
        documents.append(Document(page_content=summary, metadata={"source": "twitter_summary", "data_type": "twitter"}))
        for i, tweet in enumerate(tweets):
            if tweet:
                tweet_doc = f"Tweet {i+1}: {tweet}"
                documents.append(Document(page_content=tweet_doc, metadata={"source": "tweet", "tweet_number": i+1, "data_type": "twitter"}))
        
        topics = {
            "crypto": 0,
            "ai": 0,
            "technology": 0,
            "personal": 0,
            "business": 0
        }
        
        for tweet in tweets:
            lower_tweet = tweet.lower()
            if any(term in lower_tweet for term in ["crypto", "bitcoin", "ethereum", "token", "blockchain", "defi"]):
                topics["crypto"] += 1
            if any(term in lower_tweet for term in ["ai", "artificial intelligence", "ml", "machine learning"]):
                topics["ai"] += 1
            if any(term in lower_tweet for term in ["tech", "technology", "software", "hardware", "device"]):
                topics["technology"] += 1
            if any(term in lower_tweet for term in ["i", "me", "my", "we", "our", "us"]):
                topics["personal"] += 1
            if any(term in lower_tweet for term in ["business", "company", "startup", "product", "service"]):
                topics["business"] += 1
        
        for topic, count in topics.items():
            if count > 0:
                topic_info = f"User has {count} tweets related to {topic}."
                documents.append(Document(page_content=topic_info, metadata={"source": "topic_analysis", "topic": topic, "data_type": "twitter"}))
        
    except Exception as e:
        print(f"Error processing Twitter data: {e}")
        documents.append(Document(page_content=f"Error processing Twitter data: {str(e)}", metadata={"source": "error", "data_type": "twitter"}))
    
    return documents

def load_crypto_wallet_data(file_path: str) -> List[Document]:
    """Load and process cryptocurrency wallet information into Document objects."""
    print(f"Loading crypto wallet data from {file_path}")
    documents = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split("\n")
        wallet_address = ""
        for line in lines:
            if line.startswith("Wallet address:"):
                wallet_address = line.split("Wallet address:")[1].strip()
                break
        
        if wallet_address:
            wallet_doc = f"Ethereum wallet address: {wallet_address}"
            documents.append(Document(page_content=wallet_doc, metadata={"source": "wallet_address", "address": wallet_address, "data_type": "crypto"}))
        
        start_idx = content.find("# Wallet Analysis:")
        if start_idx != -1:
            analysis_section = content[start_idx:]
            sections = {
                "Assets Summary": (analysis_section.find("## Assets Summary"), analysis_section.find("## Portfolio Analysis")),
                "Portfolio Analysis": (analysis_section.find("## Portfolio Analysis"), len(analysis_section))
            }
            
            for section_name, (start, end) in sections.items():
                if start != -1:
                    section_content = analysis_section[start:end if end != -1 else len(analysis_section)]
                    subsections = section_content.split("###")
                    for i, subsection in enumerate(subsections):
                        if i > 0:  
                            subsection_title = subsection.split("\n")[0].strip()
                            subsection_content = "\n".join(subsection.split("\n")[1:]).strip()
                            if subsection_content:
                                doc = f"{section_name} - {subsection_title}: {subsection_content}"
                                documents.append(Document(page_content=doc, metadata={"source": f"{section_name.lower().replace(' ', '_')}_{subsection_title.lower().replace(' ', '_')}", "data_type": "crypto"}))
            
            holdings = []
            if "Token Holdings:" in analysis_section:
                holdings_section = analysis_section[analysis_section.find("Token Holdings:"):analysis_section.find("### DeFi Positions:")]
                for line in holdings_section.split("\n"):
                    if line.strip().startswith("**") and ":" in line:
                        holdings.append(line.strip())
            
            if holdings:
                holdings_doc = "Token Holdings: " + ", ".join(holdings)
                documents.append(Document(page_content=holdings_doc, metadata={"source": "token_holdings", "data_type": "crypto"}))
            
            portfolio_value = ""
            if "### Total Portfolio Value:" in analysis_section:
                for line in analysis_section.split("\n"):
                    if "Total Portfolio Value:" in line:
                        portfolio_value = line.strip()
                        break
            
            if portfolio_value:
                documents.append(Document(page_content=portfolio_value, metadata={"source": "portfolio_value", "data_type": "crypto"}))
            
    except Exception as e:
        print(f"Error processing crypto wallet data: {e}")
        documents.append(Document(page_content=f"Error processing crypto wallet data: {str(e)}", metadata={"source": "error", "data_type": "crypto"}))
    
    return documents

def create_vector_store(documents: List[Document], output_dir: str, device: str) -> FAISS:
    """Create and save FAISS vector store from documents."""
    print(f"Creating vector store with {len(documents)} documents...")
    model_name = "BAAI/bge-small-en-v1.5"
    model_kwargs = {'device': device}
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs
    )
    
    vector_store = FAISS.from_documents(documents, embeddings)
    os.makedirs(output_dir, exist_ok=True)
    vector_store.save_local(output_dir)
    print(f"Vector store saved to {output_dir}")
    
    return vector_store

def main():
    parser = argparse.ArgumentParser(description="Create vector databases for Personal AI")
    parser.add_argument("--output_dir", type=str, default="./vector_stores",
                        help="Directory to save vector stores")
    parser.add_argument("--steam_file", type=str, default="steam.json",
                        help="Path to Steam JSON data file")
    parser.add_argument("--amazon_file", type=str, default="amazon_shopping_history.txt",
                        help="Path to Amazon shopping history file")
    parser.add_argument("--twitter_file", type=str, default="tweets.txt",
                        help="Path to Twitter/X posts file")
    parser.add_argument("--crypto_file", type=str, default="wallet_information.txt",
                        help="Path to crypto wallet information file")
    parser.add_argument("--device", type=str, choices=['auto', 'cuda', 'cpu'], default='auto',
                        help="Compute device to use for embeddings: cuda, cpu, or auto (default)")
    parser.add_argument("--datasets", type=str, nargs='+', 
                        choices=['all', 'steam', 'amazon', 'twitter', 'crypto'], default=['all'],
                        help="Datasets to process (default: all)")
    
    args = parser.parse_args()
    
    if args.device == 'auto':
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = args.device
        if device == 'cuda' and not torch.cuda.is_available():
            print("WARNING: CUDA requested but not available. Using CPU instead.")
            device = "cpu"
    
    print(f"Using device: {device}")
    
    datasets_to_process = args.datasets
    if 'all' in datasets_to_process:
        datasets_to_process = ['steam', 'amazon', 'twitter', 'crypto']
    
    all_documents = []
    
    if 'steam' in datasets_to_process:
        if os.path.exists(args.steam_file):
            steam_docs = load_steam_data(args.steam_file)
            print(f"Loaded {len(steam_docs)} documents from Steam data")
            all_documents.extend(steam_docs)
            steam_dir = os.path.join(args.output_dir, "steam")
            create_vector_store(steam_docs, steam_dir, device)
        else:
            print(f"Steam data file not found: {args.steam_file}")
    
    if 'amazon' in datasets_to_process:
        if os.path.exists(args.amazon_file):
            amazon_docs = load_amazon_data(args.amazon_file)
            print(f"Loaded {len(amazon_docs)} documents from Amazon data")
            all_documents.extend(amazon_docs)
            amazon_dir = os.path.join(args.output_dir, "amazon")
            create_vector_store(amazon_docs, amazon_dir, device)
        else:
            print(f"Amazon data file not found: {args.amazon_file}")
    
    if 'twitter' in datasets_to_process:
        if os.path.exists(args.twitter_file):
            twitter_docs = load_twitter_data(args.twitter_file)
            print(f"Loaded {len(twitter_docs)} documents from Twitter data")
            all_documents.extend(twitter_docs)
            twitter_dir = os.path.join(args.output_dir, "twitter")
            create_vector_store(twitter_docs, twitter_dir, device)
        else:
            print(f"Twitter data file not found: {args.twitter_file}")
    
    if 'crypto' in datasets_to_process:
        if os.path.exists(args.crypto_file):
            crypto_docs = load_crypto_wallet_data(args.crypto_file)
            print(f"Loaded {len(crypto_docs)} documents from Crypto wallet data")
            all_documents.extend(crypto_docs)
            crypto_dir = os.path.join(args.output_dir, "crypto")
            create_vector_store(crypto_docs, crypto_dir, device)
        else:
            print(f"Crypto wallet data file not found: {args.crypto_file}")
    
    if len(all_documents) > 0:
        combined_dir = os.path.join(args.output_dir, "combined")
        create_vector_store(all_documents, combined_dir, device)
        print(f"Created combined vector store with {len(all_documents)} documents")
    else:
        print("No documents were loaded. Check file paths and try again.")

if __name__ == "__main__":
    main()