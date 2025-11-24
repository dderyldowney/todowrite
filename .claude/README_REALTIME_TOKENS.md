# Real-time Token Tracking and Statusline Updates

This document describes the real-time token tracking system that ensures your Claude Code statusline shows the most current token savings at all times.

## Overview

The real-time token tracking system provides:

- **Immediate Updates**: Token savings are tracked and displayed in real-time as they happen
- **Multiple Sources**: Tracks tokens from HAL preprocessing, token optimization, and manual activities
- **Detailed Logging**: Maintains comprehensive logs of all token optimization activities
- **Statusline Integration**: Seamlessly integrates with Claude Code's statusline display

## Components

### 1. Enhanced Statusline (`~/.claude/statusline.py`)

The main statusline script has been enhanced with:

- **Real-time Log Reading**: Reads from `realtime_tokens.log` for immediate updates
- **Multiple Log Sources**: Supports various token log formats and sources
- **Command Line Interface**: Provides commands for manual token tracking

#### Key Functions:

```python
# Get current token count with real-time updates
get_token_count()

# Log token savings immediately
log_realtime_tokens(tokens_saved, source)

# Command-line usage
python3 ~/.claude/statusline.py --log-realtime 150 "HAL_preprocessing"
```

### 2. Real-time Token Monitor (`.claude/realtime_token_monitor.py`)

A dedicated monitoring system that:

- **Tracks Activities**: Logs token optimization activities as they happen
- **Manages Logs**: Maintains organized log files for tracking and analysis
- **Provides Interface**: Command-line interface for monitoring and testing

#### Usage:

```bash
# Start monitoring
python3 .claude/realtime_token_monitor.py start

# Log an activity
python3 .claude/realtime_token_monitor.py log 100 "source" "context"

# Check current status
python3 .claude/realtime_token_monitor.py status

# Simulate activity for testing
python3 .claude/realtime_token_monitor.py simulate 50 "test_source"
```

### 3. HAL Integration

The HAL Agent System (`dev_tools/agent_controls/hal_token_savvy_agent.py`) has been updated to:

- **Calculate Savings**: Estimate token savings based on processing parameters
- **Log Immediately**: Update token counters in real-time
- **Provide Context**: Include detailed context for each optimization activity

#### Token Savings Calculation:

```python
# Base savings for HAL processing
estimated_savings = 100

# Additional savings based on parameters
if chars_processed:
    estimated_savings += min(200, chars_processed // 20)
if delta_mode:
    estimated_savings += 75
if complex_goal:
    estimated_savings += 100
```

### 4. Token Optimization Integration

The token optimization system (`dev_tools/token_optimization/always_token_sage.py`) now:

- **Tracks Activities**: Automatically logs all token optimization activities
- **Estimates Impact**: Calculates potential token savings from optimizations
- **Real-time Updates**: Immediately updates the statusline when optimizations occur

### 5. Startup Integration

The startup enforcement script automatically initializes real-time monitoring:

```python
# During startup
python3 .claude/realtime_token_monitor.py start
```

## Log Files

The system maintains several log files:

### 1. Real-time Tokens Log (`.claude/realtime_tokens.log`)

Format: `timestamp:tokens:source`

Example:
```
2025-11-24T10:30:15.123456:150:HAL_preprocessing
2025-11-24T10:31:22.456789:75:token_optimization
2025-11-24T10:32:05.789012:50:manual_entry
```

### 2. Token Activities Log (`.claude/token_activities.log`)

Format: `timestamp:tokens:source:context`

Example:
```
2025-11-24T10:30:15.123456:150:HAL_preprocessing:goal: analyze database models, chars: 3200
2025-11-24T10:31:22.456789:75:token_optimization:context optimization active
2025-11-24T10:32:05.789012:50:manual_entry:user added savings
```

### 3. Traditional Token Logs

The system continues to support existing token logs:
- `.claude/token_usage.log`
- `.claude/token_usage 2.log`

## Manual Usage

### Adding Token Savings

```bash
# Direct statusline update
python3 ~/.claude/statusline.py --add-savings 100 "manual"

# Real-time logging
python3 ~/.claude/statusline.py --log-realtime 100 "source" "context"

# Using the monitor
python3 .claude/realtime_token_monitor.py log 100 "source" "context"
```

### Checking Status

```bash
# Get current token count
python3 ~/.claude/statusline.py --get-tokens

# Show statusline preview
python3 ~/.claude/statusline.py

# Monitor status
python3 .claude/realtime_token_monitor.py status
```

### Testing

```bash
# Run comprehensive test suite
python3 .claude/test_realtime_tokens.py

# Test statusline functionality
python3 ~/.claude/statusline.py --test
```

## Integration Examples

### HAL Processing

When HAL processes a request:

1. **Preprocessing**: HAL analyzes the goal and filters repository content
2. **Savings Calculation**: Estimates tokens saved vs. full repository processing
3. **Real-time Logging**: Immediately logs the savings with context
4. **Statusline Update**: Statusline reflects the new total immediately

### Token Optimization

When token optimization occurs:

1. **Activity Detection**: System detects optimization activities
2. **Impact Assessment**: Calculates estimated token savings
3. **Immediate Logging**: Logs the activity in real-time
4. **Statusline Refresh**: Updates the displayed token count

### Manual Tracking

For manual token savings:

1. **User Input**: User manually logs savings via command line
2. **Validation**: System validates the input
3. **Logging**: Records the activity with source and context
4. **Update**: Immediately updates all tracking systems

## Configuration

### Environment Variables

No additional environment variables required. The system uses existing paths and configurations.

### Paths and Files

- **Statusline**: `~/.claude/statusline.py`
- **Monitor**: `.claude/realtime_token_monitor.py`
- **Token Monitor**: `.claude/token_monitoring.py`
- **Test Script**: `.claude/test_realtime_tokens.py`

### Log Locations

- **Real-time Log**: `.claude/realtime_tokens.log`
- **Activities Log**: `.claude/token_activities.log`
- **Traditional Logs**: `.claude/token_usage.log`, `.claude/token_usage 2.log`

## Troubleshooting

### Statusline Not Updating

1. **Check Monitor Status**:
   ```bash
   python3 .claude/realtime_token_monitor.py status
   ```

2. **Verify Log Files**:
   ```bash
   ls -la .claude/realtime_tokens.log .claude/token_activities.log
   ```

3. **Test Functionality**:
   ```bash
   python3 .claude/test_realtime_tokens.py
   ```

### Missing Token Updates

1. **Check HAL Integration**:
   ```bash
   python3 dev_tools/agent_controls/hal_token_savvy_agent.py --goal "test"
   ```

2. **Verify Token Optimization**:
   ```bash
   python3 dev_tools/token_optimization/always_token_sage.py "test goal"
   ```

3. **Manual Test**:
   ```bash
   python3 ~/.claude/statusline.py --log-realtime 100 "test" "manual test"
   ```

## Performance Considerations

- **Update Throttling**: Statusline updates are throttled to prevent overwhelming the system
- **Log Rotation**: Consider implementing log rotation for long-term usage
- **Memory Usage**: The system maintains minimal in-memory state for efficiency

## Future Enhancements

Potential improvements:

1. **Web Dashboard**: Real-time web interface for token tracking
2. **Historical Analysis**: Tools for analyzing token savings over time
3. **Integration Alerts**: Notifications for significant token savings milestones
4. **Automated Reports**: Periodic reports on token optimization effectiveness

## Security and Privacy

- **Local Storage**: All logs are stored locally on your machine
- **No External Data**: No token data is sent to external services
- **User Control**: Full control over what gets logged and tracked

---

This real-time token tracking system ensures that your Claude Code statusline always reflects the most current token savings, providing immediate feedback on the effectiveness of your token optimization activities.
