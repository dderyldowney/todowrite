# ⚠️ CRITICAL: SYSTEM SEPARATION MANDATE

## **TWO COMPLETELY SEPARATE SYSTEMS - NEVER MIX**

### 🚫 **FORBIDDEN: ANY CROSS-SYSTEM DATA POLLUTION**
- **NEVER** store session data in ToDoWrite model tables
- **NEVER** store ToDoWrite model data in sessions tables
- **NEVER** mix `session_id` with ToDoWrite `metadata`
- **NEVER** use sessions tables for ToDoWrite hierarchical data
- **NEVER** use ToDoWrite tables for session tracking

---

## 🏗️ **SYSTEM 1: TODOWRITE MODELS API**

**Purpose**: Hierarchical project planning and task management
**Tables**: `goals`, `concepts`, `contexts`, `constraints`, `requirements`, `acceptance_criteria`, `interface_contracts`, `phases`, `steps`, `tasks`, `sub_tasks`, `commands`, `labels`

### **✅ ALLOWED in ToDoWrite Tables:**
- **title**: Project/goal/task titles
- **description**: Detailed descriptions
- **status**: Project status values
- **priority**: Priority levels
- **metadata**: **ONLY** ToDoWrite model-specific data (NEVER session data)
- **tags**: Project tags and labels
- **owner**: Project ownership
- **severity**: Issue severity levels

### **🚫 FORBIDDEN in ToDoWrite Tables:**
- **session_id**: **ABSOLUTELY FORBIDDEN**
- **actions**: Session tracking data
- **context**: Session context
- **environment**: Session environment
- **last_activity**: Session timestamps

### **Correct Usage Example:**
```python
# ✅ CORRECT: Clean ToDoWrite data
cursor.execute(
    "INSERT INTO goals (title, description) VALUES (%s, %s) RETURNING id",
    (title, description)
)

# ❌ FORBIDDEN: Never do this!
cursor.execute(
    "INSERT INTO goals (title, description, metadata) VALUES (%s, %s, %s)",
    (title, description, json.dumps({"session_id": session_id}))  # FORBIDDEN!
)
```

---

## 📋 **SYSTEM 2: SESSIONS TRACKING**

**Purpose**: Cross-session continuity, audit trail, and conversation state
**Tables**: `sessions` ONLY

### **✅ ALLOWED in Sessions Tables:**
- **session_id**: Unique session identifiers
- **title**: Session descriptive titles
- **description**: Session purpose
- **actions**: JSON array of all actions performed
- **context**: Session context and state
- **environment**: Environment configuration
- **current_focus_id**: Current active item
- **last_activity**: Session activity timestamps
- **conversations**: Conversation history

### **Correct Usage Example:**
```python
# ✅ CORRECT: Session tracking in dedicated table
actions_json = json.dumps([{
    "type": "create_goal",
    "layer": "goal",
    "title": title,
    "goal_id": goal_id,
    "timestamp": datetime.now().isoformat()
}])

cursor.execute(
    "INSERT INTO sessions (session_id, title, actions) VALUES (%s, %s, %s)",
    (session_id, f"Created Goal: {title}", actions_json)
)
```

---

## 🔥 **ENFORCEMENT RULES**

### **For All AI Agents (Chat, CLI, VSCode):**
1. **ALWAYS** use ToDoWrite models API for hierarchical data
2. **ALWAYS** use sessions table for session tracking
3. **NEVER** mix the two systems
4. **NEVER** store session_id in ToDoWrite metadata
5. **ALWAYS** keep metadata clean of session data

### **For Database Operations:**
- ToDoWrite tables get: `title`, `description`, clean `metadata`
- Sessions table gets: `session_id`, `actions`, `context`
- **NEVER CROSS-REFERENCE**

### **For Code Reviews:**
- **IMMEDIATELY REJECT** any code mixing systems
- **IMMEDIATELY FLAG** session_id in ToDoWrite tables
- **IMMEDIATELY REQUIRE** separation fixes

---

## 🛡️ **SAFE PATTERNS**

### **Pattern 1: Clean Separation**
```python
# ToDoWrite system - pure model data
goal_id = create_goal(title, description)  # Clean

# Sessions system - tracking only
track_session_action(session_id, "create_goal", goal_id)  # Separate
```

### **Pattern 2: Query Separation**
```python
# Get ToDoWrite data
goals = "SELECT title, description FROM goals"

# Get session data
sessions = "SELECT session_id, actions FROM sessions"
```

---

## 🚨 **VIOLATION CONSEQUENCES**

Any agent, code, or human that violates this separation will:
1. **IMMEDIATELY CORRUPT** both systems
2. **DESTROY** project data integrity
3. **BREAK** cross-session functionality
4. **REQUIRE** complete data cleanup
5. **BLOCK** further development until fixed

---

## ✅ **VERIFICATION CHECKLIST**

Before committing any code:
- [ ] No session_id in ToDoWrite tables
- [ ] No ToDoWrite model data in sessions
- [ ] Clean metadata columns in ToDoWrite
- [ ] Proper session tracking in sessions table only
- [ ] Zero cross-system pollution

---

**🔒 THIS SEPARATION IS NON-NEGOTIABLE AND ABSOLUTE**
**🔒 VIOLATIONS WILL BE IMMEDIATELY REJECTED**
**🔒 ALL AGENTS MUST ENFORCE THIS SEPARATION**