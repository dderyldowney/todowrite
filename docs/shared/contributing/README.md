# Contributing to ToDoWrite

**Guidelines for contributing to the ToDoWrite project with ActiveRecord-inspired architecture.**

---

## 🚀 Quick Start

### Development Setup
```bash
# Clone and setup
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite
./dev_tools/build.sh install

# Install todowrite library
cd lib_package && uv pip install -e . && cd ..
```

## 🏗️ Development Approach

### Architecture Understanding
ToDoWrite uses **Rails ActiveRecord-inspired architecture**:

- **Models** with relationships (`has_many`, `belongs_to`)
- **Migrations** for schema management
- **Query builder** for chainable queries
- **Validations** at model level
- **Callbacks** for lifecycle events

### Key Patterns

#### Model Development
```python
from todowrite.core.models import Node, has_many, belongs_to

class NewModel(Node):
    """Follow ActiveRecord patterns."""

    class Meta:
        table_name = "custom_table"
        layer = "CustomLayer"

    # Associations
    has_many("related_items")
    belongs_to("parent", optional=True)

    # Validations
    validates_presence_of(["title"])

    # Callbacks
    before_save :prepare_data
```

#### Testing
```python
# Follow TDD: RED → GREEN → REFACTOR
class TestNewModel:
    def test_model_creation(self):
        # Write failing test first (RED)
        model = NewModel.create(title="Test")
        assert model.title == "Test"  # GREEN after implementation
```

## 📋 Contribution Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/new-active-record-features
```

### 2. Development
```bash
# Follow TDD methodology
./dev_tools/build.sh dev

# Build documentation if needed
./dev_tools/build.sh docs
```

### 3. Testing Requirements
- ✅ **Real implementations only** (no mocking)
- ✅ **100% test pass rate**
- ✅ **Component and subsystem organization**
- ✅ **TDD Red-Green-Refactor**

### 4. Documentation
- Update relevant docs in `docs/` structure
- Update API documentation if adding models/methods
- Update development guides if changing architecture

### 5. Submit Pull Request
```bash
git add .
git commit -m "feat(models): add ActiveRecord-style model with associations"
git push origin feature/new-active-record-features
```

## 🔧 Development Standards

### Code Quality
```bash
# Automatic quality checks
./dev_tools/build.sh lint
./dev_tools/build.sh format
./dev_tools/build.sh audit
```

### Testing Standards
- **No mocking** - Use real database connections and implementations
- **Component tests** - Test integration between components
- **TDD workflow** - Write tests before implementation

### Documentation Standards
- **Keep current** - Update docs when changing functionality
- **Accurate** - Reflect current ActiveRecord architecture
- **Complete** - Include examples and usage patterns

## 📚 Resources

### Development Documentation
- [Development Guide](../development/README.md) - Complete development workflow
- [Build System](../development/BUILD_SYSTEM.md) - Build tools and automation
- [Architecture](../development/UNIVERSAL_DATABASE_ARCHITECTURE.md) - Database design

### Project Documentation
- [Main Documentation Hub](../../README.md) - Complete documentation overview
- [Library Documentation](../../library/README.md) - API documentation

### Standards
- [TODOWRITE_STANDARDS_NEEDED.md](../../TODOWRITE_STANDARDS_NEEDED.md) - Industry standards to implement
- [CLAUDE.md](../../.claude/CLAUDE.md) - Project rules and policies

---

**Last Updated**: 2025-11-17
**Architecture**: ActiveRecord-inspired
**Testing**: TDD Required
