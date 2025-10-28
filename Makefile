# ToDoWrite System Makefile
# Complete workflow automation for 12-layer declarative planning framework

.PHONY: help tw-all tw-deps tw-init tw-schema tw-lint tw-validate tw-trace tw-prove tw-hooks tw-clean tw-check tw-test tw-dev tw-prod

help: ## Show this help message
	@echo "ToDoWrite System - Makefile targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

tw-deps: ## Install Python dependencies
	@echo "Installing ToDoWrite dependencies..."
	@pip install --upgrade pip
	@pip install pyyaml jsonschema click fastapi uvicorn sqlalchemy pytest ruff mypy
	@echo "Dependencies installed successfully"

tw-init: ## Initialize ToDoWrite directory structure
	@echo "Initializing ToDoWrite directory structure..."
	@mkdir -p configs/plans/{goals,concepts,contexts,constraints,requirements,acceptance_criteria,interface_contracts,phases,steps,tasks,subtasks}
	@mkdir -p configs/commands configs/schemas
	@mkdir -p todowrite/tools trace results .git/hooks
	@touch trace/trace.csv trace/graph.json
	@echo "Directory structure initialized successfully"

tw-schema: ## Generate JSON schema from specification
	@echo "Generating JSON schema..."
	@python -c "import json; schema={'$$schema':'https://json-schema.org/draft/2020-12/schema','title':'ToDoWrite Node','type':'object','required':['id','layer','title','description','links'],'properties':{'id':{'type':'string','pattern':'^(GOAL|CON|CTX|CST|R|AC|IF|PH|STP|TSK|SUB|CMD)-[A-Z0-9_-]+$$'},'layer':{'type':'string','enum':['Goal','Concept','Context','Constraints','Requirements','AcceptanceCriteria','InterfaceContract','Phase','Step','Task','SubTask','Command']},'title':{'type':'string','minLength':1},'description':{'type':'string'},'metadata':{'type':'object','properties':{'owner':{'type':'string'},'labels':{'type':'array','items':{'type':'string'}},'severity':{'type':'string','enum':['low','med','high']},'work_type':{'type':'string','enum':['architecture','spec','interface','validation','implementation','docs','ops','refactor','chore','test']}},'additionalProperties':True},'links':{'type':'object','required':['parents','children'],'properties':{'parents':{'type':'array','items':{'type':'string'}},'children':{'type':'array','items':{'type':'string'}}}},'command':{'type':'object','properties':{'ac_ref':{'type':'string','pattern':'^AC-[A-Z0-9_-]+$$'},'run':{'type':'object','properties':{'shell':{'type':'string'},'workdir':{'type':'string'},'env':{'type':'object','additionalProperties':{'type':'string'}}},'required':['shell']},'artifacts':{'type':'array','items':{'type':'string'}}},'required':['ac_ref','run'],'additionalProperties':False}},'allOf':[{'if':{'properties':{'layer':{'const':'Command'}}},'then':{'required':['command']}},{'if':{'properties':{'layer':{'enum':['Goal','Concept','Context','Constraints','Requirements','AcceptanceCriteria','InterfaceContract','Phase','Step','Task','SubTask']}}},'then':{'not':{'required':['command']}}}],'additionalProperties':False}; print(json.dumps(schema, indent=2))" > configs/schemas/todowrite.schema.json
	@echo "JSON schema generated successfully"

tw-lint: ## Check Separation of Concerns for layers 1-11
	@echo "Running SoC linter..."
	@python todowrite/tools/tw_lint_soc.py

tw-validate: ## Validate all YAML files against schema
	@echo "Validating YAML files..."
	@python todowrite/tools/tw_validate.py

tw-trace: ## Build traceability matrix and graph
	@echo "Building traceability matrix..."
	@python todowrite/tools/tw_trace.py

tw-prove: ## Generate command stubs from Acceptance Criteria
	@echo "Generating command stubs..."
	@python todowrite/tools/tw_stub_command.py

tw-hooks: ## Install git commit hooks
	@echo "Installing git hooks..."
	@cp todowrite/tools/git-commit-msg-hook.sh .git/hooks/commit-msg
	@chmod +x .git/hooks/commit-msg
	@echo "Git hooks installed successfully"

tw-clean: ## Remove generated files
	@echo "Cleaning generated files..."
	@rm -rf trace/* results/* .git/hooks/commit-msg
	@touch trace/trace.csv trace/graph.json
	@echo "Clean completed"

tw-all: tw-schema tw-lint tw-validate tw-trace tw-prove ## Run schema, lint, validate, trace, prove (default)
	@echo "ToDoWrite validation complete"

tw-check: tw-all ## Full validation with strict error checking
	@echo "Running strict validation checks..."
	@python todowrite/tools/tw_validate.py --strict
	@echo "Strict validation passed"

tw-test: ## Test complete ToDoWrite system
	@echo "Running system tests..."
	@python -m pytest tests/ -v
	@echo "System tests completed"

tw-dev: tw-lint tw-validate tw-prove ## Development workflow (lint + validate + generate commands)
	@echo "Development workflow completed"

tw-prod: tw-all tw-check ## Production workflow (full validation + traceability + commands)
	@echo "Production workflow completed"

# Default target
.DEFAULT_GOAL := tw-all