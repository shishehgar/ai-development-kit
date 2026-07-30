import type { PropsWithChildren } from 'react'
import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import SmartToyRoundedIcon from '@mui/icons-material/SmartToyRounded'
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

import DashboardRoundedIcon from '@mui/icons-material/DashboardRounded'
import FolderRoundedIcon from '@mui/icons-material/FolderRounded'
import HelpOutlineRoundedIcon from '@mui/icons-material/HelpOutlineRounded'
import MenuRoundedIcon from '@mui/icons-material/MenuRounded'
import TerminalRoundedIcon from '@mui/icons-material/TerminalRounded'
import SmartToyRoundedIcon from '@mui/icons-material/SmartToyRounded'

const drawerWidth = 260


const navigation = [
  {
    label: 'داشبورد',
    path: '/',
    icon: <DashboardRoundedIcon />,
  },
  {
    label:"AI Assistant",
    path:"/assistant",
    icon:<SmartToyRoundedIcon />,
  },
  {
    label: 'پروژه‌ها',
    path: '/projects',
    icon: <FolderRoundedIcon />,
  },
  {
    label: 'ابزارها',
    path: '/commands',
    icon: <TerminalRoundedIcon />,
  },
]


export function StudioLayout({
  children,
}: PropsWithChildren) {

  const location = useLocation()

  const [
    mobileOpen,
    setMobileOpen,
  ] = useState(false)


  const drawerContent = (

    <Box>

      <Toolbar>

        <Box>

          <Typography
            color="primary"
            variant="h6"
            sx={{
              fontWeight: 900,
            }}
          >
            AIDK Studio
          </Typography>


          <Typography
            color="text.secondary"
            variant="caption"
          >
            محیط مهندسی بصری پروژه‌ها
          </Typography>

        </Box>

      </Toolbar>


      <Divider />


      <List
        sx={{
          px: 1,
          py: 2,
        }}
      >

        {navigation.map((item) => (

          <ListItemButton

            component={Link}

            key={item.path}

            onClick={() =>
              setMobileOpen(false)
            }

            selected={
              location.pathname === item.path
            }

            sx={{
              borderRadius: 2,
              mb: 0.5,
            }}

            to={item.path}

          >

            <ListItemIcon>
              {item.icon}
            </ListItemIcon>


            <ListItemText
              primary={item.label}
            />

          </ListItemButton>

        ))}

      </List>

    </Box>
  )


  return (

    <Box
      sx={{
        display:'flex',
        minHeight:'100vh',
      }}
    >

      <AppBar

        color="inherit"

        elevation={0}

        position="fixed"

        sx={{
          borderBottom:'1px solid',
          borderColor:'divider',

          mr:{
            md:`${drawerWidth}px`,
          },

          width:{
            md:`calc(100% - ${drawerWidth}px)`,
          },
        }}

      >

        <Toolbar>


          <IconButton

            aria-label="نمایش منو"

            onClick={() =>
              setMobileOpen(true)
            }

            sx={{
              display:{
                md:'none',
              },

              ml:1,
            }}

          >

            <MenuRoundedIcon />

          </IconButton>



          <Typography

            component="div"

            sx={{
              flexGrow:1,
              fontWeight:800,
            }}

          >
            مرکز مدیریت پروژه
          </Typography>


          <IconButton aria-label="راهنما">

            <HelpOutlineRoundedIcon />

          </IconButton>


        </Toolbar>

      </AppBar>


      <Box
        component="nav"
        sx={{
          flexShrink:{
            md:0,
          },

          width:{
            md:drawerWidth,
          },
        }}
      >

        <Drawer

          ModalProps={{
            keepMounted:true,
          }}

          onClose={() =>
            setMobileOpen(false)
          }

          open={mobileOpen}

          sx={{

            display:{
              md:'none',
              xs:'block',
            },

            '& .MuiDrawer-paper':{
              width:drawerWidth,
            },

          }}

          variant="temporary"

        >

          {drawerContent}

        </Drawer>



        <Drawer

          open

          sx={{

            display:{
              md:'block',
              xs:'none',
            },

            '& .MuiDrawer-paper':{

              borderLeft:'1px solid',

              borderRight:0,

              borderColor:'divider',

              width:drawerWidth,

            },

          }}

          variant="permanent"

        >

          {drawerContent}

        </Drawer>

      </Box>



      <Box

        component="main"

        sx={{
          flexGrow:1,
          minWidth:0,

          p:{
            md:4,
            xs:2,
          },
        }}

      >

        <Toolbar />

        {children}

      </Box>


    </Box>

  )
}
