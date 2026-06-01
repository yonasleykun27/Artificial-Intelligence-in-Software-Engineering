# AI: Preemptive Bug Fixing

## Objective
Apply a structured AI prompt to review a vulnerable C function, identify 
logical and memory safety flaws, and generate the corrected fix.

## Files
| File | Description |
|------|-------------|
| `initial_code.c` | Original vulnerable C function |
| `fixed_code.c` | Corrected C function after AI code review |

## AI Tool Used
ChatGPT with a structured Senior C Developer role prompt.

## Flaws Identified
1. **Logical Error**: Loop traverses past last node to NULL, so 
   `current = new_node` only changes a local variable — list is never linked.
2. **Memory Flaw**: No NULL check after `malloc()` — if allocation fails, 
   dereferencing causes a Segmentation Fault.

## Fix Summary
- Changed `while (current)` to `while (current->next)`
- Changed `current = new_node` to `current->next = new_node`
- Added `if (!new_node) return (NULL);` after malloc
