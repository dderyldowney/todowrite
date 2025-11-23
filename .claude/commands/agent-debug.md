# Agent Debug Command

Systematic debugging and root cause analysis using industry-standard debugging methodologies.

## Usage
/agent-debug "describe the bug or issue you're experiencing"

## Examples
/agent-debug "API returns 500 error when uploading files larger than 1MB"
/agent-debug "Memory usage spikes when processing large datasets"
/agent-debug "Database deadlock in concurrent transactions"

## Features
- **Root Cause Analysis**: Systematic approach to identify underlying issues
- **Hypothesis Testing**: Scientific method for debugging
- **Log Analysis**: Techniques for effective log parsing and analysis
- **Performance Profiling**: CPU, memory, and I/O bottleneck identification
- **Error Pattern Recognition**: Common bug patterns and solutions

## Debugging Methodology
1. **Reproduce the Issue**: Create reproducible test cases
2. **Gather Evidence**: Collect logs, metrics, and system state
3. **Form Hypotheses**: List potential root causes
4. **Test Hypotheses**: Systematic elimination of possibilities
5. **Verify Fix**: Ensure resolution doesn't introduce regressions

## Example Output
```
🔍 Debug Analysis: API returns 500 error when uploading files larger than 1MB

## Issue Reproduction
✅ Reproducible with files >1MB
✅ Works fine with files <1MB
✅ Error occurs after 30-second timeout

## Evidence Collection
- HTTP Status: 500 Internal Server Error
- Error Logs: "Request timeout exceeded"
- Network: Upload progress stops at ~870KB
- Server: Memory usage stable

## Hypotheses (Ranked by Probability)
1. **Most Likely**: Request timeout configured to 30 seconds
   - Evidence: 1MB file takes ~45 seconds on current network
   - Test: Increase timeout to 60 seconds

2. **Possible**: Nginx/Gateway body size limit
   - Evidence: Error at ~870KB (close to common 1MB limits)
   - Test: Check nginx.conf client_max_body_size

3. **Unlikely**: Application memory limit
   - Evidence: Memory usage stable during upload
   - Test: Monitor heap usage during upload

## Action Plan
1. Check application timeout settings
2. Verify gateway configuration
3. Test with increased timeout value
4. Add progress logging for better visibility

## Estimated Fix Time: 2-4 hours
## Risk Level: Low (configuration change)
```
