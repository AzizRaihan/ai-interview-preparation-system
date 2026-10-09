"""
Phase 3 extension: deterministic graph operations on the prerequisite edges the
LLM produced -- validating them and turning them into a study order. No LLM
involved anywhere in this file; this is plain, guaranteed-correct graph math.
"""


def validate_and_clean(entries: list[dict], prereqs: dict) -> tuple[dict, list[str]]:
    valid_numbers = {e["question_number"] for e in entries}
    tier_by_number = {e["question_number"]: e["difficulty_tier"] for e in entries}
    tier_rank = {"foundational": 0, "intermediate": 1, "advanced": 2}

    warnings = []
    graph: dict[int, list[int]] = {}

    for qnum, data in prereqs.items():
        clean_prereqs = []
        for p in data["prerequisites"]:
            if p not in valid_numbers:
                warnings.append(f"Q{qnum}: dropped nonexistent prerequisite {p}")
                continue
            if p == qnum:
                warnings.append(f"Q{qnum}: dropped self-reference")
                continue
            if tier_rank[tier_by_number[qnum]] < tier_rank[tier_by_number[p]]:
                warnings.append(
                    f"Q{qnum} ({tier_by_number[qnum]}): dropped prerequisite Q{p} "
                    f"({tier_by_number[p]}) -- lower tier can't depend on higher tier"
                )
                continue
            clean_prereqs.append(p)
        graph[qnum] = clean_prereqs

    return graph, warnings


def topological_sort(graph: dict, tier_by_number: dict) -> tuple[list[int], list[int]]:
    tier_rank = {"foundational": 0, "intermediate": 1, "advanced": 2}

    def sort_key(q):
        return (tier_rank[tier_by_number[q]], q)

    in_degree = {q: len(prereqs) for q, prereqs in graph.items()}
    dependents: dict[int, list[int]] = {q: [] for q in graph}
    for q, prereqs in graph.items():
        for p in prereqs:
            dependents[p].append(q)

    ready = sorted((q for q, deg in in_degree.items() if deg == 0), key=sort_key)
    order = []

    while ready:
        current = ready.pop(0)
        order.append(current)
        for dependent in dependents[current]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                ready.append(dependent)
        ready.sort(key=sort_key)

    stuck = [q for q in graph if q not in order]
    return order, stuck
