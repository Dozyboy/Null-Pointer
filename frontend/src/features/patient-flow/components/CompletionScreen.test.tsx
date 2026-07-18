/* @vitest-environment jsdom */

import '@testing-library/jest-dom/vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { CompletionScreen } from './CompletionScreen'

describe('CompletionScreen', () => {
  it('cho phép quay lại màn hình chính', () => {
    const onBackToDashboard = vi.fn()

    render(
      <CompletionScreen
        onShowDirections={() => undefined}
        onBackToDashboard={onBackToDashboard}
      />,
    )

    fireEvent.click(screen.getByRole('button', { name: 'Quay lại màn hình chính' }))

    expect(onBackToDashboard).toHaveBeenCalledOnce()
  })
})
