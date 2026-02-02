"""
RAG (Retrieval-Augmented Generation) Engine
Uses GPT-4o to generate personalized practice advice based on difficulty classification.
"""

import json
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


def load_knowledge_base():
    """
    Load the knowledge base containing practice advice for each difficulty category.
    
    Returns:
        dict: Knowledge base dictionary
    """
    kb_path = Path(__file__).parent / "knowledge_base.json"
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        knowledge_base = json.load(f)
    
    return knowledge_base


def query_gpt4o(prompt, api_key=None):
    """
    Query GPT-4o with a prompt.
    
    Args:
        prompt (str): The prompt to send to GPT-4o
        api_key (str, optional): OpenAI API key (uses env var if not provided)
        
    Returns:
        str: GPT-4o response
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
    
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert piano teacher providing personalized practice advice."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error querying GPT-4o: {str(e)}")
        return None


def generate_advice(difficulty_category, features, piece_info=None):
    """
    Generate personalized practice advice using RAG.
    
    Args:
        difficulty_category (str): Predicted difficulty category
        features (dict): Extracted features from MIDI file
        piece_info (dict, optional): Additional piece information (composer, title)
        
    Returns:
        dict: Advice dictionary with structured recommendations
    """
    # Load knowledge base
    kb = load_knowledge_base()
    
    # Get category-specific knowledge
    if difficulty_category not in kb:
        return {
            'error': f"Unknown difficulty category: {difficulty_category}",
            'category': difficulty_category
        }
    
    category_info = kb[difficulty_category]
    
    # Build context for GPT-4o
    context = f"""
You are analyzing a piano piece with the following characteristics:

**Technical Category**: {difficulty_category}
**Category Description**: {category_info['description']}

**Extracted Features**:
- Maximum hand stretch: {features.get('max_stretch', 'N/A')} semitones
- Maximum chord size: {features.get('max_chord_size', 'N/A')} notes
- Note density: {features.get('note_density', 'N/A'):.2f} notes per second
- Total duration: {features.get('duration', 'N/A')} quarter notes
- Total notes: {features.get('total_notes', 'N/A')}

**Known Practice Tips for {difficulty_category}**:
{chr(10).join('- ' + tip for tip in category_info['practice_tips'])}

**Technical Focus**: {category_info['technical_focus']}

**Similar Composers**: {', '.join(category_info['composers'])}
"""
    
    if piece_info:
        context += f"\n**Piece Information**: {piece_info.get('composer', 'Unknown')} - {piece_info.get('title', 'Unknown')}"
    
    # Create prompt for GPT-4o
    prompt = f"""{context}

Based on this analysis, provide personalized practice advice for this piece. Include:
1. Specific technical challenges to focus on
2. Practice strategies tailored to the extracted features
3. Progressive practice steps (beginner to advanced)
4. Common pitfalls to avoid

Keep the advice practical, encouraging, and specific to the piece's characteristics.
"""
    
    # Query GPT-4o
    gpt_response = query_gpt4o(prompt)
    
    # Structure the response
    advice = {
        'category': difficulty_category,
        'category_description': category_info['description'],
        'technical_focus': category_info['technical_focus'],
        'base_practice_tips': category_info['practice_tips'],
        'example_pieces': category_info['example_pieces'],
        'personalized_advice': gpt_response if gpt_response else "Unable to generate personalized advice (API error)",
        'features_summary': {
            'max_stretch': features.get('max_stretch'),
            'max_chord_size': features.get('max_chord_size'),
            'note_density': round(features.get('note_density', 0), 2)
        }
    }
    
    return advice


def generate_advice_fallback(difficulty_category, features):
    """
    Generate advice without GPT-4o (fallback mode).
    
    Args:
        difficulty_category (str): Predicted difficulty category
        features (dict): Extracted features
        
    Returns:
        dict: Basic advice dictionary
    """
    kb = load_knowledge_base()
    
    if difficulty_category not in kb:
        return {'error': f"Unknown category: {difficulty_category}"}
    
    category_info = kb[difficulty_category]
    
    return {
        'category': difficulty_category,
        'category_description': category_info['description'],
        'technical_focus': category_info['technical_focus'],
        'practice_tips': category_info['practice_tips'],
        'example_pieces': category_info['example_pieces'],
        'features_summary': {
            'max_stretch': features.get('max_stretch'),
            'max_chord_size': features.get('max_chord_size'),
            'note_density': round(features.get('note_density', 0), 2)
        },
        'note': 'Using fallback mode (no GPT-4o integration)'
    }


if __name__ == "__main__":
    # Test knowledge base loading
    kb = load_knowledge_base()
    print("Knowledge Base Categories:")
    for category in kb.keys():
        print(f"  - {category}")
