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
        Format: value|translation|complexity|frequency|age (one per line)
        
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
                    
                    parts = line.split('|')
                    if len(parts) < 2:
                        logger.warning(f"Skipping malformed line {line_num}: {line}")
                        continue
                    
                    try:
                        value = parts[0].strip()
                        translation = parts[1].strip()
                        complexity = int(parts[2]) if len(parts) > 2 else 1
                        frequency = int(parts[3]) if len(parts) > 3 else 0
                        age = int(parts[4]) if len(parts) > 4 else 0
                        
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
        Format: phrase_value|translation|complexity (one per line)
        
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
                    
                    parts = line.split('|')
                    if len(parts) < 2:
                        logger.warning(f"Skipping malformed phrase line {line_num}: {line}")
                        continue
                    
                    try:
                        value = parts[0].strip()
                        translation = parts[1].strip()
                        complexity = int(parts[2]) if len(parts) > 2 else 1
                        frequency = int(parts[3]) if len(parts) > 3 else 0
                        age = int(parts[4]) if len(parts) > 4 else 0
                        
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
        Load memory state (frequency updates for known items).
        Format: JSON or simple key|value mapping
        
        Args:
            file_path: Path to memory file
        
        Returns:
            Dictionary mapping item values to updated frequency
        """
        memory: Dict[str, int] = {}
        
        if not file_path.exists():
            logger.debug(f"Memory file not found: {file_path}")
            return memory
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content.startswith('{'):
                    # Try JSON format
                    memory = json.loads(content)
                else:
                    # Simple line format: value|frequency
                    for line in content.split('\n'):
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        parts = line.split('|')
                        if len(parts) >= 2:
                            try:
                                memory[parts[0]] = int(parts[1])
                            except ValueError:
                                logger.warning(f"Invalid frequency value in memory: {line}")
            
            logger.info(f"Loaded memory state: {len(memory)} items")
        
        except Exception as e:
            logger.error(f"Error loading memory from {file_path}: {e}")
        
        return memory
