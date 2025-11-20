import React, { useState, useCallback } from 'react';
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { ChevronRight, ChevronDown, Plus, GripVertical, MoreHorizontal } from 'lucide-react';

// Types for drag and drop
interface DragItem {
  id: number;
  type: string;
  itemType: string;
  parentId?: number;
  originalParentId?: number;
  index: number;
}

interface TodoItem {
  id: number;
  title: string;
  description?: string;
  type: string; // goal, concept, context, constraints, requirement, etc.
  status: 'planned' | 'in_progress' | 'completed';
  progress?: number;
  owner?: string;
  severity?: 'low' | 'medium' | 'high' | 'critical';
  children?: TodoItem[];
  expanded?: boolean;
}

// Layer configurations
const LAYER_CONFIG = {
  goal: { color: 'bg-purple-100 border-purple-300 text-purple-800', icon: '🎯' },
  concept: { color: 'bg-blue-100 border-blue-300 text-blue-800', icon: '💡' },
  context: { color: 'bg-green-100 border-green-300 text-green-800', icon: '🌍' },
  constraints: { color: 'bg-yellow-100 border-yellow-300 text-yellow-800', icon: '⚠️' },
  requirement: { color: 'bg-red-100 border-red-300 text-red-800', icon: '📋' },
  acceptancecriteria: { color: 'bg-indigo-100 border-indigo-300 text-indigo-800', icon: '✅' },
  interfacecontract: { color: 'bg-pink-100 border-pink-300 text-pink-800', icon: '🤝' },
  phase: { color: 'bg-orange-100 border-orange-300 text-orange-800', icon: '📅' },
  step: { color: 'bg-teal-100 border-teal-300 text-teal-800', icon: '🔢' },
  task: { color: 'bg-cyan-100 border-cyan-300 text-cyan-800', icon: '📝' },
  subtask: { color: 'bg-lime-100 border-lime-300 text-lime-800', icon: '🔧' },
  command: { color: 'bg-gray-100 border-gray-300 text-gray-800', icon: '⚡' },
};

// Draggable Item Component
const DraggableItem: React.FC<{
  item: TodoItem;
  index: number;
  parentId?: number;
  onMove: (draggedId: number, targetId: number, newParentId?: number) => void;
  onToggleExpand: (id: number) => void;
  onAddChild: (parentId: number, type: string) => void;
  level: number;
}> = ({ item, index, parentId, onMove, onToggleExpand, onAddChild, level }) => {
  const [{ isDragging }, drag] = useDrag({
    type: 'TODO_ITEM',
    item: (): DragItem => ({
      id: item.id,
      type: 'TODO_ITEM',
      itemType: item.type,
      parentId,
      originalParentId: parentId,
      index,
    }),
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  const [{ isOver, canDrop }, drop] = useDrop({
    accept: 'TODO_ITEM',
    hover: (draggedItem: DragItem) => {
      if (draggedItem.id === item.id) return;

      // Allow dropping on items that can accept children
      const canAcceptChildren = ['goal', 'concept', 'requirement', 'phase', 'step', 'task', 'subtask'];
      if (canAcceptChildren.includes(item.type)) {
        onMove(draggedItem.id, item.id, item.id);
      }
    },
    drop: (draggedItem: DragItem) => {
      // Handle drop for reordering within the same parent
      if (parentId === draggedItem.originalParentId && draggedItem.id !== item.id) {
        onMove(draggedItem.id, item.id, parentId);
      }
    },
    collect: (monitor) => ({
      isOver: monitor.isOver(),
      canDrop: monitor.canDrop(),
    }),
  });

  const layerConfig = LAYER_CONFIG[item.type as keyof typeof LAYER_CONFIG];
  const hasChildren = item.children && item.children.length > 0;
  const canAcceptChildren = ['goal', 'concept', 'requirement', 'phase', 'step', 'task', 'subtask'].includes(item.type);

  return (
    <div
      ref={(node) => drag(drop(node))}
      className={`transition-all duration-200 ${isDragging ? 'opacity-50' : ''} ${
        isOver && canDrop ? 'ring-2 ring-blue-400 ring-opacity-50' : ''
      }`}
      style={{ marginLeft: `${level * 24}px` }}
    >
      <div
        className={`border rounded-lg p-3 mb-2 cursor-move hover:shadow-md transition-shadow ${layerConfig.color} ${
          isOver && canDrop ? 'border-blue-400' : ''
        }`}
      >
        <div className="flex items-center gap-2">
          {/* Drag Handle */}
          <GripVertical className="w-4 h-4 opacity-50 hover:opacity-100" />

          {/* Expand/Collapse for items with children */}
          {hasChildren && (
            <button
              onClick={() => onToggleExpand(item.id)}
              className="p-1 hover:bg-black hover:bg-opacity-10 rounded"
            >
              {item.expanded ? (
                <ChevronDown className="w-4 h-4" />
              ) : (
                <ChevronRight className="w-4 h-4" />
              )}
            </button>
          )}

          {/* Type Icon */}
          <span className="text-lg">{layerConfig.icon}</span>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <h4 className="font-semibold text-sm truncate">{item.title}</h4>
            {item.description && (
              <p className="text-xs opacity-75 truncate">{item.description}</p>
            )}

            {/* Metadata */}
            <div className="flex items-center gap-4 mt-1 text-xs opacity-75">
              {item.owner && <span>👤 {item.owner}</span>}
              {item.progress !== undefined && <span>📊 {item.progress}%</span>}
              {item.severity && <span>🚨 {item.severity}</span>}
              <span className={`px-2 py-1 rounded-full text-xs ${
                item.status === 'completed' ? 'bg-green-200 text-green-800' :
                item.status === 'in_progress' ? 'bg-yellow-200 text-yellow-800' :
                'bg-gray-200 text-gray-800'
              }`}>
                {item.status}
              </span>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-1">
            {canAcceptChildren && (
              <button
                onClick={() => onAddChild(item.id, getNextChildType(item.type))}
                className="p-1 hover:bg-black hover:bg-opacity-10 rounded opacity-50 hover:opacity-100"
                title="Add child item"
              >
                <Plus className="w-4 h-4" />
              </button>
            )}
            <button className="p-1 hover:bg-black hover:bg-opacity-10 rounded opacity-50 hover:opacity-100">
              <MoreHorizontal className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Render children if expanded */}
      {hasChildren && item.expanded && (
        <div className="ml-2">
          {item.children!.map((child, childIndex) => (
            <DraggableItem
              key={child.id}
              item={child}
              index={childIndex}
              parentId={item.id}
              onMove={onMove}
              onToggleExpand={onToggleExpand}
              onAddChild={onAddChild}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
};

// Helper function to determine next logical child type
function getNextChildType(parentType: string): string {
  const childTypes: Record<string, string> = {
    goal: 'concept',
    concept: 'context',
    context: 'constraints',
    constraints: 'requirement',
    requirement: 'acceptancecriteria',
    acceptancecriteria: 'interfacecontract',
    interfacecontract: 'phase',
    phase: 'step',
    step: 'task',
    task: 'subtask',
    subtask: 'command',
    command: 'command', // Commands can't have children
  };
  return childTypes[parentType] || 'task';
}

// Main Hierarchical View Component
export const HierarchicalTaskView: React.FC = () => {
  const [items, setItems] = useState<TodoItem[]>([
    // Sample data - this would come from API
    {
      id: 1,
      title: "Launch Q1 Product",
      description: "Complete product launch by end of Q1",
      type: "goal",
      status: "in_progress",
      owner: "product-team",
      severity: "high",
      expanded: true,
      children: [
        {
          id: 2,
          title: "Mobile-First Design Strategy",
          type: "concept",
          status: "in_progress",
          owner: "design-team",
          expanded: true,
          children: [
            {
              id: 3,
              title: "Responsive Design Requirements",
              type: "requirement",
              status: "in_progress",
              owner: "design-team",
              children: [
                {
                  id: 4,
                  title: "Mobile Layout Works on All Screen Sizes",
                  type: "acceptancecriteria",
                  status: "planned",
                  owner: "qa-team"
                }
              ]
            }
          ]
        },
        {
          id: 5,
          title: "User Authentication Flow",
          type: "requirement",
          status: "planned",
          owner: "dev-team",
          children: [
            {
              id: 6,
              title: "Sprint 1: Backend Setup",
              type: "phase",
              status: "planned",
              owner: "dev-team",
              children: [
                {
                  id: 7,
                  title: "Design Database Schema",
                  type: "step",
                  status: "planned",
                  owner: "dev-team",
                  children: [
                    {
                      id: 8,
                      title: "Create User Table Migration",
                      type: "task",
                      status: "planned",
                      owner: "dev-team",
                      progress: 0,
                      children: [
                        {
                          id: 9,
                          title: "Add Email Field to User Table",
                          type: "subtask",
                          status: "planned",
                          owner: "dev-team",
                          children: [
                            {
                              id: 10,
                              title: "Run Database Migration",
                              type: "command",
                              run_command: "python manage.py migrate",
                              status: "planned",
                              owner: "dev-team"
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]);

  const handleMove = useCallback((draggedId: number, targetId: number, newParentId?: number) => {
    setItems(prevItems => {
      // Complex logic to reorder/move items in hierarchy
      // This would update the database via API calls
      console.log(`Moving item ${draggedId} to target ${targetId}, new parent: ${newParentId}`);
      return prevItems; // Placeholder - would implement actual reordering logic
    });
  }, []);

  const handleToggleExpand = useCallback((id: number) => {
    setItems(prevItems => {
      const updateItem = (items: TodoItem[]): TodoItem[] => {
        return items.map(item => {
          if (item.id === id) {
            return { ...item, expanded: !item.expanded };
          }
          if (item.children) {
            return { ...item, children: updateItem(item.children) };
          }
          return item;
        });
      };
      return updateItem(prevItems);
    });
  }, []);

  const handleAddChild = useCallback((parentId: number, type: string) => {
    // Logic to add a new child item
    console.log(`Adding ${type} to parent ${parentId}`);
    // This would open a modal or inline form for creating the new item
  }, []);

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="p-6 bg-gray-50 min-h-screen">
        <div className="max-w-6xl mx-auto">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Task Management</h1>
            <p className="text-gray-600">Drag and drop to reorganize your hierarchical tasks</p>
          </div>

          {/* Quick Actions */}
          <div className="mb-6 flex gap-2">
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              + Add Goal
            </button>
            <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
              + Add Task
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              🔍 Search
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              ⚙️ Filter
            </button>
          </div>

          {/* Hierarchical Items */}
          <div className="space-y-2">
            {items.map((item, index) => (
              <DraggableItem
                key={item.id}
                item={item}
                index={index}
                onMove={handleMove}
                onToggleExpand={handleToggleExpand}
                onAddChild={handleAddChild}
                level={0}
              />
            ))}
          </div>
        </div>
      </div>
    </DndProvider>
  );
};