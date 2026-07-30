import {
    useEffect,
    useState,
} from 'react'


import ReactFlow, {

    Background,

    Controls,

} from 'reactflow'


import 'reactflow/dist/style.css'


import {
    getProjectGraph,
} from '../../api/client'


import {
    useState,
} from "react"


import {
    getImpactReport,
} from "../../api/client"


import {
    ImpactPanel,
} from "../../components/impact/ImpactPanel"

export default function DependencyGraphPage(){

    const [
        elements,
        setElements,
    ] = useState<any[]>([])


    const [
        impact,
        setImpact
    ] = useState(null)

    useEffect(()=>{


        getProjectGraph()
        .then(data=>{


            const nodes =
                data.nodes.map(
                    node=>({

                        id:node.id,

                        position:{
                            x:Math.random()*500,
                            y:Math.random()*500,
                        },

                        data:{
                            label:
                            node.name
                        }

                    })
                )



            const edges =
                data.edges.map(
                    edge=>({

                        id:
                        `${edge.source}-${edge.target}`,

                        source:
                        edge.source,

                        target:
                        edge.target,

                        label:
                        edge.relation,

                    })
                )


            setElements(
                [
                    ...nodes,
                    ...edges,
                ]
            )


        })


    },[])



    return (

        <div
            style={{
                height:'80vh'
            }}
        >

            <ReactFlow
                nodes={
                    elements.filter(
                        item=>item.position
                    )
                }

                edges={
                    elements.filter(
                        item=>item.source
                    )
                }
                
                onNodeClick={
                    (_,node)=>{

                        getImpactReport(
                            node.id
                        )
                        .then(
                            result =>
                            setImpact(result)
                        )

                    }
                }
            >

                <Background />

                <Controls />

            </ReactFlow>

        </div>

    )

}
