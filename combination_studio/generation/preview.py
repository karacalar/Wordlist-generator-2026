from itertools import islice
from .index_converter import index_to_combination
from .cartesian_generator import generate_fixed, generate_range, generate_product_from_sets
from .template_generator import template_to_position_sets
from ..models.enums import GenerationMode

def theoretical_total(settings) -> int:
    cs = settings.charset.build()
    m = settings.mode
    if m in (GenerationMode.FIXED, GenerationMode.PREFIX_SUFFIX):
        return (len(cs) ** settings.exact_length) * len(settings.prefixes or [""]) * len(settings.suffixes or [""])
    if m == GenerationMode.RANGE:
        return sum(len(cs) ** n for n in range(settings.min_length, settings.max_length + 1))
    if m == GenerationMode.PATTERN:
        total = 1
        for s in settings.position_sets: total *= len(s)
        return total
    if m == GenerationMode.TEMPLATE:
        total = 1
        for s in template_to_position_sets(settings.template, settings.custom_tokens): total *= len(s)
        return total
    if m == GenerationMode.COUNTER:
        from .counter_generator import counter_count
        return counter_count(settings.counter_start, settings.counter_end, settings.counter_step)
    return settings.random_count

def preview_values(settings, limit=100, around_index=None, final=False):
    limit = max(0, min(int(limit), 10000))
    if limit == 0: return []
    total = theoretical_total(settings)
    start = 0
    if final:
        start = max(0, total - limit)
    elif around_index is not None:
        start = max(0, int(around_index) - limit // 2)
    clone = settings
    old_start, old_end = clone.start_index, clone.end_index
    clone.start_index, clone.end_index = start, min(total - 1, start + limit - 1)
    from ..jobs.worker import iter_generated_values
    out = [value for _, value, _, _ in islice(iter_generated_values(clone), limit)]
    clone.start_index, clone.end_index = old_start, old_end
    return out
