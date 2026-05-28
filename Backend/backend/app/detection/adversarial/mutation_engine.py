from __future__ import annotations

from app.detection.adversarial.leetspeak_mutator import leetspeak
from app.detection.adversarial.spacing_mutator import spacing_attack
from app.detection.adversarial.synonym_mutator import synonym_replace
from app.detection.adversarial.unicode_obfuscator import unicode_obfuscate


class MutationEngine:
    """Generate adversarial prompt variants for indexing and risk estimation."""

    def generate(self, prompt: str) -> list[str]:
        variants = {
            synonym_replace(prompt),
            leetspeak(prompt),
            unicode_obfuscate(prompt),
            spacing_attack(prompt[:120]),
        }
        return [variant for variant in variants if variant and variant != prompt]

