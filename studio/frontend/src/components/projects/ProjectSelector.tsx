import {
  useEffect,
  useState,
} from 'react'


import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  CircularProgress,
  Box,
} from '@mui/material'


import {
  getProjects,
} from '../../api/client'


import type {
  ProjectRegistryItem,
} from '../../types/api'



interface ProjectSelectorProps {

  value: string | null

  onChange: (
    projectId: string
  ) => void

}



export default function ProjectSelector(
  {
    value,
    onChange,
  }: ProjectSelectorProps
) {


  const [
    projects,
    setProjects,
  ] = useState<ProjectRegistryItem[]>([])



  const [
    loading,
    setLoading,
  ] = useState(true)



  useEffect(

    () => {

      async function load(){

        try {

          const result =
            await getProjects()

          setProjects(
            result
          )


          if(
            !value &&
            result.length > 0
          ){

            onChange(
              result[0].id
            )

          }


        }
        finally {

          setLoading(false)

        }

      }


      load()

    },

    [
      value,
      onChange,
    ]

  )



  if(loading){

    return (

      <Box>

        <CircularProgress
          size={24}
        />

      </Box>

    )

  }



  return (

    <FormControl
      fullWidth
    >

      <InputLabel>
        پروژه فعال
      </InputLabel>


      <Select

        value={
          value ?? ''
        }

        label="پروژه فعال"

        onChange={
          event =>
          onChange(
            event.target.value
          )
        }

      >

        {
          projects.map(
            project => (

              <MenuItem

                key={
                  project.id
                }

                value={
                  project.id
                }

              >

                {
                  project.name
                }

              </MenuItem>

            )
          )
        }


      </Select>


    </FormControl>

  )

}
