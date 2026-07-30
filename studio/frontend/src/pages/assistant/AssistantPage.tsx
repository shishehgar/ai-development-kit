import {
    useState,
} from 'react'


import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Stack,
    TextField,
    Typography,
} from '@mui/material'


import SmartToyRoundedIcon from '@mui/icons-material/SmartToyRounded'


import {
    askAssistant,
} from '../../api/client'



export default function AssistantPage(){


    const [
        question,
        setQuestion,
    ] = useState('')



    const [
        answer,
        setAnswer,
    ] = useState<string | null>(
        null
    )



    const [
        data,
        setData,
    ] = useState<Record<string, unknown> | null>(
        null
    )



    const [
        loading,
        setLoading,
    ] = useState(false)




    async function handleAsk(){


        if(!question.trim()){

            return

        }


        setLoading(true)


        try {


            const result =
                await askAssistant(
                    question
                )


            setAnswer(
                result.answer
            )


            setData(
                result.data
            )


        }

        finally {

            setLoading(false)

        }

    }





    return (

        <Stack spacing={3}>


            <Box>

                <Typography
                    variant="h4"
                >

                    AI Engineering Assistant

                </Typography>


                <Typography
                    color="text.secondary"
                >

                    پرسش درباره ساختار و معماری پروژه

                </Typography>

            </Box>




            <Card>

                <CardContent>


                    <Stack spacing={2}>


                        <TextField

                            multiline

                            minRows={3}

                            label="سؤال شما"

                            value={question}

                            onChange={
                                event =>
                                setQuestion(
                                    event.target.value
                                )
                            }

                        />



                        <Button

                            variant="contained"

                            startIcon={
                                <SmartToyRoundedIcon />
                            }

                            disabled={
                                loading
                            }

                            onClick={
                                handleAsk
                            }

                        >

                            {loading
                                ?
                                'در حال تحلیل...'
                                :
                                'ارسال سؤال'
                            }


                        </Button>


                    </Stack>


                </CardContent>


            </Card>





            {answer && (

                <Card>

                    <CardContent>


                        <Typography

                            sx={{
                                fontWeight:800,
                            }}

                        >

                            پاسخ

                        </Typography>



                        <Typography>

                            {answer}

                        </Typography>



                        {data && (

                            <Alert
                                severity="info"
                                sx={{
                                    mt:2,
                                }}
                            >

                                {JSON.stringify(
                                    data,
                                    null,
                                    2
                                )}

                            </Alert>

                        )}



                    </CardContent>


                </Card>

            )}



        </Stack>

    )

}
