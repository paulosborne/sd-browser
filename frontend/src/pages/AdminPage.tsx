function AdminPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Admin Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Background Jobs</h3>
          <p className="text-gray-600">Monitor job queue status</p>
        </div>
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">System Health</h3>
          <p className="text-gray-600">View system health metrics</p>
        </div>
      </div>
    </div>
  )
}

export default AdminPage
