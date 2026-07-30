import {
  useState,
} from 'react'

import type {
  FormEvent,
} from 'react'


import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Stack,
  TextField,
  Typography,
} from '@mui/material'


import FolderOpenRoundedIcon from '@mui/icons-material/FolderOpenRounded'


import { validateProjectPath } from '../api/client'

import type {
  ProjectPathResult,
} from '../types/api'



export function ProjectsPage() {


  const [
    path,
    setPath,
  ] = useState('')


  const [
    result,
    setResult,
  ] = useState<ProjectPathResult | null>(
    null
  )


  const [
    loading,
    setLoading,
  ] = useState(false)


  const [
    error,
    setError,
  ] = useState<string | null>(
    null
  )



  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {

    event.preventDefault()


    setLoading(true)

    setError(null)

    setResult(null)



    try {

      const response =
        await validateProjectPath(
          path
        )


      setResult(response)


    } catch (requestError: unknown) {


      setError(

        requestError instanceof Error

          ? requestError.message

          : 'اعتبارسنجی پروژه انجام نشد.'

      )


    } finally {


      setLoading(false)


    }

  }




  return (

    <Stack spacing={3}>


      <Box>


        <Typography
          variant="h4"
        >

          مدیریت پروژه‌ها

        </Typography>



        <Typography

          color="text.secondary"

          sx={{
            mt:1,
          }}

        >

          مسیر یک پروژه موجود را برای بررسی وارد کنید.

        </Typography>


      </Box>




      <Card>

        <CardContent>


          <Box

            component="form"

            onSubmit={handleSubmit}

          >

            <Stack spacing={2}>


              <TextField

                fullWidth

                label="مسیر پروژه"

                onChange={(event) => {

                  setPath(
                    event.target.value
                  )

                }}

                placeholder="/home/ubuntu/my_services/projects/example"


                slotProps={{

                  htmlInput:{

                    dir:'ltr',

                  },

                }}


                value={path}

              />



              <Button


                disabled={
                  loading ||
                  path.trim().length === 0
                }


                startIcon={

                  loading

                    ? (
                      <CircularProgress
                        size={18}
                      />
                    )

                    : (
                      <FolderOpenRoundedIcon />
                    )

                }


                type="submit"

                variant="contained"


              >

                بررسی مسیر پروژه

              </Button>


            </Stack>


          </Box>


        </CardContent>


      </Card>





      {error ? (

        <Alert severity="error">

          {error}

        </Alert>

      ) : null}





      {result ? (

        <Alert

          severity={
            result.allowed
              ? 'success'
              : 'warning'
          }

        >

          <Stack spacing={1}>


            <Typography

              sx={{
                fontWeight:800,
              }}

            >

              {result.message}

            </Typography>



            <Typography

              component="code"

              dir="ltr"

              sx={{
                overflowWrap:'anywhere',
              }}

            >

              {result.path}

            </Typography>




            <Stack

              direction="row"

              sx={{

                flexWrap:'wrap',

                gap:1,

              }}

            >


              <Chip

                label={

                  result.exists

                    ? 'مسیر موجود است'

                    : 'مسیر موجود نیست'

                }

                size="small"

              />



              <Chip

                label={

                  result.is_git_repository

                    ? 'مخزن Git'

                    : 'بدون Git'

                }

                size="small"

              />



            </Stack>



          </Stack>


        </Alert>


      ) : null}


    </Stack>

  )

}
