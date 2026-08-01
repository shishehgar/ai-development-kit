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


import ProjectSelector
    from '../../components/projects/ProjectSelector'



export default function AssistantPage(){


    const [
        question,
        setQuestion,
    ] = useState('')

    const [
        project,
        setProject,
    ] = useState(
        'ai-development-kit'
    )




    const [
        answer,
        setAnswer,
    ] = useState<string | null>(
        null
    )


    const [
        provider,
        setProvider,
    ] = useState<string | null>(
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
                    question,
                    project
                )


            setAnswer(
                result.answer
            )


            setProvider(
                result.provider
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


                        <ProjectSelector

                            value={project}

                            onChange={
                                setProject
                            }

                        />



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

                            {
                                loading
                                ?
                                'در حال تحلیل...'
                                :
                                'ارسال سؤال'
                            }

                        </Button>


                    </Stack>


                </CardContent>

            </Card>



            {
                answer &&

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



                        {
                            provider &&

                            <Alert
                                severity="info"
                                sx={{
                                    mt:2,
                                }}
                            >

                                Provider: {provider}

                            </Alert>

                        }


                    </CardContent>

                </Card>

            }


        </Stack>

    )

}
