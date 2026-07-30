import {
  Box,
  Chip,
  Divider,
  Drawer,
  IconButton,
  Stack,
  Typography,
} from '@mui/material'
import CloseRoundedIcon from '@mui/icons-material/CloseRounded'
import TerminalRoundedIcon from '@mui/icons-material/TerminalRounded'

import type { CommandSummary } from '../../types/api'

interface HelpDrawerProps {
  open: boolean
  command: CommandSummary | null
  onClose: () => void
}

const safetyLabels: Record<string, string> = {
  'read-only': 'فقط خواندنی',
  'writes-database': 'ثبت در پایگاه داده',
  'confirmation-required': 'نیازمند تأیید',
  unknown: 'نامشخص',
}

export function HelpDrawer({
  open,
  command,
  onClose,
}: HelpDrawerProps) {
  return (
    <Drawer
      anchor="left"
      open={open}
      onClose={onClose}
      slotProps={{
        paper: {
        sx: {
          maxWidth: '100%',
          p: 3,
          width: 420,
        },
        }
      }}
    >
      <Stack spacing={3}>
        <Box
          sx={{
            alignItems: 'center',
            display: 'flex',
            justifyContent: 'space-between',
          }}
        >
          <Typography variant="h6">
            راهنمای لحظه‌ای
          </Typography>

          <IconButton
            aria-label="بستن راهنما"
            onClick={onClose}
          >
            <CloseRoundedIcon />
          </IconButton>
        </Box>

        <Divider />

        {command ? (
          <>
            <Box>
              <Typography variant="h5">
                {command.title_fa}
              </Typography>

              <Typography
                color="text.secondary"
                sx={{ mt: 1 }}
              >
                {command.description_fa}
              </Typography>
            </Box>

            <Stack
              direction="row"
              sx={{              
                  flexWrap:"wrap",
                  gap: 2
              }}
            >
              <Chip
                label={
                  safetyLabels[command.safety] ??
                  command.safety
                }
              />

              <Chip
                label={command.category}
                variant="outlined"
              />
            </Stack>

            <Box>
              <Typography
                  sx={{  
                      fontWeight:800
                  }}  
                gutterBottom
              >
                فرمان معادل
              </Typography>

              <Box
                component="code"
                dir="ltr"
                sx={{
                  alignItems: 'center',
                  bgcolor: 'grey.900',
                  borderRadius: 2,
                  color: 'common.white',
                  display: 'flex',
                  fontFamily: 'monospace',
                  gap: 1,
                  overflowX: 'auto',
                  p: 2,
                }}
              >
                <TerminalRoundedIcon fontSize="small" />
                {command.cli_equivalent}
              </Box>
            </Box>

            <Box>
              <Typography
                gutterBottom
                sx={{
                    fontWeight: 800,
                }}
              >
                وضعیت ایمنی
              </Typography>

              <Typography color="text.secondary">
                {command.safety === 'read-only'
                  ? 'این عملیات فقط اطلاعات پروژه را بررسی می‌کند و فایلی را تغییر نمی‌دهد.'
                  : 'پیش از اجرای این عملیات باید جزئیات تغییر نمایش داده و تأیید صریح دریافت شود.'}
              </Typography>
            </Box>
          </>
        ) : (
          <Typography color="text.secondary">
            برای مشاهده راهنما، یکی از ابزارهای پروژه را انتخاب کنید.
          </Typography>
        )}
      </Stack>
    </Drawer>
  )
}
