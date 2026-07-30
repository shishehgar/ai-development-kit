import type { PropsWithChildren } from 'react'

import {
  AppBar,
  Box,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
} from '@mui/material'


import MenuRoundedIcon from '@mui/icons-material/MenuRounded'
import DashboardRoundedIcon from '@mui/icons-material/DashboardRounded'
import SmartToyRoundedIcon from '@mui/icons-material/SmartToyRounded'
import HelpOutlineRoundedIcon from '@mui/icons-material/HelpOutlineRounded'



const drawerWidth = 260



const navigation = [

  {
    label:'Dashboard',

    path:'/',

    icon:<DashboardRoundedIcon />,
  },


  {
    label:'AI Assistant',

    path:'/assistant',

    icon:<SmartToyRoundedIcon />,
  },

]




export function StudioLayout(
  {
    children,
  }: PropsWithChildren
) {


  return (

    <Box
      sx={{
        display:'flex',
        minHeight:'100vh',
      }}
    >


      <AppBar
        position="fixed"
        color="inherit"
      >

        <Toolbar>


          <IconButton>

            <MenuRoundedIcon />

          </IconButton>


          <Typography
            sx={{
              flexGrow:1,
              fontWeight:800,
            }}
          >

            AIDK Studio

          </Typography>



          <IconButton>

            <HelpOutlineRoundedIcon />

          </IconButton>


        </Toolbar>


      </AppBar>





      <Drawer

        variant="permanent"

        sx={{

          width:drawerWidth,

          '& .MuiDrawer-paper':{

            width:drawerWidth,

          },

        }}

      >


        <Toolbar />


        <Divider />


        <List>


          {
            navigation.map(
              item=>(

                <ListItemButton
                  key={item.path}
                  component="a"
                  href={item.path}
                >


                  <ListItemIcon>

                    {item.icon}

                  </ListItemIcon>



                  <ListItemText

                    primary={
                      item.label
                    }

                  />


                </ListItemButton>

              )
            )
          }


        </List>


      </Drawer>





      <Box

        component="main"

        sx={{

          flexGrow:1,

          p:3,

          mt:8,

        }}

      >

        {children}

      </Box>



    </Box>

  )

}
