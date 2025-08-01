'use client';

import React from 'react';

export default function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 py-20 lg:py-32">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-grid-slate-100/[0.02] bg-[size:75px_75px]" />
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 via-transparent to-purple-500/10" />
      
      {/* Content Container */}
      <div className="relative mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-5xl text-center">
          {/* Hero Headline - Single line with reduced font size */}
          <h1 className="text-3xl font-bold tracking-tight text-white sm:text-4xl lg:text-5xl xl:text-6xl">
            <span className="block whitespace-nowrap">
              Automatos AI: Stop Fighting Your AI Agents
            </span>
          </h1>
          
          {/* Hero Description - Reduced font size */}
          <p className="mx-auto mt-8 max-w-4xl text-base leading-relaxed text-slate-300 sm:text-lg lg:text-lg xl:text-lg">
            Built for developers tired of agents that lose context, fabricate results, and require constant re-explanation. 
            The open-source multi-agent orchestration platform that combines advanced context engineering with persistent memory. 
            Build, deploy, and scale intelligent workflows that learn from and adapt to your infrastructure.
          </p>
          
          {/* CTA Buttons */}
          <div className="mt-10 flex flex-col gap-4 sm:flex-row sm:justify-center sm:gap-6">
            <a
              href="#get-started"
              className="inline-flex items-center justify-center rounded-lg bg-blue-600 px-8 py-3 text-lg font-semibold text-white shadow-lg transition-all duration-200 hover:bg-blue-700 hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-slate-900"
            >
              Get Started
              <svg className="ml-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </a>
            <a
              href="#documentation"
              className="inline-flex items-center justify-center rounded-lg border border-slate-600 bg-slate-800/50 px-8 py-3 text-lg font-semibold text-white backdrop-blur-sm transition-all duration-200 hover:bg-slate-700/50 hover:border-slate-500 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2 focus:ring-offset-slate-900"
            >
              View Documentation
            </a>
          </div>
          
          {/* Key Features */}
          <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-3">
            <div className="flex flex-col items-center text-center">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-600/20 backdrop-blur-sm">
                <svg className="h-6 w-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="mt-4 text-lg font-semibold text-white">Context Engineering</h3>
              <p className="mt-2 text-sm text-slate-400">Advanced context management that maintains coherence across agent interactions</p>
            </div>
            
            <div className="flex flex-col items-center text-center">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-600/20 backdrop-blur-sm">
                <svg className="h-6 w-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="mt-4 text-lg font-semibold text-white">Persistent Memory</h3>
              <p className="mt-2 text-sm text-slate-400">Agents remember past interactions and learn from previous workflows</p>
            </div>
            
            <div className="flex flex-col items-center text-center">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-600/20 backdrop-blur-sm">
                <svg className="h-6 w-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                </svg>
              </div>
              <h3 className="mt-4 text-lg font-semibold text-white">Infrastructure Aware</h3>
              <p className="mt-2 text-sm text-slate-400">Deploy and scale workflows that adapt to your existing infrastructure</p>
            </div>
          </div>
        </div>
      </div>
      
      {/* Floating Elements */}
      <div className="absolute top-10 left-10 h-20 w-20 rounded-full bg-blue-500/10 blur-xl" />
      <div className="absolute bottom-10 right-10 h-32 w-32 rounded-full bg-purple-500/10 blur-xl" />
    </section>
  );
}