import {
  useCallback,
  useState,
} from 'react'

import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  Chip,
  Grid,
  Stack,
  Typography,
} from '@mui/material'
import HelpOutlineRoundedIcon from '@mui/icons-material/HelpOutlineRounded'

import { getCommands } from '../api/client'
import { ErrorState } from '../components/common/ErrorState'
import { LoadingState } from '../components/common/LoadingState'
import { HelpDrawer } from '../components/help/HelpDrawer'
import { useAsync } from '../hooks/useAsync'
import type { CommandSummary } from '../types/api'

const safetyLabels: Record<string, string> = {
  'read-only': 'فقط خواندنی',
  'writes-database': 'ثبت اطلاعات',
  'confirmation-required': 'نیازمند تأیید',
  unknown: 'نامشخص',
}

export function CommandsPage() {
  const [selectedCommand, setSelectedCommand] =
    useState<CommandSummary | null>(null)

  const operation = useCallback(
    () => getCommands(),
    [],
  )

  const {
    data,
    loading,
    error,
    reload,
  } = useAsync(operation)

  if (loading) {
    return <LoadingState />
  }

  if (error || !data) {
    return (
      <ErrorState
        message={error ?? 'فهرست ابزارها در دسترس نیست.'}
        onRetry={reload}
      />
    )
  }

  return (
    <>
      <Stack spacing={3}>
        <Box>
          <Typography variant="h4">
            ابزارهای AIDK
          </Typography>

          <Typography
            color="text.secondary"
            sx={{ mt: 1 }}
          >
            {data.count} قابلیت از هسته AIDK شناسایی شد.
          </Typography>
        </Box>

        <Grid container spacing={2}>
          {data.commands.map((command) => (
            <Grid
              key={command.name}
              size={{
                lg: 4,
                md: 6,
                xs: 12,
              }}
            >
              <Card
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  height: '100%',
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Stack spacing={2}>
                    <Box>
                      <Typography variant="h6">
                        {command.title_fa}
                      </Typography>

                      <Typography
                        color="text.secondary"
                        variant="caption"
                      >
                        {command.name}
                      </Typography>
                    </Box>

                    <Typography color="text.secondary">
                      {command.description_fa}
                    </Typography>

                    <Stack
                      direction="row"
                      flexWrap="wrap"
                      gap={1}
                    >
                      <Chip
                        label={
                          safetyLabels[command.safety] ??
                          command.safety
                        }
                        size="small"
                      />

                      <Chip
                        label={command.category}
                        size="small"
                        variant="outlined"
                      />
                    </Stack>
                  </Stack>
                </CardContent>

                <CardActions>
                  <Button
                    onClick={() => {
                      setSelectedCommand(command)
                    }}
                    startIcon={<HelpOutlineRoundedIcon />}
                  >
                    راهنمای کامل
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Stack>

      <HelpDrawer
        command={selectedCommand}
        onClose={() => setSelectedCommand(null)}
        open={selectedCommand !== null}
      />
    </>
  )
}
