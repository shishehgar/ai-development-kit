import {
  useCallback,
} from 'react'

import {
  Alert,
  Box,
  Card,
  CardContent,
  Chip,
  Grid,
  Stack,
  Typography,
} from '@mui/material'

import CheckCircleRoundedIcon from '@mui/icons-material/CheckCircleRounded'
import FolderRoundedIcon from '@mui/icons-material/FolderRounded'
import TerminalRoundedIcon from '@mui/icons-material/TerminalRounded'

import { getSystemStatus } from '../api/client'
import { ErrorState } from '../components/common/ErrorState'
import { LoadingState } from '../components/common/LoadingState'
import { useAsync } from '../hooks/useAsync'



export function DashboardPage() {


  const operation = useCallback(
    () => getSystemStatus(),
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

        message={
          error ??
          'اطلاعات سیستم در دسترس نیست.'
        }

        onRetry={reload}

      />

    )

  }



  return (

    <Stack spacing={3}>


      <Box>

        <Typography
          variant="h4"
        >
          داشبورد
        </Typography>


        <Typography

          color="text.secondary"

          sx={{
            mt:1,
          }}

        >

          نمای کلی محیط مهندسی AIDK

        </Typography>


      </Box>



      <Alert

        icon={
          <CheckCircleRoundedIcon />
        }

        severity="success"

      >

        Backend محیط AIDK Studio فعال و آماده استفاده است.

      </Alert>



      <Grid
        container
        spacing={2}
      >


        <Grid
          size={{
            md:4,
            xs:12,
          }}
        >

          <Card>

            <CardContent>

              <Stack spacing={2}>


                <TerminalRoundedIcon
                  color="primary"
                />


                <Typography

                  color="text.secondary"

                  variant="body2"

                >

                  ابزارهای قابل استفاده

                </Typography>


                <Typography
                  variant="h4"
                >

                  {data.command_count}

                </Typography>


              </Stack>

            </CardContent>

          </Card>

        </Grid>




        <Grid
          size={{
            md:4,
            xs:12,
          }}
        >

          <Card>

            <CardContent>


              <Stack spacing={2}>


                <CheckCircleRoundedIcon
                  color="success"
                />


                <Typography

                  color="text.secondary"

                  variant="body2"

                >

                  وضعیت سیستم

                </Typography>


                <Chip

                  color="success"

                  label={data.status}

                  sx={{
                    alignSelf:'flex-start',
                  }}

                />


              </Stack>


            </CardContent>


          </Card>


        </Grid>





        <Grid
          size={{
            md:4,
            xs:12,
          }}
        >


          <Card>

            <CardContent>


              <Stack spacing={2}>


                <FolderRoundedIcon
                  color="primary"
                />


                <Typography

                  color="text.secondary"

                  variant="body2"

                >

                  نسخه Studio

                </Typography>


                <Typography
                  variant="h4"
                >

                  {data.version}

                </Typography>


              </Stack>


            </CardContent>


          </Card>


        </Grid>



      </Grid>




      <Card>

        <CardContent>


          <Typography

            gutterBottom

            sx={{
              fontWeight:800,
            }}

          >

            مسیر Workspace

          </Typography>



          <Box

            component="code"

            dir="ltr"

            sx={{

              bgcolor:'grey.100',

              borderRadius:2,

              display:'block',

              overflowX:'auto',

              p:2,

            }}

          >

            {data.workspace_root}

          </Box>



        </CardContent>


      </Card>



    </Stack>

  )

}
