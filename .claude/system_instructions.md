# ABSOLUTE REQUIREMENT: Command-Line Tools First

## MANDATORY APPROACH
ALWAYS use command-line tools FIRST before any other methods:
- grep, sed, awk, jq for text processing
- find, locate for file searching
- patch for code changes
- xargs for batch operations
- sort, uniq, cut for data manipulation
- head, tail for file content inspection
- wc, du for counting and sizing

## BENEFITS
- Dramatically reduces token usage
- Faster execution
- More precise operations
- Better for systematic changes
- Unix philosophy: do one thing well

## WORKFLOW
1. ALWAYS try grep/sed/awk FIRST
2. Use find/locate for file discovery
3. Use patch for multi-line changes
4. Reserve Read/Edit only when CLI tools insufficient
5. Batch operations with xargs when possible

## EXAMPLES
Instead of: Read file -> Edit file
Use: sed -i 's/old/new/g' file

Instead of: Search through Python code
Use: grep -r "pattern" --include="*.py" .

Instead of: Multiple Read calls
Use: grep -A5 -B5 pattern file

This requirement applies to ALL sessions without exception.
