import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import React from 'react'
import CollaborationPanel from '../components/CollaborationPanel'

describe('CollaborationPanel status handling', () => {
  it('shows error when load fails', async () => {
    const loadPrefs = vi.fn().mockRejectedValue(new Error('fail'))
    render(<CollaborationPanel loadPrefs={loadPrefs} />)
    expect(await screen.findByRole('alert')).toHaveTextContent(/error/i)
  })

  it('displays saved status after successful save', async () => {
    const loadPrefs = vi.fn().mockResolvedValue({ mode: 'solo' })
    const savePrefs = vi.fn().mockResolvedValue({})
    render(<CollaborationPanel loadPrefs={loadPrefs} savePrefs={savePrefs} />)
    await screen.findByDisplayValue('solo')
    fireEvent.click(screen.getByRole('button', { name: /save/i }))
    expect(await screen.findByRole('status')).toHaveTextContent(/saved/i)
  })
})
