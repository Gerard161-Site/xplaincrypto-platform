import Layout from '../components/Layout';
import { useState, useEffect } from 'react';

export default function Workflows() {
  const [workflows, setWorkflows] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newWorkflow, setNewWorkflow] = useState({
    name: '',
    description: '',
    repoUrl: '',
    prompt: '',
    mode: 'self-contained' // or 'prompt-driven'
  });

  const createWorkflow = async () => {
    try {
      const response = await fetch('/api/workflows/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newWorkflow),
      });
      
      if (response.ok) {
        const workflow = await response.json();
        setWorkflows(prev => [workflow, ...prev]);
        setShowCreateModal(false);
        setNewWorkflow({ name: '', description: '', repoUrl: '', prompt: '', mode: 'self-contained' });
      }
    } catch (error) {
      console.error('Failed to create workflow:', error);
    }
  };

  return (
    <Layout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-white">Workflows</h1>
            <p className="text-gray-400 mt-2">Manage your AI agent workflows</p>
          </div>
          <button 
            onClick={() => setShowCreateModal(true)}
            className="btn-primary"
          >
            + New Workflow
          </button>
        </div>

        {/* Workflow Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {workflows.map((workflow, index) => (
            <div key={index} className="card hover:border-orange-500/40 transition-all cursor-pointer">
              <div className="flex items-start justify-between mb-4">
                <div className="w-12 h-12 gradient-bg rounded-lg flex items-center justify-center">
                  <span className="text-white text-xl">⚡</span>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs ${
                  workflow.status === 'running' ? 'bg-orange-500/20 text-orange-400' :
                  workflow.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                  'bg-gray-500/20 text-gray-400'
                }`}>
                  {workflow.status}
                </span>
              </div>
              
              <h3 className="text-lg font-semibold text-white mb-2">{workflow.name}</h3>
              <p className="text-gray-400 text-sm mb-4">{workflow.description}</p>
              
              <div className="space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-gray-500">Mode:</span>
                  <span className="text-gray-300">{workflow.mode}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Created:</span>
                  <span className="text-gray-300">{workflow.createdAt}</span>
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t border-gray-700 flex space-x-2">
                <button className="flex-1 px-3 py-2 bg-orange-500/20 text-orange-400 rounded text-sm hover:bg-orange-500/30 transition-colors">
                  View
                </button>
                <button className="flex-1 px-3 py-2 bg-gray-700/50 text-gray-300 rounded text-sm hover:bg-gray-700 transition-colors">
                  Edit
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Create Modal */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="card max-w-2xl w-full mx-4">
              <h3 className="text-2xl font-bold text-white mb-6">Create New Workflow</h3>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Workflow Name
                  </label>
                  <input
                    type="text"
                    value={newWorkflow.name}
                    onChange={(e) => setNewWorkflow({...newWorkflow, name: e.target.value})}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20"
                    placeholder="Bug Fix Workflow"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Repository URL
                  </label>
                  <input
                    type="url"
                    value={newWorkflow.repoUrl}
                    onChange={(e) => setNewWorkflow({...newWorkflow, repoUrl: e.target.value})}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20"
                    placeholder="https://github.com/user/repo"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Mode
                  </label>
                  <div className="flex space-x-4">
                    <label className="flex items-center">
                      <input
                        type="radio"
                        value="self-contained"
                        checked={newWorkflow.mode === 'self-contained'}
                        onChange={(e) => setNewWorkflow({...newWorkflow, mode: e.target.value})}
                        className="mr-2"
                      />
                      <span className="text-gray-300">Self-Contained Repo</span>
                    </label>
                    <label className="flex items-center">
                      <input
                        type="radio"
                        value="prompt-driven"
                        checked={newWorkflow.mode === 'prompt-driven'}
                        onChange={(e) => setNewWorkflow({...newWorkflow, mode: e.target.value})}
                        className="mr-2"
                      />
                      <span className="text-gray-300">Prompt-Driven</span>
                    </label>
                  </div>
                </div>

                {newWorkflow.mode === 'prompt-driven' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Task Prompt
                    </label>
                    <textarea
                      value={newWorkflow.prompt}
                      onChange={(e) => setNewWorkflow({...newWorkflow, prompt: e.target.value})}
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 h-32"
                      placeholder="Describe the task you want the AI agents to perform..."
                    />
                  </div>
                )}
              </div>

              <div className="flex space-x-4 mt-8">
                <button
                  onClick={createWorkflow}
                  className="btn-primary flex-1"
                >
                  Create Workflow
                </button>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 px-4 py-3 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}