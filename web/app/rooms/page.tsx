"use client"

import { Card } from "@/components/ui/card"


const rooms = [
  { id: 1, name: "Ruang Rapat 1", location: "Gedung A", capacity: 10, status: "Tersedia" },
  { id: 2, name: "Lab Komputer", location: "Gedung B", capacity: 25, status: "Penuh" },
  { id: 3, name: "Ruang Diskusi", location: "Gedung C", capacity: 8, status: "Tersedia" },
]

export default function RoomsPage() {
  return (
    <main className="min-h-screen bg-muted px-6 py-10">
      <div className="max-w-4xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-foreground mb-6">Daftar Ruangan</h1>

        {rooms.map((room) => (
          <Card
            key={room.id}
            className="p-5 border hover:shadow transition cursor-pointer"
            onClick={() => window.location.href = `/rooms/${room.id}`}
          >
            <div className="text-xl font-semibold">{room.name}</div>
            <div className="text-muted-foreground text-sm">{room.location}</div>
            <div className="mt-2 flex justify-between items-center text-sm">
              <span>Kapasitas: {room.capacity}</span>
              <span className={`font-medium ${room.status === "Tersedia" ? "text-green-600" : "text-red-600"}`}>
                {room.status}
              </span>
            </div>
          </Card>
        ))}
      </div>
    </main>
  )
}

