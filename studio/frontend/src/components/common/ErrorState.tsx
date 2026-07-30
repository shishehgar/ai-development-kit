import {
  Alert,
  Button,
  Stack,
} from '@mui/material'
import RefreshRoundedIcon from '@mui/icons-material/RefreshRounded'

interface ErrorStateProps {
  message: string
  onRetry?: () => void
}

export function ErrorState({
  message,
  onRetry,
}: ErrorStateProps) {
  return (
    <Stack spacing={2}>
      <Alert severity="error">
        {message}
      </Alert>

      {onRetry ? (
        <Button
          onClick={onRetry}
          startIcon={<RefreshRoundedIcon />}
          variant="outlined"
        >
          تلاش دوباره
        </Button>
      ) : null}
    </Stack>
  )
}
