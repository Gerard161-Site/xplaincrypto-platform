
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Card, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, Github, Code, MessageSquare } from 'lucide-react';
import { WorkflowFormData, Workflow } from '@/lib/types';
import { toast } from 'sonner';

interface WorkflowFormProps {
  onWorkflowStart: (workflow: Workflow) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export function WorkflowForm({ onWorkflowStart, isLoading, setIsLoading }: WorkflowFormProps) {
  const [formData, setFormData] = useState<WorkflowFormData>({
    githubUrl: '',
    prompt: '',
    mode: 'self-contained',
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      // Validate GitHub URL
      if (!formData.githubUrl.includes('github.com')) {
        throw new Error('Please provide a valid GitHub URL');
      }

      // Validate prompt for prompt-driven mode
      if (formData.mode === 'prompt-driven' && !formData.prompt?.trim()) {
        throw new Error('Prompt is required for prompt-driven mode');
      }

      // Map frontend field names to backend API field names
      const apiData = {
        repository_url: formData.githubUrl,
        task_prompt: formData.prompt,
      };

      const response = await fetch('/api/workflow', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(apiData),
      });

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error || 'Failed to start workflow');
      }

      // Create workflow object for the callback - handle both response formats
      const workflowId = result.workflow_id || result.data?.workflowId || 'unknown';
      const mockWorkflow: Workflow = {
        id: workflowId,
        githubUrl: formData.githubUrl,
        prompt: formData.prompt,
        mode: formData.mode,
        status: 'pending',
        progress: 0,
        userId: '',
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      onWorkflowStart(mockWorkflow);

      // Reset form
      setFormData({
        githubUrl: '',
        prompt: '',
        mode: 'self-contained',
      });

      toast.success('Workflow started successfully!');

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An error occurred';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleModeChange = (checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      mode: checked ? 'prompt-driven' : 'self-contained',
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <Alert className="border-red-500 bg-red-500/10">
          <AlertDescription className="text-red-400">
            {error}
          </AlertDescription>
        </Alert>
      )}

      {/* GitHub URL Input */}
      <div className="space-y-2">
        <Label htmlFor="githubUrl" className="text-white flex items-center">
          <Github className="h-4 w-4 mr-2" />
          GitHub Repository URL
        </Label>
        <Input
          id="githubUrl"
          type="url"
          value={formData.githubUrl}
          onChange={(e) => setFormData(prev => ({ ...prev, githubUrl: e.target.value }))}
          placeholder="https://github.com/username/repository"
          className="bg-slate-800 border-slate-600 text-white placeholder-slate-400"
          required
        />
      </div>

      {/* Mode Toggle */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <Label htmlFor="mode-toggle" className="text-white flex items-center">
            <Code className="h-4 w-4 mr-2" />
            Workflow Mode
          </Label>
          <div className="flex items-center space-x-2">
            <span className={`text-sm ${formData.mode === 'self-contained' ? 'text-white' : 'text-slate-400'}`}>
              Self-contained
            </span>
            <Switch
              id="mode-toggle"
              checked={formData.mode === 'prompt-driven'}
              onCheckedChange={handleModeChange}
            />
            <span className={`text-sm ${formData.mode === 'prompt-driven' ? 'text-white' : 'text-slate-400'}`}>
              Prompt-driven
            </span>
          </div>
        </div>

        <Card className="bg-slate-700/50 border-slate-600">
          <CardContent className="pt-4">
            <p className="text-sm text-slate-300">
              {formData.mode === 'self-contained' 
                ? "Automatically analyze and deploy the repository based on detected patterns and configurations."
                : "Use a custom prompt to guide the multi-agent workflow for specific tasks and objectives."
              }
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Prompt Input (conditional) */}
      {formData.mode === 'prompt-driven' && (
        <div className="space-y-2">
          <Label htmlFor="prompt" className="text-white flex items-center">
            <MessageSquare className="h-4 w-4 mr-2" />
            Task Prompt
          </Label>
          <Textarea
            id="prompt"
            value={formData.prompt}
            onChange={(e) => setFormData(prev => ({ ...prev, prompt: e.target.value }))}
            placeholder="Describe what you want the AI agents to accomplish..."
            className="bg-slate-800 border-slate-600 text-white placeholder-slate-400 min-h-[100px]"
            required={formData.mode === 'prompt-driven'}
          />
        </div>
      )}

      {/* Submit Button */}
      <Button
        type="submit"
        disabled={isLoading}
        className="w-full bg-purple-600 hover:bg-purple-700 text-white"
      >
        {isLoading ? (
          <>
            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
            Starting Workflow...
          </>
        ) : (
          'Start Workflow'
        )}
      </Button>
    </form>
  );
}
