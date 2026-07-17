import { Link } from 'react-router-dom'

interface FeatureAction {
  label: string
  to: string
}

interface FeaturePlaceholderProps {
  eyebrow: string
  title: string
  description: string
  status?: 'ready' | 'planned'
  actions?: FeatureAction[]
}

export function FeaturePlaceholder({
  eyebrow,
  title,
  description,
  status = 'planned',
  actions = [],
}: FeaturePlaceholderProps) {
  return (
    <section className="feature-card">
      <div className="feature-card__heading">
        <div>
          <p className="feature-card__eyebrow">{eyebrow}</p>
          <h2>{title}</h2>
        </div>
        <span className={`status-badge status-badge--${status}`}>
          {status === 'ready' ? 'Khung đã sẵn sàng' : 'Chờ phát triển giao diện'}
        </span>
      </div>
      <p className="feature-card__description">{description}</p>
      {actions.length > 0 && (
        <div className="feature-card__actions">
          {actions.map((action, index) => (
            <Link
              key={action.to}
              className={index === 0 ? 'button button--primary' : 'button button--secondary'}
              to={action.to}
            >
              {action.label}
            </Link>
          ))}
        </div>
      )}
    </section>
  )
}
