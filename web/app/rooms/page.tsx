"use client"

import { Card } from "@/components/ui/card"
import { useRouter } from "next/navigation"
import { Building, LayoutPanelLeft, MapPin, Users } from "lucide-react"
import { rooms } from "@/lib/utils"

export default function RoomsPage() {
  const router = useRouter()

  return (
    <main className="min-h-screen bg-muted px-6 py-10">
      <div className="max-w-4xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-foreground mb-2 flex items-center gap-2">
          <Building className="w-6 h-6 text-primary" />
          Daftar Ruangan
        </h1>
        <p className="text-muted-foreground text-sm mb-6">
          Klik ruangan di bawah untuk melihat jadwal dan melakukan booking.
        </p>

        {rooms.map((room) => (
          <Card
            key={room.id}
            className={`p-5 border rounded-xl transition-all duration-200 cursor-pointer hover:shadow-lg hover:scale-[1.01] ${
              room.status === "Tersedia"
                ? "bg-green-50 border-green-200"
                : "bg-red-50 border-red-200"
            }`}
            onClick={() => router.push(`/rooms/${room.id}`)}
          >
            <div className="text-xl font-semibold mb-2 flex items-center gap-2">
              <LayoutPanelLeft className="w-5 h-5 text-muted-foreground" />
              {room.name}
            </div>

            <div className="flex items-center text-sm text-muted-foreground gap-2 mb-2">
              <MapPin className="w-4 h-4" />
              <span>{room.location}</span>
            </div>

            <div className="flex justify-between items-center text-sm font-medium">
              <div className="flex items-center gap-2">
                <Users className="w-4 h-4 text-gray-600" />
                <span>Kapasitas: {room.capacity} orang</span>
              </div>

              <span
                className={`px-2 py-1 rounded-full text-xs font-semibold ${
                  room.status === "Tersedia"
                    ? "bg-green-600 text-white"
                    : "bg-red-600 text-white"
                }`}
              >
                {room.status}
              </span>
            </div>
          </Card>
        ))}
      </div>
    </main>
  )
}
