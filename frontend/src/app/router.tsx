import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { PatientLayout } from './layouts/PatientLayout'
import { DashboardPage } from '../features/patient-home/pages/DashboardPage'
import { HospitalMapPage } from '../features/hospital-map/pages/HospitalMapPage'
import {
  PrescriptionPage,
  PriorityPage,
  ReservationPage,
  RouteDetailPage,
  RouteOptionsPage,
} from '../features/care-routing/pages/CareRoutingPages'
import {
  CompletedPage,
  DirectionsPage,
  TodayJourneyPage,
  WaitingPage,
} from '../features/active-journey/pages/JourneyPages'
import { NotificationsPage } from '../features/notifications/pages/NotificationsPage'
import { SupportPage } from '../features/support/pages/SupportPage'
import { NotFoundPage } from '../shared/ui/NotFoundPage'

const router = createBrowserRouter([
  {
    path: '/',
    element: <PatientLayout />,
    errorElement: <NotFoundPage />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'map', element: <HospitalMapPage /> },
      { path: 'routing/prescription', element: <PrescriptionPage /> },
      { path: 'routing/priority', element: <PriorityPage /> },
      { path: 'routing/options', element: <RouteOptionsPage /> },
      { path: 'routing/options/:routeId', element: <RouteDetailPage /> },
      { path: 'routing/reservation/:routeId', element: <ReservationPage /> },
      { path: 'journey/:journeyId', element: <TodayJourneyPage /> },
      {
        path: 'journey/:journeyId/waiting/:stepId',
        element: <WaitingPage />,
      },
      {
        path: 'journey/:journeyId/directions/:stepId',
        element: <DirectionsPage />,
      },
      { path: 'journey/:journeyId/completed', element: <CompletedPage /> },
      { path: 'notifications', element: <NotificationsPage /> },
      { path: 'support', element: <SupportPage /> },
    ],
  },
])

export function AppRouter() {
  return <RouterProvider router={router} />
}
