import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface RoomDetailProps {
  params: {
    id: string
  }
}

const schedules = [
  { time: "08:00 - 10:00", booked: true },
  { time: "10:00 - 12:00", booked: false },
  { time: "13:00 - 15:00", booked: false },
  { time: "15:00 - 17:00", booked: true },
]

export default async function RoomDetailPage({ params }: RoomDetailProps) {
  const { id: roomId } = await params

  return (
    <main className="min-h-screen bg-muted px-6 py-10">
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-foreground mb-2">Jadwal Ruangan #{roomId}</h1>
        <p className="text-muted-foreground mb-6">Berikut adalah jadwal pemakaian untuk hari ini:</p>

        <div className="space-y-3">
          {schedules.map((slot, index) => (
            <Card key={index} className="p-4 flex items-center justify-between">
              <span className="text-sm">{slot.time}</span>
              <Button variant={slot.booked ? "destructive" : "default"} disabled={slot.booked}>
                {slot.booked ? "Terpakai" : "Booking"}
              </Button>
            </Card>
          ))}
        </div>
      </div>
    </main>
  )
}
