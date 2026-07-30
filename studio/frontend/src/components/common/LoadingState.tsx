import {
  Box,
  CircularProgress,
  Typography,
} from '@mui/material'

interface LoadingStateProps {
  message?: string
}

export function LoadingState({
  message = 'در حال دریافت اطلاعات...',
}: LoadingStateProps) {
  return (
    <Box
      sx={{
        alignItems: 'center',
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        justifyContent: 'center',
        minHeight: 220,
      }}
    >
      <CircularProgress />

      <Typography color="text.secondary">
        {message}
      </Typography>
    </Box>
  )
}
