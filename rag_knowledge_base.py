"""
Dronacharya's knowledge base: Curated food safety passages.
Small, single-idea chunks for better retrieval.
"""

SAFETY_KNOWLEDGE_BASE = [
    {
        "id": "kb_001",
        "title": "Hot holding temperature limits",
        "text": "Cooked foods must be held at 57°C (135°F) or higher to prevent bacterial growth. Do not hold below this temperature.",
    },
    {
        "id": "kb_002",
        "title": "Cold holding temperature limits",
        "text": "Potentially hazardous foods must be held at 5°C (41°F) or lower when cold-holding. Check regularly for proper temperature maintenance.",
    },
    {
        "id": "kb_003",
        "title": "Time-temperature for cooked meat",
        "text": "Cooked poultry and meat dishes: Safe for hot-holding for maximum 3 hours at 60°C or above. Discard if exceeded.",
    },
    {
        "id": "kb_004",
        "title": "Time-temperature for cooked vegetables and starch",
        "text": "Cooked vegetables and starch-based dishes: Safe for hot-holding for up to 4 hours at 57°C or above.",
    },
    {
        "id": "kb_005",
        "title": "Cooked rice safety",
        "text": "Cooked rice can develop spores if held improperly. Must be cooled rapidly to 21°C within 1 hour, or discarded if held warm for more than 4 hours.",
    },
    {
        "id": "kb_006",
        "title": "Dairy product holding",
        "text": "Dairy-based foods and desserts: Maximum 2-hour holding at 5°C. Any exceeding this window presents significant safety risk.",
    },
    {
        "id": "kb_007",
        "title": "Packaged and shelf-stable foods",
        "text": "Packaged, unopened foods can be held at room temperature (20°C) for extended periods if packaging is intact. Discard if opened and held >2 hours at room temp.",
    },
    {
        "id": "kb_008",
        "title": "Allergen considerations",
        "text": "Always disclose presence of common allergens: peanuts, tree nuts, milk, eggs, fish, shellfish, soy, wheat. Recipient must confirm acceptability.",
    },
    {
        "id": "kb_009",
        "title": "Visual inspection for safety",
        "text": "Reject food that shows signs of mold, unusual odor, discoloration, or pests. When in doubt, discard.",
    },
    {
        "id": "kb_010",
        "title": "Cross-contamination risk",
        "text": "Raw and cooked foods must never be in direct contact. Ensure cooked food redistributed has not been exposed to raw food.",
    },
    {
        "id": "kb_011",
        "title": "Vegetarian vs non-vegetarian food handling",
        "text": "Some recipients accept only vegetarian food. Always verify dietary restrictions before assigning recipient.",
    },
    {
        "id": "kb_012",
        "title": "Reheating guidelines",
        "text": "If food will be reheated, it must reach 74°C (165°F) throughout. Inform recipient of proper reheating procedure.",
    },
    {
        "id": "kb_013",
        "title": "Rapid cooling procedures",
        "text": "For emergency cooling: submerge container in ice bath or use blast chiller. Cool from 60°C to 21°C within 1 hour maximum.",
    },
    {
        "id": "kb_014",
        "title": "Transportation safety",
        "text": "Transport hot food in insulated containers to maintain 57°C. Transport cold food in coolers with ice. Total transport time should not exceed 30 minutes.",
    },
    {
        "id": "kb_015",
        "title": "Recipient training requirement",
        "text": "Recipient organization must have trained food handlers on staff. Verify before assignment to ensure safe final handling.",
    },
]


def build_knowledge_base_index():
    """Return indexed knowledge base for FAISS embedding."""
    return SAFETY_KNOWLEDGE_BASE


def retrieve_passages(query: str, k: int = 3) -> list:
    """
    Simple keyword-based retrieval (mock FAISS).
    In production, use sentence-transformers + FAISS for semantic search.
    """
    keywords = query.lower().split()
    scores = []
    
    for passage in SAFETY_KNOWLEDGE_BASE:
        title_lower = passage["title"].lower()
        text_lower = passage["text"].lower()
        
        # Count keyword matches
        matches = sum(1 for kw in keywords if kw in title_lower or kw in text_lower)
        scores.append((passage, matches))
    
    # Sort by match count, return top k
    scores.sort(key=lambda x: x[1], reverse=True)
    return [p[0] for p in scores[:k]]


if __name__ == "__main__":
    # Test retrieval
    results = retrieve_passages("cooked meat temperature holding")
    print("Retrieved passages:")
    for r in results:
        print(f"  - {r['id']}: {r['title']}")
