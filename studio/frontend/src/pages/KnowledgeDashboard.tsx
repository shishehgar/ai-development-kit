import { useEffect, useState } from "react";


type Summary = {

    entities: number;

    relations: number;

    projects: number;

    modules: number;

    symbols: number;
};



export default function KnowledgeDashboard() {

    const [
        summary,
        setSummary
    ] = useState<Summary | null>(
        null
    );


    useEffect(() => {

        fetch(
            "/knowledge/summary"
        )
        .then(
            response =>
                response.json()
        )
        .then(
            data =>
                setSummary(data)
        );

    }, []);



    if (!summary) {

        return (
            <div>
                Loading Knowledge...
            </div>
        );
    }



    return (

        <div
            style={{
                padding: "24px"
            }}
        >

            <h1>
                Knowledge Dashboard
            </h1>


            <div>

                <p>
                    Entities:
                    {summary.entities}
                </p>


                <p>
                    Relations:
                    {summary.relations}
                </p>


                <p>
                    Projects:
                    {summary.projects}
                </p>


                <p>
                    Modules:
                    {summary.modules}
                </p>


                <p>
                    Symbols:
                    {summary.symbols}
                </p>

            </div>

        </div>
    );
}
