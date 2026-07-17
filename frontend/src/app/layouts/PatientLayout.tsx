import { NavLink, Outlet } from 'react-router-dom'

const navigationItems = [
  { to: '/', label: 'Hôm nay', end: true },
  { to: '/routing/prescription', label: 'Điều phối' },
  { to: '/notifications', label: 'Thông báo' },
  { to: '/support', label: 'Hỗ trợ' },
]

export function PatientLayout() {
  return (
    <div className="patient-shell">
      <header className="patient-header">
        <p className="patient-header__hospital">Bệnh viện Đa khoa TW</p>
        <h1>NHỊP VIỆN</h1>
        <p>Điều phối hành trình khám và xét nghiệm</p>
      </header>

      <main className="patient-content">
        <Outlet />
      </main>

      <nav className="bottom-navigation" aria-label="Điều hướng chính">
        {navigationItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.end}
            className={({ isActive }) =>
              isActive ? 'bottom-navigation__link is-active' : 'bottom-navigation__link'
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </div>
  )
}
