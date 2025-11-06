#!/bin/bash

# Test Publishing Script
# This script helps test the build and local installation process before publishing to PyPI

set -e

echo "🚀 Starting publish test..."

# Check if we're in the correct directory
if [ ! -f "PyPI_HOWTO.md" ]; then
    echo "❌ Error: PyPI_HOWTO.md not found. Please run this script from the project root."
    exit 1
fi

# Clean up previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/
rm -rf lib_package/build/ lib_package/dist/
rm -rf cli_package/build/ cli_package/dist/

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check required commands
echo "🔍 Checking required commands..."
for cmd in python pip twine pyright; do
    if command_exists "$cmd"; then
        echo "✅ $cmd is available"
    else
        echo "❌ $cmd is missing. Please install it first."
        echo "   Run: pip install hatchling twine pyright"
        exit 1
    fi
done

# Build library package
echo "📦 Building library package..."
cd lib_package
python -m build
echo "✅ Library package built successfully"
ls -la dist/

# Test library installation locally
echo "🧪 Testing library installation..."
pip install --force-reinstall dist/*.whl
python -c "import todowrite; print(f'✅ Library version: {todowrite.__version__}')"

# Run type checking
echo "🔍 Running type checking..."
pyright todowrite/
echo "✅ Type checking passed"

cd ..

# Build CLI package
echo "📦 Building CLI package..."
cd cli_package
python -m build
echo "✅ CLI package built successfully"
ls -la dist/

# Test CLI installation locally
echo "🧪 Testing CLI installation..."
pip install --force-reinstall dist/*.whl
todowrite --version
echo "✅ CLI installation successful"

# Run type checking
echo "🔍 Running type checking..."
pyright todowrite_cli/
echo "✅ Type checking passed"

cd ..

# Test both packages work together
echo "🔗 Testing package integration..."
python -c "
from todowrite import ToDoWrite
print('✅ Both packages integrated successfully')
print(f'✅ Library: {todowrite.__version__}')
"

# Check package distributions
echo "📊 Package distribution check..."
echo "=== Library Package ==="
cd lib_package
twine check dist/*
cd ..

echo "=== CLI Package ==="
cd cli_package
twine check dist/*
cd ..

echo ""
echo "🎉 All tests passed! Ready for publishing to PyPI."
echo ""
echo "Next steps:"
echo "1. Publish to TestPyPI:"
echo "   cd lib_package && twine upload --repository testpypi dist/*"
echo "   cd ../cli_package && twine upload --repository testpypi dist/*"
echo ""
echo "2. Publish to Production PyPI:"
echo "   cd lib_package && twine upload dist/*"
echo "   cd ../cli_package && twine upload dist/*"
echo ""
echo "3. Or use GitHub Actions workflows for automated publishing"
