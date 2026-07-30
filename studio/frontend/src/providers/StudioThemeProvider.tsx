import type { PropsWithChildren } from 'react'

import { CacheProvider } from '@emotion/react'
import createCache from '@emotion/cache'
import {
  CssBaseline,
  ThemeProvider,
} from '@mui/material'
import rtlPlugin from '@mui/stylis-plugin-rtl'
import { prefixer } from 'stylis'

import { studioTheme } from '../theme/theme'

const rtlCache = createCache({
  key: 'aidk-rtl',
  stylisPlugins: [prefixer, rtlPlugin],
})

export function StudioThemeProvider({
  children,
}: PropsWithChildren) {
  return (
    <CacheProvider value={rtlCache}>
      <ThemeProvider theme={studioTheme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </CacheProvider>
  )
}
