"""
SignBridge - Dictionary Tests
================================
Tests for the ASL dictionary module.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dictionary import (
    lookup, get_all_signs, get_sign_categories,
    get_character_for_label, is_dynamic_sign,
    get_dynamic_letter_note, ASL_DICTIONARY
)


class TestLookup:
    """Test dictionary lookup functionality."""

    def test_lookup_valid_letter(self):
        """Test looking up a valid letter."""
        result = lookup('A')
        assert result['letter'] == 'A'
        assert result['meaning'] == 'The letter A'
        assert 'description' in result

    def test_lookup_all_letters(self):
        """Test that all 26 letters are in the dictionary."""
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            result = lookup(letter)
            assert result['letter'] == letter
            assert 'meaning' in result

    def test_lookup_special_signs(self):
        """Test special signs: del, nothing, space."""
        for sign in ['del', 'nothing', 'space']:
            result = lookup(sign)
            assert result['letter'] == sign
            assert 'meaning' in result

    def test_lookup_case_insensitive(self):
        """Test case-insensitive lookup."""
        result_upper = lookup('A')
        result_lower = lookup('a')
        assert result_upper['letter'] == result_lower['letter']

    def test_lookup_unknown_label(self):
        """Test looking up an unknown label."""
        result = lookup('UNKNOWN_SIGN')
        assert 'Unknown' in result['meaning']

    def test_lookup_empty_string(self):
        """Test looking up an empty string."""
        result = lookup('')
        assert 'Unknown' in result['meaning']

    def test_lookup_with_whitespace(self):
        """Test looking up a label with whitespace."""
        result = lookup('  A  ')
        assert result['letter'] == 'A'

    def test_lookup_returns_copy(self):
        """Test that lookup returns a copy, not a reference."""
        result1 = lookup('A')
        result2 = lookup('A')
        result1['meaning'] = 'modified'
        assert result2['meaning'] != 'modified'


class TestDictionary:
    """Test dictionary data integrity."""

    def test_dictionary_has_29_entries(self):
        """Test that the dictionary has all 29 ASL classes."""
        assert len(ASL_DICTIONARY) == 29

    def test_all_entries_have_required_keys(self):
        """Test that all entries have required keys."""
        required_keys = ['letter', 'meaning', 'description']
        for key, value in ASL_DICTIONARY.items():
            for req_key in required_keys:
                assert req_key in value, f"Missing '{req_key}' in entry '{key}'"

    def test_get_all_signs(self):
        """Test getting all signs."""
        signs = get_all_signs()
        assert len(signs) == 29
        assert 'A' in signs
        assert 'del' in signs


class TestSignCategories:
    """Test sign categorization."""

    def test_categories_complete(self):
        """Test that all categories are present."""
        categories = get_sign_categories()
        assert 'letters' in categories
        assert 'special' in categories
        assert 'dynamic' in categories

    def test_special_signs(self):
        """Test special sign categorization."""
        categories = get_sign_categories()
        special = categories['special']
        assert 'del' in special
        assert 'nothing' in special
        assert 'space' in special

    def test_dynamic_signs(self):
        """Test dynamic sign categorization."""
        categories = get_sign_categories()
        dynamic = categories['dynamic']
        assert 'J' in dynamic
        assert 'Z' in dynamic


class TestCharacterForLabel:
    """Test character conversion for text composition."""

    def test_letter_returns_uppercase(self):
        assert get_character_for_label('A') == 'A'
        assert get_character_for_label('z') == 'Z'

    def test_space_returns_space(self):
        assert get_character_for_label('space') == ' '

    def test_del_returns_none(self):
        assert get_character_for_label('del') is None

    def test_nothing_returns_empty(self):
        assert get_character_for_label('nothing') == ''


class TestDynamicSigns:
    """Test dynamic sign detection."""

    def test_j_is_dynamic(self):
        assert is_dynamic_sign('J') is True

    def test_z_is_dynamic(self):
        assert is_dynamic_sign('Z') is True

    def test_a_is_not_dynamic(self):
        assert is_dynamic_sign('A') is False

    def test_dynamic_note_exists(self):
        note = get_dynamic_letter_note()
        assert isinstance(note, str)
        assert len(note) > 0
        assert 'J' in note or 'motion' in note.lower()
