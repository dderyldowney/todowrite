# ToDoWrite Documentation Hub

**🌐 Live Documentation**: [https://todowrite.davidderyldowney.com](https://todowrite.davidderyldowney.com)

---

## 📚 Browse Documentation by Package

### 🔧 Core Library (`library/`)
Comprehensive documentation for the todowrite Python library.

- **📖 Overview** → [`library/README.md`](library/README.md)
- **📋 User Guides** → [`library/guides/`](library/guides/)
- **💡 Examples** → [`library/examples/`](library/examples/)
- **🔗 API Reference** → [Library API Docs](https://todowrite.davidderyldowney.com/library/todowrite.html)

### ⚡ CLI Interface (`cli/`)
Command-line interface documentation and usage guides.

- **📖 Overview** → [`cli/README.md`](cli/README.md) *(coming soon)*
- **🚀 Installation** → [`cli/installation/`](cli/installation/)
- **💻 Commands** → [`cli/commands/`](cli/commands/) *(coming soon)*
- **🔧 Shell Integration** → [`cli/integration/`](cli/integration/)
- **🐛 Troubleshooting** → [`cli/troubleshooting/`](cli/troubleshooting/) *(coming soon)*

### 🌐 Web Application (`web/`)
Web application documentation (planning stage).

- **📖 Overview** → [`web/README.md`](web/README.md) *(coming soon)*
- **🔌 API** → [`web/api/`](web/api/) *(coming soon)*
- **🚀 Deployment** → [`web/deployment/`](web/deployment/) *(coming soon)*

## 🛠️ Shared Resources

### 👥 Development & Contributing
Resources for developers and contributors.

- **🛠️ Development Guide** → [`shared/development/README.md`](shared/development/README.md) *(coming soon)*
- **🏗️ Build System** → [`shared/development/BUILD_SYSTEM.md`](shared/development/BUILD_SYSTEM.md)
- **⚡ Development Workflow** → [`shared/development/DEVELOPMENT_WORKFLOW.md`](shared/development/DEVELOPMENT_WORKFLOW.md)
- **🤝 Contributing** → [`shared/contributing/README.md`](shared/contributing/README.md) *(coming soon)*

### 🚀 Release Process
Release and deployment documentation.

- **📋 Release Guide** → [`shared/release/README.md`](shared/release/README.md) *(coming soon)*
- **🔧 Release Workflow** → [`shared/release/RELEASE_WORKFLOW.md`](shared/release/RELEASE_WORKFLOW.md)
- **📦 PyPI Guide** → [`shared/release/PyPI_HOWTO.md`](shared/release/PyPI_HOWTO.md)
- **📝 Version Management** → [`shared/release/VERSION_MANAGEMENT.md`](shared/release/VERSION_MANAGEMENT.md)

### 📚 Archive
Historical and superseded documentation.

- **📜 Archive** → [`shared/archive/`](shared/archive/)

## 🌟 Generated Documentation

### 📖 Professional HTML Documentation
Auto-generated API documentation with search, navigation, and cross-references.

- **🔗 Live Site**: [https://todowrite.davilderyldowney.com](https://todowrite.davilderyldowney.com)
- **🔧 Build locally**: `./dev_tools/build.sh docs`
- **📂 Generated in**: [`sphinx/build/html/`](sphinx/build/html/)

### 🔍 What's Included in Generated Docs
- **📚 Complete API Reference** - All classes, functions, and methods
- **🔗 Cross-References** - Clickable links between components
- **🔍 Full-Text Search** - Search across all documentation
- **📱 Mobile-Friendly** - Responsive design
- **⚡ Fast Navigation** - Professional Read the Docs theme

## 🚀 Quick Start

### For Users
```bash
# Install todowrite
pip install todowrite-cli

# Initialize a project
todowrite init

# View documentation
open docs/sphinx/build/html/index.html
```

### For Developers
```bash
# Clone repository
git clone https://github.com/dderyldowney/todowrite.git
cd todowrite

# Setup development environment
./dev_tools/build.sh install

# Build documentation
./dev_tools/build.sh docs

# Run tests
./dev_tools/build.sh test
```

## 📋 Documentation Standards

This project follows strict documentation standards:

- **✅ TDD Methodology** - All features documented via tests
- **✅ No Mocking** - Real implementations only
- **✅ Current Content** - Documentation kept current with development
- **✅ Clear Structure** - Organized by package and purpose
- **✅ Professional Output** - Industry-standard documentation generation

---

**Last Updated**: 2025-11-17
**Status**: ✅ Production Ready
**Generated with**: Sphinx + Read the Docs Theme
