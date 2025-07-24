
'use client';

import { useState, useEffect } from 'react';
import { useSession, signOut } from 'next-auth/react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { LogOut, Terminal, Activity, Github } from 'lucide-react';

import { ProgressPanel } from '@/components/progress-panel';
import { WorkflowHistory } from '@/components/workflow-history';
import { Workflow } from '@/lib/types';
import { toast } from 'sonner';

export default function DashboardClient() {
  const { data: session } = useSession();
  const [activeWorkflow, setActiveWorkflow] = useState<Workflow | null>(null);
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchWorkflows = async () => {
    try {
      const response = await fetch('/api/workflow');
      const result = await response.json();
      
      if (result.success) {
        setWorkflows(result.data || []);
      }
    } catch (error) {
      console.error('Error fetching workflows:', error);
    }
  };

  useEffect(() => {
    fetchWorkflows();
  }, []);

  const handleWorkflowStart = async (workflow: Workflow) => {
    setActiveWorkflow(workflow);
    await fetchWorkflows();
    toast.success('Workflow started successfully');
  };

  const handleSignOut = () => {
    signOut({ callbackUrl: '/login' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b border-orange-500/20 bg-black/50 backdrop-blur-xl">
        <div className="container mx-auto max-w-6xl flex h-16 items-center justify-between px-4">
          <div className="flex items-center space-x-3">
            <div className="gradient-bg p-2 rounded-lg">
              <Terminal className="h-5 w-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-semibold text-white">Automotas AI</h1>
              <p className="text-xs text-gray-400">Multi-Agent Orchestrator</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-sm font-medium text-white">{session?.user?.name || session?.user?.email}</p>
              <p className="text-xs text-slate-400">Administrator</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={handleSignOut}
              className="border-orange-500/20 hover:bg-orange-500/10 hover:text-orange-400"
            >
              <LogOut className="h-4 w-4 mr-2" />
              Sign Out
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto max-w-6xl p-4 space-y-6">
        {/* Welcome Section */}
        <div className="text-center py-8">
          <h2 className="text-3xl font-bold text-white mb-2">
            Welcome to Automotas AI
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Manage and monitor your multi-agent workflows. Submit GitHub repositories for automated analysis, 
            review, and deployment through our intelligent orchestration system.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Workflow Form */}
          <Card className="card">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Activity className="h-5 w-5 mr-2 text-orange-400" />
                New Workflow
              </CardTitle>
              <CardDescription className="text-gray-400">
                Start a new multi-agent workflow by providing a GitHub repository
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8 space-y-4">
                <div className="gradient-bg w-16 h-16 rounded-lg flex items-center justify-center mx-auto">
                  <Github className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white">Orange Theme Test</h3>
                <p className="text-gray-400">Testing the new Automotas AI orange styling</p>
                <Button className="btn-primary">Test Orange Button</Button>
              </div>
            </CardContent>
          </Card>

          {/* Progress Panel */}
          <Card className="card">
            <CardHeader>
              <CardTitle className="text-white">Real-time Progress</CardTitle>
              <CardDescription className="text-gray-400">
                Monitor active workflow progress and agent activities
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ProgressPanel activeWorkflow={activeWorkflow} />
            </CardContent>
          </Card>
        </div>

        {/* Workflow History */}
        <Card className="card">
          <CardHeader>
            <CardTitle className="text-white">Workflow History</CardTitle>
            <CardDescription className="text-gray-400">
              Review past workflows and their results
            </CardDescription>
          </CardHeader>
          <CardContent>
            <WorkflowHistory 
              workflows={workflows} 
              onRefresh={fetchWorkflows}
              onViewWorkflow={setActiveWorkflow}
            />
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
