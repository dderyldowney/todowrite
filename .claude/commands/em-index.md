# Episodic Memory Index Command

Index conversation files from your Claude projects directory into PostgreSQL for fast searching.

## Usage
/em-index

## Features
- **Adaptive Processing**: Only indexes new or changed files
- **Resource-Aware**: Processes files in batches to prevent system bogging
- **Change Detection**: Uses SHA256 hashing to detect file modifications
- **Incremental Updates**: Fast re-indexing of recently modified conversations

## Example Output
```
📁 Indexing conversations from: /Users/dderyldowney/.claude/projects
🔄 Adaptive mode: Only processing new/changed files
⚙️  Batch size: 25 files
✅ Connected to PostgreSQL database
✅ Adaptive schema columns already exist
✅ Conversation schema created successfully
📊 Processed 50 files (+0 skipped), indexed 0 | Rate: 12.5 files/sec
✅ Completed: 0 conversations indexed from 50 files
📈 Skipped 50 unchanged files | Total time: 4.0s
✅ Successfully indexed 0 conversations
📊 Total: 6,686 conversations, 43,491 messages
🏗️  Projects: 15
```

## Notes
- First run may take several minutes to process all conversations
- Subsequent runs are much faster due to adaptive processing
- All data is stored in PostgreSQL for persistent access