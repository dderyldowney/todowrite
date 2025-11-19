# ToDoWrite Documentation Hub

**🌐 Live Documentation**: [https://todowrite.davidderyldowney.com](https://todowrite.davidderyldowney.com)

---

## 📚 Browse Documentation by Package

### 🔧 Core Library (`lib/`)
Comprehensive documentation for the todowrite Python library.

- **📖 Overview** → [`lib/README.md`](lib/README.md)
- **📋 User Guides** → [`lib/guides/`](lib/guides/)
- **💡 Examples** → [`lib/examples/`](lib/examples/)
- **🔗 API Reference** → [Library API Docs](https://todowrite.davidderyldowney.com/library/todowrite.html)

### ⚡ CLI Interface (`cli/`)
Command-line interface documentation and usage guides.

- **📖 Overview** → [`cli/README.md`](cli/README.md)
- **🚀 Installation** → [`cli/installation/`](cli/installation/)
- **🔧 Shell Integration** → [`cli/ZSH_INTEGRATION.md`](cli/ZSH_INTEGRATION.md)

### 🌐 Web Application (`web_package/`)
Web application documentation (planning stage).

- **📖 Package** → [`../web_package/README.md`](../web_package/README.md) *(planning stage)*

## 🛠️ Shared Resources

### 👥 Development & Contributing
Resources for developers and contributors.

- **🛠️ Development Guide** → [`shared/development/README.md`](shared/development/README.md)
- **🏗️ Build System** → [`BUILD_SYSTEM.md`](BUILD_SYSTEM.md)
- **⚡ Development Workflow** → [`DEVELOPMENT_WORKFLOW.md`](DEVELOPMENT_WORKFLOW.md)
- **🤝 Contributing** → [`shared/contributing/README.md`](shared/contributing/README.md)
- **📋 Branch Workflow** → [`BRANCH_WORKFLOW.md`](BRANCH_WORKFLOW.md)

### 🚀 Release Process
Release and deployment documentation.

- **📋 Release Guide** → [`shared/release/README.md`](shared/release/README.md)
- **🔧 Release Workflow** → [`RELEASE_WORKFLOW.md`](RELEASE_WORKFLOW.md)
- **📦 PyPI Guide** → [`PyPI_HOWTO.md`](PyPI_HOWTO.md)
- **📝 Version Management** → [`VERSION_MANAGEMENT.md`](VERSION_MANAGEMENT.md)

### 🏗️ Project Architecture
Core architecture and design documentation.

- **🎯 ToDoWrite Models** → [`ToDoWrite.md`](ToDoWrite.md) - SQLAlchemy-based architecture
- **🗄️ Database Architecture** → [`UNIVERSAL_DATABASE_ARCHITECTURE.md`](UNIVERSAL_DATABASE_ARCHITECTURE.md)
- **📋 API Documentation** → [`API_DOCUMENTATION.md`](API_DOCUMENTATION.md)
- **📊 Monorepo Structure** → [`MONOREPO_STRUCTURE.md`](MONOREPO_STRUCTURE.md)

### 🔧 Development Tools
Development utilities and automation.

- **🛠️ Project Utilities** → [`PROJECT_UTILITIES.md`](PROJECT_UTILITIES.md)
- **📋 Schema Usage** → [`SCHEMA_USAGE.md`](SCHEMA_USAGE.md)
- **🔄 Schema Migration** → [`SCHEMA_MIGRATION_GUIDE.md`](SCHEMA_MIGRATION_GUIDE.md)
- **📈 Status Tracking** → [`STATUS_TRACKING.md`](STATUS_TRACKING.md)

### 📚 Archive
Historical and superseded documentation.

- **📜 Archive** → [`shared/archive/`](shared/archive/)

## 🌟 Generated Documentation

### 📖 Professional HTML Documentation
Auto-generated API documentation with search, navigation, and cross-references.

- **🔗 Live Site**: [https://todowrite.davidderyldowney.com](https://todowrite.davidderyldowney.com)
- **🔧 Build locally**: `./dev_tools/build.sh docs`
- **📂 Generated in**: [`sphinx/build/html/`](sphinx/build/html/)
- **📚 Direct API Reference**: [Library API Documentation](sphinx/build/html/library/todowrite.html)

### 🔍 What's Included in Generated Docs
- **📚 Complete API Reference** - All SQLAlchemy models, functions, and methods
- **🔗 Cross-References** - Clickable links between components
- **🔍 Full-Text Search** - Search across all documentation
- **📱 Mobile-Friendly** - Responsive design
- **⚡ Fast Navigation** - Professional Read the Docs theme

## 🚀 Quick Start

### For Users
```bash
# Install todowrite CLI and library
pip install todowrite todowrite-cli

# Initialize a project
todowrite init

# Create your first goal
todowrite create --layer goal --title "My First Goal" --description "Getting started with ToDoWrite"

# View all items
todowrite list

# View project statistics
todowrite stats
```

### For Developers
```bash
# Clone repository
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Setup development environment
source .venv/bin/activate  # Activate virtual environment
./dev_tools/build.sh install

# Build documentation
./dev_tools/build.sh docs

# Run tests
./dev_tools/build.sh test

# Full development workflow
./dev_tools/build.sh dev
```

### Python API Usage
```python
from todowrite.core.models import Goal, Task
from todowrite.core.schema_validator import initialize_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Initialize database
initialize_database("sqlite:///myproject.db")

# Create session
engine = create_engine("sqlite:///myproject.db")
Session = sessionmaker(bind=engine)
session = Session()

# Create items
goal = Goal(title="Launch Product", owner="product-team", status="planned")
task = Task(title="Design UI", owner="design-team", progress=25)

session.add(goal)
session.add(task)
session.commit()

print(f"Created goal with ID: {goal.id}")
print(f"Created task with ID: {task.id}")
```

## 📋 Documentation Standards

This project follows strict documentation standards:

- **✅ TDD Methodology** - All features documented via tests
- **✅ No Mocking** - Real implementations only
- **✅ Current Content** - Documentation kept current with development
- **✅ Clear Structure** - Organized by package and purpose
- **✅ Professional Output** - Industry-standard documentation generation
- **✅ SQLAlchemy Models** - All examples use current ToDoWrite Models API
- **✅ Working CLI** - Command examples reflect actual working commands

## 🎯 Current Project Status

### ✅ Completed Features
- **SQLAlchemy-based Models**: 12-layer hierarchy with proper relationships
- **Modern CLI**: Integer IDs, Rich tables, comprehensive commands
- **Database Support**: SQLite and PostgreSQL with auto-migrations
- **Professional Documentation**: Sphinx-generated HTML docs
- **Build System**: Automated testing, linting, and deployment
- **Schema Validation**: JSON schema validation and type safety

### 🔄 Architecture
- **12-Layer Hierarchy**: Goals → Concepts → Contexts → Constraints → Requirements → AcceptanceCriteria → InterfaceContracts → Phases → Steps → Tasks → SubTasks → Commands
- **SQLAlchemy ORM**: Modern database patterns with proper relationships
- **Auto-generated Integer IDs**: No more string-based ID management
- **Many-to-Many Associations**: Proper join tables for complex relationships

### 📦 Available Packages
- **`todowrite`**: Core Python library (v0.4.1)
- **`todowrite-cli`**: Command-line interface (v0.4.1)
- **`web_package`**: Web application (planning stage)

---

**Last Updated**: 2025-11-19
**Status**: ✅ Production Ready
**Architecture**: SQLAlchemy-based ToDoWrite Models
**CLI**: ✅ Modern with Integer IDs and Rich Output
**Documentation**: ✅ Professional Sphinx-Generated HTML
**Generated with**: Sphinx + Read the Docs Theme
