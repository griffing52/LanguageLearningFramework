"""
Data loader for parsing and deserializing learned data files.
Bridges between C++ data format and Python domain models.
"""

from typing import Dict, List, Tuple, Set, Optional
from pathlib import Path
import json
from core.models import WordDTO, PhraseDTO
from utils.logger import get_logger

logger = get_logger(__name__)


class DataLoader:
    """Loads vocabulary and phrase data from seed files and memory files."""
    
    @staticmethod
    def load_words(file_path: Path) -> Dict[str, WordDTO]:
        """
        Load words from seed file.
        Format: word=translation or *word=translation or !word=translation (one per line)
        
        Prefixes:
        - * marks a known word (low complexity, aged)
        - ! marks an important word (higher complexity, prioritized)
        
        Args:
            file_path: Path to words.txt
        
        Returns:
            Dictionary mapping word value to WordDTO
        """
        words: Dict[str, WordDTO] = {}
        
        if not file_path.exists():
            logger.warning(f"Words file not found: {file_path}")
            return words
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Check for special markers
                    is_known = line.startswith('*')
                    is_important = line.startswith('!')
                    if is_known or is_important:
                        line = line[1:]  # Remove marker
                    
                    # Split on = to get value and translation
                    if '=' not in line:
                        logger.warning(f"Skipping malformed line {line_num}: {line}")
                        continue
                    
                    try:
                        value, translation = line.split('=', 1)
                        value = value.strip()
                        translation = translation.strip()
                        
                        if not value or not translation:
                            logger.warning(f"Skipping empty value/translation on line {line_num}")
                            continue
                        
                        # Determine complexity and initial state based on markers
                        # Word complexity is simple (1) by default
                        # * marker: known word - set low values, mark as studied
                        # ! marker: important word - higher complexity, mark as prioritized
                        if is_known:
                            complexity = 1  # Known words are simple
                            frequency = 1   # Mark as having been studied once
                            age = 100       # Mark as old/established
                        elif is_important:
                            complexity = 2  # Important words slightly more complex
                            frequency = 0   # Not yet studied
                            age = 0         # Starting fresh
                        else:
                            complexity = 1  # Regular words are simple
                            frequency = 0   # Start unlearned
                            age = 0         # Brand new
                        
                        word = WordDTO(
                            value=value,
                            translation=translation,
                            complexity=complexity,
                            frequency=frequency,
                            age=age
                        )
                        words[value] = word
                    
                    except (ValueError, IndexError) as e:
                        logger.warning(f"Error parsing line {line_num}: {line}. Error: {e}")
                        continue
            
            logger.info(f"Loaded {len(words)} words from {file_path}")
        
        except Exception as e:
            logger.error(f"Error loading words from {file_path}: {e}")
        
        return words
    
    @staticmethod
    def load_phrases(
        file_path: Path,
        words_map: Dict[str, WordDTO]
    ) -> Tuple[Dict[str, PhraseDTO], Dict[str, Set[str]]]:
        """
        Load phrases and compute dependencies.
        Format: phrase_value=translation (one per line)
        
        Args:
            file_path: Path to phrases file
            words_map: Dictionary of known words for dependency inference
        
        Returns:
            Tuple of (phrases dict, dependencies dict)
            dependencies maps phrase -> set of prerequisite phrase values
        """
        phrases: Dict[str, PhraseDTO] = {}
        phrase_words: Dict[str, Set[str]] = {}  # phrase_value -> set of word values
        dependencies: Dict[str, Set[str]] = {}
        
        if not file_path.exists():
            logger.warning(f"Phrases file not found: {file_path}")
            return phrases, dependencies
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    if not line or line.startswith('#'):
                        continue
                    
                    # Split on = to get value and translation
                    if '=' not in line:
                        logger.warning(f"Skipping malformed phrase line {line_num}: {line}")
                        continue
                    
                    try:
                        value, translation = line.split('=', 1)
                        value = value.strip()
                        translation = translation.strip()
                        
                        if not value or not translation:
                            logger.warning(f"Skipping empty phrase value/translation on line {line_num}")
                            continue
                        
                        # Extract words from phrase (simple split on spaces)
                        phrase_tokens = value.split()
                        phrase_word_set = set()
                        
                        for token in phrase_tokens:
                            clean_token = token.lower()
                            # Match against known words (case-insensitive)
                            matching_word = next(
                                (w for w in words_map.keys() if w.lower() == clean_token),
                                None
                            )
                            if matching_word:
                                phrase_word_set.add(matching_word)
                        
                        phrase_words[value] = phrase_word_set
                        
                        # Phrases start with 0 frequency and 0 age when first created
                        complexity = 1  # Default complexity
                        frequency = 0   # Start unlearned
                        age = 0         # Brand new
                        
                        phrase = PhraseDTO(
                            value=value,
                            translation=translation,
                            complexity=complexity,
                            frequency=frequency,
                            age=age,
                            words=list(phrase_word_set)
                        )
                        phrases[value] = phrase
                        dependencies[value] = set()
                    
                    except (ValueError, IndexError) as e:
                        logger.warning(f"Error parsing phrase line {line_num}: {line}. Error: {e}")
                        continue
            
            # Infer dependencies: phrase A depends on phrase B if all words of A are in B
            for phrase_a, words_a in phrase_words.items():
                for phrase_b, words_b in phrase_words.items():
                    if phrase_a != phrase_b and words_a.issubset(words_b):
                        dependencies[phrase_a].add(phrase_b)
            
            # Add dependencies to DTOs
            for phrase_value, deps in dependencies.items():
                if phrase_value in phrases:
                    phrases[phrase_value].dependencies = list(deps)
            
            logger.info(f"Loaded {len(phrases)} phrases from {file_path}")
        
        except Exception as e:
            logger.error(f"Error loading phrases from {file_path}: {e}")
        
        return phrases, dependencies
    
    @staticmethod
    def load_memory(file_path: Path) -> Dict[str, int]:
        """
        Load memory state (frequency and age updates for known items).
        
        Supports two formats:
        1. Line-based format (as per data-files.md):
           <num_phrases>
           <phrase_value>
           <phrase_translation>
           <phrase_frequency>
           <phrase_age>
           <phrase_dependency_count>
           ... (repeat for each item)
           <dep_indices...>
        
        2. Legacy JSON/key-value format:
           {"item_value": frequency, ...}
           OR
           item_value|frequency
        
        Args:
            file_path: Path to memory file
        
        Returns:
            Dictionary mapping item values to updated frequency (for backward compatibility)
        """
        memory: Dict[str, int] = {}
        
        if not file_path.exists():
            logger.debug(f"Memory file not found: {file_path}")
            return memory
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                return memory
            
            lines = content.split('\n')
            
            # Check if it's JSON format
            if content.startswith('{'):
                memory = json.loads(content)
                logger.info(f"Loaded memory state (JSON format): {len(memory)} items")
                return memory
            
            # Try line-based format
            if lines and lines[0].isdigit():
                # This appears to be the structured line-based format
                try:
                    num_items = int(lines[0])
                    line_idx = 1
                    
                    # Parse item records
                    for _ in range(num_items):
                        if line_idx + 4 >= len(lines):
                            break
                        
                        value = lines[line_idx].strip()
                        # translation = lines[line_idx + 1].strip()  # Not needed for memory dict
                        frequency = int(lines[line_idx + 2].strip())
                        # age = int(lines[line_idx + 3].strip())  # Not needed for memory dict
                        # dep_count = int(lines[line_idx + 4].strip())  # Dependencies handled separately
                        
                        if value:
                            memory[value] = frequency
                        
                        line_idx += 5
                    
                    logger.info(f"Loaded memory state (line-based format): {len(memory)} items")
                    return memory
                
                except (ValueError, IndexError) as e:
                    logger.warning(f"Failed to parse structured line format: {e}. Trying simple format.")
            
            # Fall back to simple line format: value|frequency
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split('|')
                if len(parts) >= 2:
                    try:
                        memory[parts[0]] = int(parts[1])
                    except ValueError:
                        logger.warning(f"Invalid frequency value in memory: {line}")
            
            logger.info(f"Loaded memory state (simple format): {len(memory)} items")
        
        except Exception as e:
            logger.error(f"Error loading memory from {file_path}: {e}")
        
        return memory
