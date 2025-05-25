"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"
import { Mail, Lock } from "lucide-react"

export default function LoginForm() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const router = useRouter()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (email === "admin@example.com" && password === "password") {
      router.push("/rooms")
    } else {
      alert("Email atau password salah")
    }
  }

  return (
    <div className="max-w-md mx-auto bg-card border border-muted rounded-xl shadow-md p-6 space-y-6">

      <form onSubmit={handleSubmit} className="space-y-5">
        <div className="grid gap-2">
          <Label htmlFor="email" className="font-medium text-foreground">
            Email
          </Label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="pl-10"
              required
            />
          </div>
        </div>

        <div className="grid gap-2">
          <Label htmlFor="password" className="font-medium text-foreground">
            Password
          </Label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <Input
              id="password"
              type="password"
              placeholder="Your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="pl-10"
              required
            />
          </div>
        </div>

        <Button
          type="submit"
          className="w-full bg-primary text-white hover:bg-primary/90 transition"
        >
          Login
        </Button>
      </form>
    </div>
  )
}
