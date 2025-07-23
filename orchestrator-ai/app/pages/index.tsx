import Head from 'next/head';

export default function HomePage() {
  return (
    <>
      <Head>
        <title>Orchestrator AI</title>
        <meta name="description" content="Advanced AI orchestration platform for seamless automation and intelligent workflow management" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <script src="https://cdn.tailwindcss.com"></script>
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900">
        <div className="container mx-auto px-4 py-16">
          {/* Header */}
          <header className="text-center mb-16">
            <h1 className="text-6xl font-bold text-white mb-4">
              Orchestrator AI
            </h1>
            <p className="text-xl text-blue-200 max-w-2xl mx-auto">
              Advanced AI orchestration platform for seamless automation and intelligent workflow management
            </p>
          </header>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-8 mb-16">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Intelligent Automation</h3>
              <p className="text-blue-200">Automate complex workflows with AI-powered decision making and adaptive orchestration.</p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Real-time Analytics</h3>
              <p className="text-blue-200">Monitor and analyze your AI workflows with comprehensive dashboards and insights.</p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <div className="w-12 h-12 bg-indigo-500 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Seamless Integration</h3>
              <p className="text-blue-200">Connect with your existing tools and services through our robust API and integration platform.</p>
            </div>
          </div>

          {/* Status Section */}
          <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10 text-center">
            <h2 className="text-2xl font-semibold text-white mb-4">System Status</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="w-3 h-3 bg-green-400 rounded-full mx-auto mb-2"></div>
                <p className="text-sm text-green-300">Frontend</p>
              </div>
              <div className="text-center">
                <div className="w-3 h-3 bg-green-400 rounded-full mx-auto mb-2"></div>
                <p className="text-sm text-green-300">Backend API</p>
              </div>
              <div className="text-center">
                <div className="w-3 h-3 bg-green-400 rounded-full mx-auto mb-2"></div>
                <p className="text-sm text-green-300">Database</p>
              </div>
              <div className="text-center">
                <div className="w-3 h-3 bg-green-400 rounded-full mx-auto mb-2"></div>
                <p className="text-sm text-green-300">Cache</p>
              </div>
            </div>
            <div className="mt-6">
              <a 
                href="/api/health" 
                className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Check Health Status
              </a>
            </div>
          </div>

          {/* Footer */}
          <footer className="text-center mt-16 text-blue-300">
            <p>&copy; 2024 Orchestrator AI. Powered by Next.js and AI.</p>
          </footer>
        </div>
      </div>
    </>
  );
}
