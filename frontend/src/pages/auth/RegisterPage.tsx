function RegisterPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
        </div>
        <form className="mt-8 space-y-6">
          <div className="space-y-4">
            <input
              type="email"
              placeholder="Email address"
              className="input"
              required
            />
            <input
              type="password"
              placeholder="Password"
              className="input"
              required
            />
          </div>
          <div>
            <button
              type="submit"
              className="btn-primary w-full py-2 px-4"
            >
              Create account
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default RegisterPage
