"use client"

import { useState, useMemo } from "react"
import { Calendar } from "@/components/ui/calendar"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { CalendarDays, Clock, CheckCircle, XCircle } from "lucide-react"

const days = ["senin", "selasa", "rabu", "kamis", "jumat", "sabtu", "minggu"]

function generateSlots(startHour: number, endHour: number) {
  const slots = []
  for (let hour = startHour; hour < endHour; hour += 2) {
    const from = hour.toString().padStart(2, "0") + ":00"
    const to = (hour + 2).toString().padStart(2, "0") + ":00"
    slots.push({ time: `${from} - ${to}`, booked: false })
  }
  return slots
}

const initialSchedules: Record<string, { time: string; booked: boolean }[]> = {
  senin: generateSlots(8, 20),
  selasa: generateSlots(8, 20),
  rabu: generateSlots(8, 20),
  kamis: generateSlots(8, 20),
  jumat: generateSlots(8, 20),
  sabtu: generateSlots(8, 20),
  minggu: generateSlots(10, 18),
}

export default function ScheduleList() {
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(new Date())
  const [schedules, setSchedules] = useState(initialSchedules)

  const getDayName = (date: Date) => {
    const dayIndex = date.getDay()
    return days[dayIndex === 0 ? 6 : dayIndex - 1]
  }

  const currentDay = useMemo(() => {
    return selectedDate ? getDayName(selectedDate) : "senin"
  }, [selectedDate])

  const handleBooking = (day: string, index: number) => {
    const updated = { ...schedules }
    updated[day][index].booked = true
    setSchedules(updated)
  }

  return (
    <div className="space-y-8">
      {/* Kalender */}
      <div>
        <h2 className="text-xl font-bold text-primary mb-3 flex items-center gap-2">
          <CalendarDays className="w-5 h-5 text-primary" />
          Pilih Tanggal
        </h2>
        <Calendar
          mode="single"
          selected={selectedDate}
          onSelect={setSelectedDate}
          className="rounded-md border shadow-sm w-fit"
        />
      </div>

      {/* Jadwal */}
      <div>
        <h2 className="text-2xl font-semibold text-foreground mb-4 flex items-center gap-2">
          <Clock className="w-5 h-5 text-muted-foreground" />
          Jadwal Hari {currentDay.charAt(0).toUpperCase() + currentDay.slice(1)}
        </h2>

        <div className="space-y-3">
          {(schedules[currentDay] ?? []).map((slot, idx) => (
            <Card
              key={idx}
              className={`p-4 flex items-center justify-between border transition-all duration-200 rounded-xl shadow-sm ${
                slot.booked
                  ? "bg-red-50 border-red-200"
                  : "bg-green-50 border-green-200 hover:shadow-md hover:scale-[1.01]"
              }`}
            >
              <div className="flex items-center gap-2">
                {slot.booked ? (
                  <XCircle className="text-red-500 w-4 h-4" />
                ) : (
                  <CheckCircle className="text-green-600 w-4 h-4" />
                )}
                <span className="text-sm font-medium text-gray-700">{slot.time}</span>
              </div>

              <Button
                variant={slot.booked ? "destructive" : "default"}
                disabled={slot.booked}
                onClick={() => handleBooking(currentDay, idx)}
                className={`text-sm px-4 py-1 rounded-md transition-all ${
                  slot.booked
                    ? "bg-red-200 text-red-900 cursor-not-allowed"
                    : "bg-green-600 hover:bg-green-700 text-white"
                }`}
              >
                {slot.booked ? "Terpakai" : "Booking"}
              </Button>
            </Card>
          ))}

          {schedules[currentDay]?.length === 0 && (
            <p className="text-muted-foreground text-sm italic">
              Tidak ada jadwal untuk hari ini.
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
