# Database Investigation Protocol - MANDATORY

## **🚨 NEVER DELETE FIRST - INVESTIGATE THOROUGHLY**

### **Step 1: Database Existence Check**
```bash
docker exec todowrite-postgres psql -U todowrite_user -d postgres -c "\l" | grep todowrite
```

### **Step 2: Table Count Verification**
```bash
docker exec todowrite-postgres psql -U todowrite_user -d todowrite -c "\dt" | wc -l
```

### **Step 3: Schema Verification**
```bash
docker exec todowrite-postgres psql -U todowrite_user -d todowrite -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'"
```

### **Step 4: Specific Table Check**
```bash
docker exec todowrite-postgres psql -U todowrite_user -d todowrite -c "\d goals"
```

### **Step 5: Data Verification**
```bash
docker exec todowrite-postgres psql -U todowrite_user -d todowrite -c "SELECT COUNT(*) FROM goals"
```

## **🚫 DELETION IS LAST RESORT**

**Only delete if ALL of these fail:**
- Database doesn't exist
- Schema is completely corrupted
- Data is irretrievably damaged
- No recovery options available

## **✅ SUCCESS CRITERIA**

If database exists and tables present → **PROCEED WITH WORK**
If database/tables missing → **INVESTIGATE ROOT CAUSE**

## **🚨 MANDATE VIOLATION CONSEQUENCES**

**Deleting data without proper investigation = Project Time Loss**
**Not following investigation protocol = Mandate Violation**

---
**This protocol is loaded in every session to prevent data loss.**
