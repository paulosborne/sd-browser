function SearchPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Search Programs</h1>
      <div className="card">
        <input
          type="text"
          placeholder="Search for programs, movies, shows..."
          className="input mb-4"
        />
        <button className="btn-primary">Search</button>
      </div>
    </div>
  )
}

export default SearchPage
