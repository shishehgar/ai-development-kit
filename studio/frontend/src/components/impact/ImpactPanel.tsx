import {
    Alert,
    Card,
    CardContent,
    Stack,
    Typography,
} from '@mui/material'


import type {
    ImpactReport,
} from '../../api/client'



interface Props {

    report:
    ImpactReport | null

}



export function ImpactPanel(
    {
        report,
    }:Props
){


    if(!report){

        return null

    }



    return (

        <Card>

            <CardContent>

                <Stack spacing={2}>


                    <Typography
                        variant="h6"
                    >

                        Impact Analysis

                    </Typography>



                    <Alert

                        severity={
                            report.risk === "HIGH"

                            ? "error"

                            : "warning"

                        }

                    >

                        Risk:
                        {report.risk}

                    </Alert>



                    <Typography>

                        Files:
                        {report.affected_files}

                    </Typography>


                    <Typography>

                        Modules:
                        {report.affected_modules}

                    </Typography>


                    <Typography>

                        Tests:
                        {report.affected_tests}

                    </Typography>


                </Stack>


            </CardContent>


        </Card>

    )

}
