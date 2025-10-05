function CalendarPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Calendar</h1>
      <div className="card">
        <p className="text-gray-600">Your scheduled recordings calendar will appear here</p>
        <button className="btn-secondary mt-4">Export to iCal</button>
      </div>
    </div>
  )
}

export default CalendarPage
