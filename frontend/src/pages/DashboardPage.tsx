function DashboardPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">EPG Guide</h3>
          <p className="text-gray-600 mb-4">Browse TV schedules and programs</p>
          <button className="btn-primary">View Guide</button>
        </div>
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Search</h3>
          <p className="text-gray-600 mb-4">Find programs by title, genre, or person</p>
          <button className="btn-primary">Search Programs</button>
        </div>
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Favourites</h3>
          <p className="text-gray-600 mb-4">Manage your favorite shows</p>
          <button className="btn-primary">View Favourites</button>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage
