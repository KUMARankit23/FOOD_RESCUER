"""
Prompt Variants Testing Framework
Multiple prompt variants for comparative evaluation:
- ReAct (Reasoning + Acting)
- Few-shot learning
- Persona-based
- Zero-shot Chain-of-Thought
- Constraint-based
"""

import json
from typing import Dict, List, Any, Optional, Literal
from datetime import datetime
from enum import Enum
from enhanced_schemas import PromptVariant, AgentPrompt


class PromptTemplate:
    """Base prompt template"""
    
    def __init__(self, name: str, variant: PromptVariant, system_prompt: str):
        self.name = name
        self.variant = variant
        self.system_prompt = system_prompt
        self.examples: List[Dict[str, str]] = []
    
    def add_example(self, input_text: str, output_text: str):
        """Add a few-shot example"""
        self.examples.append({
            "input": input_text,
            "output": output_text
        })
    
    def get_full_prompt(self, user_input: str) -> str:
        """Get complete prompt with examples"""
        prompt = self.system_prompt
        
        if self.examples:
            prompt += "\n\nExamples:\n"
            for i, example in enumerate(self.examples, 1):
                prompt += f"\nExample {i}:\nInput: {example['input']}\nOutput: {example['output']}"
        
        prompt += f"\n\nNow process:\n{user_input}"
        return prompt
    
    def to_schema(self) -> AgentPrompt:
        """Convert to schema"""
        return AgentPrompt(
            agent_id="sample_agent",
            variant=self.variant,
            system_prompt=self.system_prompt,
            examples=self.examples
        )


class ReActPromptTemplate(PromptTemplate):
    """ReAct (Reasoning + Acting) prompt template"""
    
    def __init__(self):
        super().__init__(
            "ReAct Template",
            PromptVariant.REACT,
            """You are an agent using ReAct (Reasoning + Acting) approach.

Process:
1. THOUGHT: Think about the task step by step
2. ACTION: Decide what action to take
3. OBSERVATION: Observe the result
4. THOUGHT: Reflect on the observation
5. ACTION: Take next action if needed
... repeat until complete

Always show your reasoning clearly."""
        )


class FewShotPromptTemplate(PromptTemplate):
    """Few-shot learning prompt template"""
    
    def __init__(self):
        super().__init__(
            "Few-Shot Template",
            PromptVariant.FEWSHOT,
            """You are an agent that learns from examples.

Learn from these examples and follow the same pattern for new inputs."""
        )


class PersonaPromptTemplate(PromptTemplate):
    """Persona-based prompt template"""
    
    def __init__(self, persona: str, role: str, traits: str):
        system_text = f"""You are {persona}, a {role}.

Your characteristics:
{traits}

Make decisions based on your persona and expertise."""
        
        super().__init__(
            f"Persona: {persona}",
            PromptVariant.PERSONA,
            system_text
        )
        self.persona = persona
        self.role = role


class ZeroShotCoTPromptTemplate(PromptTemplate):
    """Zero-shot Chain-of-Thought prompt template"""
    
    def __init__(self):
        super().__init__(
            "Zero-Shot CoT Template",
            PromptVariant.ZEROSHOTCOT,
            """You are an agent that solves problems through step-by-step reasoning.

IMPORTANT: Let's think step by step.

Process any input by:
1. Breaking it into components
2. Analyzing each component
3. Considering implications
4. Drawing conclusions

Always explain your reasoning."""
        )


class ConstraintPromptTemplate(PromptTemplate):
    """Constraint-based prompt template"""
    
    def __init__(self, constraints: List[str]):
        constraint_text = "\n".join(f"- {c}" for c in constraints)
        system_text = f"""You are an agent that must satisfy strict constraints.

CONSTRAINTS (MUST follow):
{constraint_text}

Never violate these constraints. If a task violates them, reject it."""
        
        super().__init__(
            "Constraint Template",
            PromptVariant.CONSTRAINT,
            system_text
        )
        self.constraints = constraints


class EklavyaVariants:
    """Prompt variants for Eklavya (Intake Agent)"""
    
    @staticmethod
    def get_react_variant() -> PromptTemplate:
        """ReAct variant for validation"""
        template = ReActPromptTemplate()
        template.system_prompt = """You are Eklavya, the intake validation agent using ReAct.

THOUGHT: Consider what validation checks are needed
ACTION: Validate each field
OBSERVATION: Check if validation passed
THOUGHT: Identify any issues
ACTION: Flag problems if found

Be thorough - flag ALL issues."""
        
        template.add_example(
            "Report: biryani, 60 portions, 58°C, Hostel, 20:00",
            "THOUGHT: Check food_type, quantity, temperature, location, deadline\nACTION: Validate each field\nOBSERVATION: All valid\nRESULT: Valid report"
        )
        
        template.add_example(
            "Report: ?, -5 portions, 100°C, ?, ?",
            "THOUGHT: Check all fields\nACTION: Validate\nOBSERVATION: Multiple issues found\nRESULT: Invalid - missing food_type, invalid quantity, invalid temperature, missing location, missing deadline"
        )
        
        return template
    
    @staticmethod
    def get_fewshot_variant() -> PromptTemplate:
        """Few-shot variant"""
        template = FewShotPromptTemplate()
        template.system_prompt = """You are Eklavya, the intake validation agent.

Learn from examples to validate reports."""
        
        template.add_example(
            "VALID: food_type=biryani, quantity=60, temp=58, location=Hostel, deadline=20:00",
            "Status: VALID - All fields present and reasonable"
        )
        
        template.add_example(
            "INVALID: food_type=, quantity=-5, temp=100, location=, deadline=",
            "Status: INVALID - Issues: Missing food_type, Invalid quantity (<0), Invalid temperature (>90), Missing location, Missing deadline"
        )
        
        template.add_example(
            "NEEDS_FIX: food_type=rice, quantity=30, temp=55.5 (below 57°C), location=Cafeteria, deadline=22:00",
            "Status: NEEDS_FIX - Issue: Temperature below safe minimum (57°C)"
        )
        
        return template
    
    @staticmethod
    def get_constraint_variant() -> PromptTemplate:
        """Constraint variant"""
        constraints = [
            "quantity must be > 0",
            "temperature must be between -10 and 90°C",
            "location must be valid",
            "all required fields must be present"
        ]
        return ConstraintPromptTemplate(constraints)


class ArjunaVariants:
    """Prompt variants for Arjuna (Matching Agent)"""
    
    @staticmethod
    def get_react_variant() -> PromptTemplate:
        """ReAct variant for matching"""
        template = ReActPromptTemplate()
        template.system_prompt = """You are Arjuna, the matching specialist using ReAct.

THOUGHT: Understand matching criteria
ACTION: Query recipients by food preference
OBSERVATION: Get candidate list
ACTION: Calculate distances
OBSERVATION: Get distance matrix
ACTION: Score each match
OBSERVATION: Get scores
RESULT: Return top 3 ranked matches"""
        
        template.add_example(
            "Find recipients for: 60 portions biryani at Hostel",
            "THOUGHT: Need recipients who take cooked_veg\nACTION: Query database\nOBSERVATION: Found 5 recipients\nACTION: Calculate distances\nOBSERVATION: Distances calculated\nACTION: Score by distance+capacity\nRESULT: [r1: 85pts, r2: 72pts, r3: 60pts]"
        )
        
        return template
    
    @staticmethod
    def get_fewshot_variant() -> PromptTemplate:
        """Few-shot variant"""
        template = FewShotPromptTemplate()
        template.system_prompt = """You are Arjuna, the matching specialist.

Score recipients based on distance and capacity."""
        
        template.add_example(
            "Food: biryani (60 portions), Candidates: r1(2.4km, cap=100), r2(5.1km, cap=150), r3(7.8km, cap=80)",
            "Scores: r1=85(best distance & good capacity), r2=72(far but large), r3=60(far & small). RANK: [r1, r2, r3]"
        )
        
        return template


class DronacharyyaVariants:
    """Prompt variants for Dronacharya (Safety Agent)"""
    
    @staticmethod
    def get_strict_persona() -> PromptTemplate:
        """Strict safety-first persona"""
        template = PersonaPromptTemplate(
            "Dronacharya the Guardian",
            "safety keeper",
            """- Strict: When in doubt, mark UNSAFE
- Evidence-based: Must cite RAG passages
- Risk-averse: Prioritize safety over convenience
- Thorough: Check all criteria"""
        )
        template.system_prompt = """You are Dronacharya, the strict safety keeper.

STRICT MODE: Safety first, always.
- Temperature violations = UNSAFE
- Missing evidence = UNSAFE
- Any doubt = Flag as conditional/unsafe

MUST cite RAG evidence for every verdict."""
        
        return template
    
    @staticmethod
    def get_flexible_persona() -> PromptTemplate:
        """Flexible but evidence-based"""
        template = PersonaPromptTemplate(
            "Dronacharya the Evaluator",
            "nuanced safety expert",
            """- Flexible: Use evidence to make nuanced calls
- Evidence-based: Always cite sources
- Balanced: Consider context
- Transparent: Explain reasoning"""
        )
        template.system_prompt = """You are Dronacharya, the nuanced evaluator.

FLEXIBLE MODE: Use evidence wisely.
- SAFE: All checks pass with good margins
- UNSAFE: Clear violations with evidence
- CONDITIONAL: Minor concerns, acceptable with warnings

Always cite RAG evidence."""
        
        return template
    
    @staticmethod
    def get_constraint_variant() -> PromptTemplate:
        """Hard constraints"""
        constraints = [
            "cooked_veg: temperature >= 57°C",
            "rice: <= 4 hours since prep",
            "meat: temperature >= 65°C",
            "MUST cite RAG evidence for verdict"
        ]
        return ConstraintPromptTemplate(constraints)


class ChanakyaVariants:
    """Prompt variants for Chanakya (Logistics Agent)"""
    
    @staticmethod
    def get_manager_persona() -> PromptTemplate:
        """Manager perspective"""
        template = PersonaPromptTemplate(
            "Chanakya the Manager",
            "logistics coordinator",
            """- Organized: Follow decision sequence
- Pragmatic: Consider all constraints
- Decisive: Make clear calls
- Coordinating: Integrate all inputs"""
        )
        template.system_prompt = """You are Chanakya, the logistics manager.

MANAGER MODE: Coordinate all constraints.

Decision sequence:
1. Is food valid? (from Eklavya)
2. Are recipients available? (from Arjuna)
3. Is food safe? (from Dronacharya)
4. Can logistics work? (time, distance)

Make final call considering ALL factors."""
        
        template.add_example(
            "Valid: YES, Safe: YES, Recipients: 3 found, Logistics: OK",
            "DECISION: DISPATCH - All checks pass. Dispatch to closest recipient."
        )
        
        template.add_example(
            "Valid: NO, Safe: UNKNOWN, Recipients: NONE, Logistics: N/A",
            "DECISION: NO_PICKUP - Food validation failed. Cannot proceed."
        )
        
        return template
    
    @staticmethod
    def get_strategist_persona() -> PromptTemplate:
        """Strategist perspective"""
        template = PersonaPromptTemplate(
            "Chanakya the Strategist",
            "impact optimizer",
            """- Strategic: Optimize for impact
- Efficient: Minimize waste
- Informed: Consider recipient needs
- Balanced: Speed vs perfection"""
        )
        template.system_prompt = """You are Chanakya, the strategist.

STRATEGIST MODE: Optimize impact.

Strategic goals:
1. Maximize food redistribution
2. Minimize waste
3. Consider recipient needs
4. Balance speed and quality

Make decisions that maximize overall impact."""
        
        return template


class PromptVariantsFramework:
    """Framework for managing and testing prompt variants"""
    
    def __init__(self):
        self.variants: Dict[str, Dict[str, PromptTemplate]] = {
            "eklavya": {
                "react": EklavyaVariants.get_react_variant(),
                "fewshot": EklavyaVariants.get_fewshot_variant(),
                "constraint": EklavyaVariants.get_constraint_variant()
            },
            "arjuna": {
                "react": ArjunaVariants.get_react_variant(),
                "fewshot": ArjunaVariants.get_fewshot_variant()
            },
            "dronacharya": {
                "strict": DronacharyyaVariants.get_strict_persona(),
                "flexible": DronacharyyaVariants.get_flexible_persona(),
                "constraint": DronacharyyaVariants.get_constraint_variant()
            },
            "chanakya": {
                "manager": ChanakyaVariants.get_manager_persona(),
                "strategist": ChanakyaVariants.get_strategist_persona()
            }
        }
        self.execution_results: List[Dict[str, Any]] = []
    
    def get_variant(self, agent: str, variant_name: str) -> Optional[PromptTemplate]:
        """Get a specific variant"""
        return self.variants.get(agent, {}).get(variant_name)
    
    def get_all_variants_for_agent(self, agent: str) -> Dict[str, PromptTemplate]:
        """Get all variants for an agent"""
        return self.variants.get(agent, {})
    
    def list_agents(self) -> List[str]:
        """List agents with variants"""
        return list(self.variants.keys())
    
    def list_variants_for_agent(self, agent: str) -> List[str]:
        """List variant names for an agent"""
        return list(self.variants.get(agent, {}).keys())
    
    def get_variant_comparison(self, agent: str) -> Dict[str, Any]:
        """Get comparison of all variants for an agent"""
        variants = self.get_all_variants_for_agent(agent)
        
        comparison = {
            "agent": agent,
            "variants": {}
        }
        
        for var_name, template in variants.items():
            comparison["variants"][var_name] = {
                "name": template.name,
                "type": template.variant.value,
                "examples": len(template.examples),
                "system_prompt_length": len(template.system_prompt)
            }
        
        return comparison
    
    def record_result(self, agent: str, variant: str, result: Dict[str, Any]):
        """Record execution result"""
        self.execution_results.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "variant": variant,
            "result": result
        })
    
    def get_results_for_variant(self, agent: str, variant: str) -> List[Dict]:
        """Get results for a specific variant"""
        return [
            r for r in self.execution_results
            if r["agent"] == agent and r["variant"] == variant
        ]
    
    def print_all_variants(self):
        """Print all available variants"""
        print("\n" + "=" * 70)
        print("AVAILABLE PROMPT VARIANTS")
        print("=" * 70)
        
        for agent in self.list_agents():
            print(f"\n{agent.upper()}:")
            for variant in self.list_variants_for_agent(agent):
                template = self.get_variant(agent, variant)
                print(f"  - {variant} ({template.variant.value})")
                if template.examples:
                    print(f"      Examples: {len(template.examples)}")


# Global framework
variants_framework = PromptVariantsFramework()


if __name__ == "__main__":
    # Demo
    print("=" * 70)
    print("PROMPT VARIANTS FRAMEWORK DEMO")
    print("=" * 70)
    
    # Show all variants
    variants_framework.print_all_variants()
    
    # Show specific variant
    print("\n[1] Eklavya ReAct Variant:")
    variant = variants_framework.get_variant("eklavya", "react")
    print(f"Type: {variant.variant.value}")
    print(f"System Prompt:\n{variant.system_prompt}")
    
    # Get full prompt
    print("\n[2] Full Prompt Example:")
    full_prompt = variant.get_full_prompt("Validate: biryani, 60, 58°C, Hostel, 20:00")
    print(full_prompt[:500] + "...")
    
    # Show variants comparison
    print("\n[3] Eklavya Variants Comparison:")
    comparison = variants_framework.get_variant_comparison("eklavya")
    for var, details in comparison["variants"].items():
        print(f"  {var}: {details['type']} (examples: {details['examples']})")
    
    print("\n✓ Prompt variants framework ready for evaluation")
