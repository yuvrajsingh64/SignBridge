"""
SignBridge - ASL Dictionary Module
===================================
Maps ASL labels to English meanings and provides lookup functionality.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ASL_CLASSES, DYNAMIC_LETTERS, DYNAMIC_LETTER_NOTE


# ASL Alphabet dictionary mapping labels to their English meanings
ASL_DICTIONARY = {
    'A': {'letter': 'A', 'meaning': 'The letter A', 'description': 'Closed fist with thumb resting on the side.'},
    'B': {'letter': 'B', 'meaning': 'The letter B', 'description': 'Open hand with fingers together pointing up, thumb tucked across palm.'},
    'C': {'letter': 'C', 'meaning': 'The letter C', 'description': 'Curved hand forming the shape of the letter C.'},
    'D': {'letter': 'D', 'meaning': 'The letter D', 'description': 'Index finger pointing up, other fingers and thumb forming a circle.'},
    'E': {'letter': 'E', 'meaning': 'The letter E', 'description': 'Fingers curled down, thumb tucked under fingers.'},
    'F': {'letter': 'F', 'meaning': 'The letter F', 'description': 'Thumb and index finger form a circle, other fingers spread upward.'},
    'G': {'letter': 'G', 'meaning': 'The letter G', 'description': 'Index finger and thumb pointing sideways, parallel to each other.'},
    'H': {'letter': 'H', 'meaning': 'The letter H', 'description': 'Index and middle fingers extended sideways together.'},
    'I': {'letter': 'I', 'meaning': 'The letter I', 'description': 'Pinky finger extended upward, all other fingers closed.'},
    'J': {'letter': 'J', 'meaning': 'The letter J', 'description': 'Pinky finger extended, then traced in a J motion. (Dynamic sign — static image only)', 'is_dynamic': True},
    'K': {'letter': 'K', 'meaning': 'The letter K', 'description': 'Index and middle fingers in a V pointing up, thumb between them.'},
    'L': {'letter': 'L', 'meaning': 'The letter L', 'description': 'Thumb and index finger extended forming an L shape.'},
    'M': {'letter': 'M', 'meaning': 'The letter M', 'description': 'Three fingers folded over thumb.'},
    'N': {'letter': 'N', 'meaning': 'The letter N', 'description': 'Two fingers folded over thumb.'},
    'O': {'letter': 'O', 'meaning': 'The letter O', 'description': 'All fingers curved to touch thumb, forming an O shape.'},
    'P': {'letter': 'P', 'meaning': 'The letter P', 'description': 'Similar to K but pointing downward.'},
    'Q': {'letter': 'Q', 'meaning': 'The letter Q', 'description': 'Similar to G but pointing downward.'},
    'R': {'letter': 'R', 'meaning': 'The letter R', 'description': 'Index and middle fingers crossed.'},
    'S': {'letter': 'S', 'meaning': 'The letter S', 'description': 'Closed fist with thumb over fingers.'},
    'T': {'letter': 'T', 'meaning': 'The letter T', 'description': 'Thumb tucked between index and middle fingers.'},
    'U': {'letter': 'U', 'meaning': 'The letter U', 'description': 'Index and middle fingers extended upward together.'},
    'V': {'letter': 'V', 'meaning': 'The letter V', 'description': 'Index and middle fingers spread apart in a V shape.'},
    'W': {'letter': 'W', 'meaning': 'The letter W', 'description': 'Index, middle, and ring fingers spread apart.'},
    'X': {'letter': 'X', 'meaning': 'The letter X', 'description': 'Index finger hooked/bent.'},
    'Y': {'letter': 'Y', 'meaning': 'The letter Y', 'description': 'Thumb and pinky extended, other fingers closed.'},
    'Z': {'letter': 'Z', 'meaning': 'The letter Z', 'description': 'Index finger traces a Z shape in the air. (Dynamic sign — static image only)', 'is_dynamic': True},
    'del': {'letter': 'del', 'meaning': 'Delete', 'description': 'Special gesture indicating deletion of the last character.'},
    'nothing': {'letter': 'nothing', 'meaning': 'Nothing / No sign detected', 'description': 'No recognizable sign is being shown.'},
    'space': {'letter': 'space', 'meaning': 'Space', 'description': 'Gesture indicating a space between words.'},
}


def lookup(label):
    """
    Look up an ASL label in the dictionary.
    
    Args:
        label: The predicted label string (e.g., 'A', 'del', 'space')
    
    Returns:
        dict with keys: letter, meaning, description, is_dynamic (optional)
        Returns a default entry if label is not found.
    """
    label = str(label).strip()
    
    if label in ASL_DICTIONARY:
        return ASL_DICTIONARY[label].copy()
    
    # Case-insensitive fallback
    for key, value in ASL_DICTIONARY.items():
        if key.lower() == label.lower():
            return value.copy()
    
    return {
        'letter': label,
        'meaning': f'Unknown sign: {label}',
        'description': 'This label was not found in the ASL dictionary.',
    }


def get_all_signs():
    """Return the complete dictionary of supported ASL signs."""
    return ASL_DICTIONARY.copy()


def get_sign_categories():
    """
    Return signs grouped by category.
    
    Returns:
        dict with keys: letters, special, dynamic
    """
    letters = {}
    special = {}
    dynamic = {}
    
    for key, value in ASL_DICTIONARY.items():
        if value.get('is_dynamic'):
            dynamic[key] = value
        elif key in ('del', 'nothing', 'space'):
            special[key] = value
        else:
            letters[key] = value
    
    return {
        'letters': letters,
        'special': special,
        'dynamic': dynamic,
    }


def get_character_for_label(label):
    """
    Convert an ASL label to the character to append to text.
    
    Returns:
        str: The character to add, or empty string for 'nothing'
              and None for 'del' (meaning delete last)
    """
    label = str(label).strip()
    
    if label == 'nothing':
        return ''
    elif label == 'space':
        return ' '
    elif label == 'del':
        return None  # Signal to delete last character
    elif len(label) == 1 and label.isalpha():
        return label.upper()
    else:
        return ''


def is_dynamic_sign(label):
    """Check if a label represents a dynamic (motion-based) sign."""
    return str(label).strip().upper() in DYNAMIC_LETTERS


def get_dynamic_letter_note():
    """Return the note about dynamic letters."""
    return DYNAMIC_LETTER_NOTE
