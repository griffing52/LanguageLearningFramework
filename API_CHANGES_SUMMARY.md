# Word and Phrase Upload API Fix - Changes Summary

All changes ensure the API aligns with the data file structure specification in [docs/data-files.md](docs/data-files.md).

## Overview of Fixes

The word and phrase upload/creation API now correctly follows the data file structure specification with proper initialization values and format handling.

---

## 1. Data Format Alignment

### Seed File Format (User-Facing)
Files use **equals-separated format** with optional markers:
- `word=translation` - regular word
- `*word=translation` - known word (pre-learned)
- `!word=translation` - important word (prioritized)
- `phrase text=translation` - phrases

### Storage Format
Seed files are stored in equals format. When items are loaded, they're converted to domain models with appropriate defaults.

### Memory File Format
The memory file supports multiple formats:
1. **Line-based format** (primary, as per data-files.md):
   ```
   <num_items>
   <item_value>
   <item_translation>
   <item_frequency>
   <item_age>
   <item_dependency_count>
   ...
   <dep_indices>
   ```
2. **JSON format** (legacy support)
3. **Simple key|value format** (legacy support)

---

## 2. Changes to DataLoader (`apps/api/data_access/loader.py`)

### `load_words()`
**Before:** Parsed pipe-separated format: `value|translation|complexity|frequency|age`

**After:** 
- Parses equals-separated format: `word=translation` with optional markers
- Handles special markers:
  - `*word=translation` → marked as known: `complexity=1, frequency=1, age=100`
  - `!word=translation` → marked as important: `complexity=2, frequency=0, age=0`
  - Regular word → `complexity=1, frequency=0, age=0`
- All words start at `frequency=0` until they are studied
- Complexity is simple (1) for regular words, slightly higher (2) for important words
- Age tracks how many other items have been taught since this word was last studied

### `load_phrases()`
**Before:** Parsed pipe-separated format with redundant complexity parsing

**After:**
- Parses equals-separated format: `phrase=translation`
- New phrases default to: `complexity=1, frequency=0, age=0`
- Correctly identifies phrase dependencies based on contained words
- Supports complexity customization for important or multi-word phrases

### `load_memory()`
**Before:** Only supported JSON and simple key|value format

**After:**
- Now supports line-based structured format (primary format from data-files.md)
- Parses phrase records with: value, translation, frequency, age, dependency_count
- Falls back to JSON and simple key|value formats for backward compatibility
- Correctly extracts frequency information from all supported formats

---

## 3. Changes to PlatformService (`apps/api/services/platform_service.py`)

### `add_word()`
**Before:** Stored in pipe format: `value|translation|complexity|frequency|age`

**After:**
- Stores in equals format: `value=translation`
- Uses default initialization: `complexity=1, frequency=0, age=0`
- Format matches seed files for consistency

### `add_phrase()`
**Before:** Stored in pipe format

**After:**
- Stores in equals format: `value=translation`
- Uses default initialization: `complexity=1, frequency=0, age=0`
- Format matches seed files for consistency

### `_normalize_vocab_lines()`
**Before:** Parsed only pipe format, converted everything to pipe format

**After:**
- **Input:** Accepts both equals format (primary) and pipe format (legacy)
- **Output:** Stores in equals format for consistency with seed files
- **Marker Handling:** Preserves `*` and `!` markers from input to output
- **Synonyms/Spellings:** Comma-separated spellings map to one word object; the last spelling is canonical
- Examples:
  - Input: `hello=hallo` → Output: `hello=hallo`
  - Input: `*hello=hallo` → Output: `*hello=hallo`
  - Input: `!important=wichtig` → Output: `!important=wichtig`
  - Input: `hello|hallo|1|0|0` → Output: `hello=hallo`
  - Input: `goh,gah=to go` → Canonical value used by API: `gah`

---

## 4. Model Initialization Verification (`apps/api/core/models.py`)

The `CreateWordRequest` and `CreatePhraseRequest` models already have correct defaults:

```python
class CreateWordRequest(BaseModel):
    value: str = Field(...)
    translation: str = Field(...)
    complexity: int = Field(default=1, ge=1)        # ✓ Correct
    frequency: int = Field(default=0, ge=0)          # ✓ Correct  
    age: int = Field(default=0, ge=0)                # ✓ Correct

class CreatePhraseRequest(BaseModel):
    value: str = Field(...)
    translation: str = Field(...)
    complexity: int = Field(default=1, ge=1)        # ✓ Correct
    frequency: int = Field(default=0, ge=0)          # ✓ Correct
    age: int = Field(default=0, ge=0)                # ✓ Correct
```

These defaults ensure that:
- Words/phrases start with **zero frequency** until they are studied
- Complexity is simple (1) by default
- Age starts at 0 and increments as other items are taught

---

## 5. Behavior Summary

### For New Words (via API)
```
POST /api/platform/words
{
  "value": "hello",
  "translation": "hallo"
}

Will store as: hello=hallo
Will load as: WordDTO(value="hello", translation="hallo", complexity=1, frequency=0, age=0)
```

### For Known Words (in seed file)
```
*hello=hallo

Will load as: WordDTO(value="hello", translation="hallo", complexity=1, frequency=1, age=100)
Indicates this word is already known and has been around for a long time
```

### For Important Words (in seed file)
```
!hello=hallo

Will load as: WordDTO(value="hello", translation="hallo", complexity=2, frequency=0, age=0)
Indicates this word is important and should be prioritized in learning
```

### For Phrases
```
ich bi neui da=i am new here

Will load as: PhraseDTO(
  value="ich bi neui da",
  translation="i am new here",
  complexity=1,
  frequency=0,
  age=0,
  words=["ich", "bi", "neui", "da"]  # extracted from phrase
)
```

---

## 6. Age Field Semantics

As clarified in your request:
- **Age** represents how many other words and phrases have been taught **since the last time this item was taught**
- Starts at 0 for new items
- Increments with each teaching session of other items
- Purpose: Identify items that need refreshing (high age = not recently studied)
- Known words are marked with high age (100) to indicate they're established

---

## 7. Frequency Field Semantics

- **Words:** Start at `frequency=0` when first added
- Only increments when the word is successfully studied/answered correctly
- **Known words** (`*prefix`): May start with `frequency=1` to indicate they've been pre-learned
- **Memory file:** Persists frequency values between sessions

---

## 8. Complexity Field Semantics

- **Words:** Simple (1) by default, since complexity is more about phrase structure
- Regular words: `complexity=1`
- Important words (`!prefix`): `complexity=2` (higher priority in teaching)
- **Phrases:** Complexity determined by structure and importance, not word count
- Reflects teaching difficulty, not just word/phrase length

---

## Testing the Changes

To test the fixed API:

### 1. Upload words file with markers:
```
*hello=hallo
!important=wichtig
water=wasser
```

### 2. Upload phrases:
```
ich bi da=i am here
du bisch da=you are here
```

### 3. Verify initialization:
- Regular items load with `frequency=0, age=0`
- Known items (`*`) load with marked state for quick review
- Important items (`!`) load with higher complexity for prioritization

---

## Backward Compatibility

The changes maintain backward compatibility:

1. **Pipe-separated import files** are still accepted and converted to equals format
2. **Existing memory files** in JSON or key|value format are still loaded correctly
3. **API continues to accept** both legacy fields in requests (they're just stored in simplified format)

---

## Files Modified

1. [apps/api/data_access/loader.py](apps/api/data_access/loader.py) - Data parsing logic
2. [apps/api/services/platform_service.py](apps/api/services/platform_service.py) - File writing and normalization
