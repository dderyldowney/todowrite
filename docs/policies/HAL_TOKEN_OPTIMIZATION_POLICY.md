# HAL and Token Optimization Policy

**Status**: MANDATORY ACTIVE SYSTEM
**Version**: Current implementation with real-time monitoring
**Policy**: All agents MUST use HAL preprocessing before any work

## 🚨 HAL MANDATE (NON-OVERRIDABLE)

**HAL (Hierarchical Agent Layer) preprocessing is MANDATORY** for all Claude Code CLI sessions.

### System Components

#### HAL Token-Savvy Agent
- **Location**: `dev_tools/agent_controls/hale_token_savvy_agent.py`
- **Function**: Token/character gating before API calls
- **Features**:
  - Hard stop if over token budget
  - Delta-aware prompts (tiny "no changes" markers for unchanged content)
  - Small directive system prompts to save tokens
  - Local-filter-first processing

#### Token Optimization System
- **Core Engine**: `dev_tools/token_optimization/always_token_sage.py`
- **Location**: `dev_tools/token_optimization/` directory
- **Features**:
  - Automatic token reduction algorithms
  - Real-time token usage tracking
  - Adaptive optimization based on context
  - Performance monitoring and reporting

#### Real-Time Monitoring
- **Monitor**: `.claude/realtime_token_monitor.py`
- **Active Logs**: `.claude/hal_active.log`
- **Status Tracking**: `.claude/token_usage.log`, `.claude/hal_violations.log`

## 🔴 MANDATORY OPERATIONAL REQUIREMENTS

### Session Startup Requirements

**1. HAL MUST be initialized on every session start:**
```bash
# MANDATORY - No session can proceed without this
./.claude/startup.sh
```

**2. HAL preprocessing is mandatory (`HAL_PREPROCESSING_MANDATORY=true`):**
- All prompts must pass through HAL preprocessing
- Token budgets must be enforced before API calls
- Delta-aware optimization must be active

**3. Active monitoring must be running:**
```bash
# HAL must be continuously monitoring
ps -p $(cat .claude/hal_active.pid) > /dev/null
```

## 🚫 FORBIDDEN OPERATIONS

**NEVER ALLOWED:**
- ❌ Bypassing HAL preprocessing
- ❌ Disabling token optimization
- ❌ Continuing work when token budget is exceeded
- ❌ Ignoring HAL violation alerts
- ❌ Modifying HAL configuration without proper justification
- ❌ Running development sessions without HAL monitoring

### HAL Violation Types

**Critical Violations (Session Stop):**
- HAL not responding to token budget limits
- Continuous token waste detected
- HAL monitoring process failure
- Unauthorized HAL configuration changes

**Warning Violations (Alert & Correct):**
- High token usage patterns detected
- Inefficient delta processing
- Missing optimization opportunities

## 🔴 REQUIRED COMPLIANCE CHECKLIST

### Before Any Work
1. ✅ Verify HAL is running: `python .claude/realtime_token_monitor.py`
2. ✅ Check token budgets are set and active
3. ✅ Verify delta-aware processing is enabled
4. ✅ Confirm monitoring logs are being written
5. ✅ Validate no HAL violations in progress

### During Work
1. ✅ Monitor token usage in real-time
2. ✅ Ensure HAL preprocessing occurs before each operation
3. ✅ Track optimization effectiveness
4. ✅ Log any HAL violations immediately
5. ✅ Maintain active session continuity

### Agent Compliance
- **MUST read HAL policy** before starting work
- **MUST apply token optimization** principles
- **MUST report HAL violations** to session manager
- **MUST maintain token efficiency** throughout session

## 📊 PERFORMANCE REQUIREMENTS

### Token Reduction Targets
- **Minimum 50% token reduction** compared to baseline
- **Maximum 15% token budget** per operation
- **Delta-aware processing** for repetitive tasks
- **Adaptive optimization** based on context complexity

### Monitoring Requirements
- **Real-time token tracking** with <1s latency
- **Violation detection** with immediate alerting
- **Performance metrics** with daily reporting
- **Session continuity** with persistent state

### Integration Requirements
- **Database persistence** - All metrics stored in PostgreSQL
- **Session management** - Cross-session continuity maintained
- **Policy enforcement** - Integration with CLAUDE.md mandates

## 🔧 OPERATIONAL COMMANDS

### System Status Commands
```bash
# Check HAL status
python .claude/realtime_token_monitor.py

# Monitor token usage in real-time
tail -f .claude/hal_active.log

# Check recent violations
tail -20 .claude/hal_violations.log

# View token optimization statistics
python dev_tools/token_optimization/always_token_sage.py --stats
```

### HAL Control Commands
```bash
# Start HAL monitoring (if not running)
./.claude/hal_active_monitor.sh

# Stop HAL monitoring
./.claude/hal_shutdown.sh

# Force HAL optimization cycle
python .claude/hal_token_optimizer.py --optimize
```

### Integration Verification
```bash
# Verify HAL integration with policy enforcement
echo $HAL_PREPROCESSING_MANDATORY
python .claude/startup_enforcement.py | grep "HAL"
```

## 🎯 COMPLIANCE METRICS

### Success Indicators
- ✅ 100% of operations processed through HAL
- ✅ Token budgets enforced without violation
- ✅ Delta-aware processing active
- ✅ Real-time monitoring operational
- ✅ Zero critical HAL violations
- ✅ Session continuity maintained

### Failure Indicators
- ❌ Operations bypassing HAL preprocessing
- ❌ Token budget exceeded without enforcement
- ❌ HAL monitoring process failure
- ❌ Policy enforcement violations
- ❌ Session continuity broken

## 📋 INTEGRATION WITH OTHER POLICIES

### Required Policy Interactions
- **TDD Requirements**: Token optimization must not affect test coverage
- **PostgreSQL Architecture**: All metrics stored in PostgreSQL
- **Development Standards**: HAL integration must follow type hints and coding standards

### Policy Enforcement Dependencies
- **Startup Sequence Policy**: HAL initialization is required step
- **Production Safety**: HAL protects against token waste in production
- **Validation & Testing**: HAL optimization effectiveness must be validated

## 🔥 ENFORCEMENT ESCALATION

### Critical System Failures
1. **HAL Process Death**: Immediate session stop required
2. **Budget Violation**: Stop work and analyze token usage patterns
3. **Monitoring Failure**: Restart HAL monitoring immediately
4. **Policy Violation**: Session stop until compliance restored

### Violation Response Protocol
1. **STOP** all work immediately
2. **LOG** violation details to session manager
3. **ANALYZE** root cause of violation
4. **CORRECT** the underlying issue
5. **RESUME** work only after compliance verification

## 🚨 AGENT MANDATORY REQUIREMENTS

### Before Starting Work
- **Read this policy document completely**
- **Verify HAL is active** using status commands
- **Confirm token budgets** are appropriately set
- **Check monitoring logs** for recent activity

### During Operations
- **All prompts must pass through HAL** preprocessing
- **Token usage must be monitored** in real-time
- **Violations must be reported** immediately
- **Efficiency must be maintained** throughout session

### Compliance Verification
- **Session completion** requires HAL compliance check
- **Token savings** must meet minimum reduction targets
- **No critical violations** should be recorded
- **Monitoring continuity** must be maintained throughout

**HAL IS NOT OPTIONAL - IT IS THE MANDATORY ENFORCEMENT MECHANISM FOR ALL DEVELOPMENT WORK.**
