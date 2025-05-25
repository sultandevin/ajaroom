import LoginForm from "@/components/forms/LoginForm"

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-muted">
      <div className="w-full max-w-md p-6 bg-background border rounded-xl shadow-md">
        <h1 className="text-2xl font-bold mb-6 text-center text-foreground">
          Login to Booking System
        </h1>
        <LoginForm />
      </div>
    </main>
  )
}
