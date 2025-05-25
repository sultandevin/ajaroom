import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const rooms = [
  {
    id: 1,
    name: "Ruang Rapat 1",
    location: "Gedung A",
    capacity: 10,
    status: "Tersedia",
  },
  {
    id: 2,
    name: "Lab Komputer",
    location: "Gedung B",
    capacity: 25,
    status: "Penuh",
  },
  {
    id: 3,
    name: "Ruang Diskusi",
    location: "Gedung C",
    capacity: 8,
    status: "Tersedia",
  },
]
