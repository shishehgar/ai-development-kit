import {
  useCallback,
  useState,
} from 'react'


import {
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  Stack,
  TextField,
  Typography,
} from '@mui/material'


import HubRoundedIcon from '@mui/icons-material/HubRounded'
import FolderRoundedIcon from '@mui/icons-material/FolderRounded'
import SchemaRoundedIcon from '@mui/icons-material/SchemaRounded'
import RefreshRoundedIcon from '@mui/icons-material/RefreshRounded'


import {
  getKnowledgeSummary,
  scanKnowledgeProject,
} from '../api/client'


import {
  LoadingState,
} from '../components/common/LoadingState'


import {
  ErrorState,
} from '../components/common/ErrorState'


import {
  useAsync,
} from '../hooks/useAsync'



export function DashboardPage() {


  const [
    projectPath,
    setProjectPath,
  ] = useState('.')


  const [
    scannedData,
    setScannedData,
  ] = useState<any>(null)



  const operation = useCallback(
    () =>
      getKnowledgeSummary(),
    [],
  )



  const {
    data,
    loading,
    error,
    reload,
  } = useAsync(
    operation
  )



  async function handleScan() {

    const result =
      await scanKnowledgeProject(
        projectPath
      )


    setScannedData(
      result
    )

  }



  if (loading) {

    return <LoadingState />

  }



  if (error || !data) {

    return (

      <ErrorState

        message={
          error ??
          'Knowledge unavailable'
        }

        onRetry={reload}

      />

    )

  }



  const current =
    scannedData ?? data



  const cards = [

    {
      title:'Entities',
      value:current.entities,
      icon:<HubRoundedIcon />,
    },


    {
      title:'Relations',
      value:current.relations,
      icon:<SchemaRoundedIcon />,
    },


    {
      title:'Projects',
      value:current.projects,
      icon:<FolderRoundedIcon />,
    },


    {
      title:'Modules',
      value:current.modules,
      icon:<SchemaRoundedIcon />,
    },


    {
      title:'Symbols',
      value:current.symbols,
      icon:<HubRoundedIcon />,
    },

  ]




  return (

    <Stack spacing={3}>


      <Box>

        <Typography
          variant="h4"
        >

          Knowledge Dashboard

        </Typography>


        <Typography
          color="text.secondary"
        >

          تحلیل ساختار پروژه توسط AIDK

        </Typography>


      </Box>



      <Card>

        <CardContent>

          <Stack spacing={2}>


            <Typography
              sx={{
                fontWeight:800,
              }}
            >

              Scan Project

            </Typography>



            <TextField

              label="Project Path"

              value={projectPath}

              onChange={
                (event)=>
                  setProjectPath(
                    event.target.value
                  )
              }


              slotProps={{

                htmlInput:{
                  dir:'ltr',
                },

              }}

            />



            <Button

              variant="contained"

              startIcon={
                <RefreshRoundedIcon />
              }

              onClick={
                handleScan
              }

            >

              Scan

            </Button>


          </Stack>


        </CardContent>

      </Card>





      <Grid
        container
        spacing={2}
      >

        {
          cards.map(
            (card)=>(

              <Grid

                key={card.title}

                size={{
                  md:4,
                  xs:12,
                }}

              >

                <Card>

                  <CardContent>

                    <Stack spacing={2}>

                      {card.icon}


                      <Typography
                        color="text.secondary"
                      >

                        {card.title}

                      </Typography>


                      <Typography
                        variant="h3"
                      >

                        {card.value}

                      </Typography>


                    </Stack>


                  </CardContent>


                </Card>


              </Grid>

            )
          )
        }


      </Grid>


    </Stack>

  )

}
