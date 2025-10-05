function LoginPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to SD Browser
          </h2>
        </div>
        <form className="mt-8 space-y-6">
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <input
                type="email"
                placeholder="Email address"
                className="input rounded-t-md"
                required
              />
            </div>
            <div>
              <input
                type="password"
                placeholder="Password"
                className="input rounded-b-md"
                required
              />
            </div>
          </div>
          <div>
            <button
              type="submit"
              className="btn-primary w-full py-2 px-4"
            >
              Sign in
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default LoginPage
