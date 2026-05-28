from __future__ import annotations

from app.services.vector_service import VectorService


async def generate_and_index_mutations(prompt: str, category: str = "adversarial_mutation") -> int:
    """Async task entrypoint for generating adversarial variants and storing vectors."""

    return await VectorService().index_mutations(prompt, category)

