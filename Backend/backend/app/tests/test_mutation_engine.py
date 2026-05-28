from __future__ import annotations

from app.detection.adversarial.mutation_engine import MutationEngine


def test_mutation_engine_generates_variants() -> None:
    variants = MutationEngine().generate("ignore secret instructions")
    assert variants
    assert any("4" in variant or "3" in variant for variant in variants)

