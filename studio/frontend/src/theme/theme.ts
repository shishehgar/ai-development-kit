import { createTheme } from '@mui/material/styles'

export const studioTheme = createTheme({
  direction: 'rtl',

  palette: {
    mode: 'light',

    primary: {
      main: '#176B87',
    },

    secondary: {
      main: '#2D9596',
    },

    background: {
      default: '#F4F7FA',
      paper: '#FFFFFF',
    },
  },

  typography: {
    fontFamily: [
      'Vazirmatn',
      'Tahoma',
      'Arial',
      'sans-serif',
    ].join(','),

    h1: {
      fontWeight: 800,
    },

    h2: {
      fontWeight: 800,
    },

    h3: {
      fontWeight: 700,
    },

    button: {
      fontWeight: 700,
    },
  },

  shape: {
    borderRadius: 12,
  },

  components: {
    MuiButton: {
      defaultProps: {
        disableElevation: true,
      },

      styleOverrides: {
        root: {
          minHeight: 40,
          textTransform: 'none',
        },
      },
    },

    MuiCard: {
      styleOverrides: {
        root: {
          border: '1px solid rgba(15, 23, 42, 0.08)',
          boxShadow: '0 8px 28px rgba(15, 23, 42, 0.06)',
        },
      },
    },
  },
})
