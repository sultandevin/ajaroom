"use client"

import { useParams, useRouter } from "next/navigation"
import ScheduleList from "./ScheduleList"
import { rooms } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ArrowLeft } from "lucide-react"

export default function RoomDetailPage() {
  const params = useParams()
  const router = useRouter()
  const roomId = params.id as string
  const room = rooms.find((r) => r.id === Number(roomId))

  return (
    <main className="min-h-screen bg-muted px-6 py-10">
      <div className="max-w-3xl mx-auto space-y-6">
        <Button
          variant="outline"
          onClick={() => router.back()}
          className="flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" />
          Kembali
        </Button>

        <h1 className="text-3xl font-bold text-foreground mb-2">
          Jadwal {room?.name ?? `Ruangan ${roomId}`}
        </h1>
        <p className="text-muted-foreground text-sm mb-4">
          Berikut adalah jadwal penggunaan ruangan ini.
        </p>

        <ScheduleList />
      </div>
    </main>
  )
}
