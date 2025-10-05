function OnboardingPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Welcome to SD Browser</h1>
      <div className="card max-w-2xl mx-auto">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Connect your Schedules Direct account</h2>
        <p className="text-gray-600 mb-6">
          To get started, please connect your Schedules Direct account to begin downloading TV guide data.
        </p>
        <button className="btn-primary">
          Connect Schedules Direct
        </button>
      </div>
    </div>
  )
}

export default OnboardingPage
