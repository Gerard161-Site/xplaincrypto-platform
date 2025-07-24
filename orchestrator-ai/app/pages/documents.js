import Layout from '../components/Layout';
import { useState, useEffect } from 'react';

export default function Documents() {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleFileUpload = async (files) => {
    setUploading(true);
    const formData = new FormData();
    
    Array.from(files).forEach(file => {
      formData.append('documents', file);
    });

    try {
      const response = await fetch('/api/documents/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        const result = await response.json();
        setDocuments(prev => [...prev, ...result.documents]);
      }
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files);
    }
  };

  return (
    <Layout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-white">Context Engineering</h1>
          <p className="text-gray-400 mt-2">Upload documents to enhance AI agent knowledge</p>
        </div>

        {/* Upload Area */}
        <div className="card">
          <h3 className="text-xl font-semibold text-white mb-6">Upload Documents</h3>
          
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-all ${
              dragActive 
                ? 'border-orange-500 bg-orange-500/10' 
                : 'border-gray-600 hover:border-orange-500/50'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            {uploading ? (
              <div className="space-y-4">
                <div className="w-16 h-16 gradient-bg rounded-full flex items-center justify-center mx-auto animate-pulse">
                  <span className="text-white text-2xl">📄</span>
                </div>
                <p className="text-white font-medium">Processing documents...</p>
                <div className="w-64 bg-gray-700 rounded-full h-2 mx-auto">
                  <div className="gradient-bg h-2 rounded-full animate-pulse"></div>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center mx-auto">
                  <span className="text-gray-400 text-2xl">📁</span>
                </div>
                <div>
                  <p className="text-white font-medium">Drop files here or click to browse</p>
                  <p className="text-gray-400 text-sm mt-2">
                    Supports PDF, DOC, TXT, MD files up to 10MB each
                  </p>
                </div>
                <input
                  type="file"
                  multiple
                  accept=".pdf,.doc,.docx,.txt,.md"
                  onChange={(e) => handleFileUpload(e.target.files)}
                  className="hidden"
                  id="file-upload"
                />
                <label htmlFor="file-upload" className="btn-primary inline-block cursor-pointer">
                  Choose Files
                </label>
              </div>
            )}
          </div>
        </div>

        {/* Document List */}
        <div className="card">
          <h3 className="text-xl font-semibold text-white mb-6">Knowledge Base</h3>
          
          {documents.length === 0 ? (
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-gray-400 text-2xl">📚</span>
              </div>
              <p className="text-gray-400">No documents uploaded yet</p>
              <p className="text-gray-500 text-sm mt-2">Upload documents to enhance AI agent knowledge</p>
            </div>
          ) : (
            <div className="space-y-4">
              {documents.map((doc, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-800/30 rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 gradient-bg rounded-lg flex items-center justify-center">
                      <span className="text-white text-sm">📄</span>
                    </div>
                    <div>
                      <p className="text-white font-medium">{doc.name}</p>
                      <p className="text-gray-400 text-sm">
                        {doc.size} • {doc.chunks} chunks • Processed {doc.processedAt}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-xs">
                      ✓ Indexed
                    </span>
                    <button className="text-gray-400 hover:text-red-400 transition-colors">
                      🗑️
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Context Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card">
            <div className="text-center">
              <div className="w-12 h-12 gradient-bg rounded-lg flex items-center justify-center mx-auto mb-3">
                <span className="text-white text-xl">📊</span>
              </div>
              <p className="text-2xl font-bold text-white">{documents.length}</p>
              <p className="text-gray-400 text-sm">Documents</p>
            </div>
          </div>
          
          <div className="card">
            <div className="text-center">
              <div className="w-12 h-12 gradient-bg rounded-lg flex items-center justify-center mx-auto mb-3">
                <span className="text-white text-xl">🧩</span>
              </div>
              <p className="text-2xl font-bold text-white">
                {documents.reduce((sum, doc) => sum + (doc.chunks || 0), 0)}
              </p>
              <p className="text-gray-400 text-sm">Text Chunks</p>
            </div>
          </div>
          
          <div className="card">
            <div className="text-center">
              <div className="w-12 h-12 gradient-bg rounded-lg flex items-center justify-center mx-auto mb-3">
                <span className="text-white text-xl">🎯</span>
              </div>
              <p className="text-2xl font-bold text-white">98%</p>
              <p className="text-gray-400 text-sm">Accuracy</p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}