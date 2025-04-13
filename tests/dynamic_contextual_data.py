import unittest
from unittest.mock import patch, MagicMock
from langchain_core.documents import Document
from enhanced_question_generator import OpenAIQuestionGenerator

class MockVectorStore:
    def __init__(self, docs_to_return=None):
        self.docs_to_return = docs_to_return or []
        
    def similarity_search(self, query, k=3):
        return self.docs_to_return[:k]

class TestOpenAIQuestionGenerator(unittest.TestCase):
    
    @patch('enhanced_question_generator.OpenAI')
    @patch('enhanced_question_generator.FAISS')
    def test_generate_questions(self, mock_faiss, mock_openai):
        # Setup mocks
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = """
        1. What draws you to multiplayer games like Counter-Strike?
        2. How do your gaming habits reflect your social preferences?
        3. What patterns do you notice in your book purchasing behavior?
        """
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # Create mock documents
        mock_docs = [
            Document(page_content="User owns 150 games on Steam", metadata={"source": "games_summary"}),
            Document(page_content="Top game: Counter-Strike - Played for 5000 minutes", metadata={"source": "top_game"}),
            Document(page_content="Made 15 purchases in the 'Books' category", metadata={"source": "category_pattern"})
        ]
        mock_faiss.load_local.return_value = MockVectorStore(mock_docs)
        
        # Test generating questions
        generator = OpenAIQuestionGenerator("test_api_key", "fake_path")
        questions = generator.generate_questions(data_type="combined", num_questions=2)
        
        # Assertions
        self.assertEqual(len(questions), 2)
        self.assertTrue(any(["multiplayer" in q.lower() or "gaming" in q.lower() for q in questions]))
        
        # Verify correct model is used
        mock_client.chat.completions.create.assert_called_once()
        self.assertEqual(mock_client.chat.completions.create.call_args[1]["model"], "gpt-4o")

if __name__ == "__main__":
    unittest.main()