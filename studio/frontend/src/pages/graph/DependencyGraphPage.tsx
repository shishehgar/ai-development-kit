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
    getImpactReport,
} from '../../api/client'


import type {
    ImpactReport,
} from '../../api/client'


import {
    ImpactPanel,
} from '../../components/impact/ImpactPanel'



export default function DependencyGraphPage(){


    const [
        nodes,
        setNodes,
    ] = useState<any[]>([])



    const [
        edges,
        setEdges,
    ] = useState<any[]>([])



    const [
        impact,
        setImpact,
    ] = useState<ImpactReport | null>(
        null
    )



    useEffect(()=>{


        getProjectGraph()
        .then(
            data=>{


                const graphNodes =
                    data.nodes.map(
                        node=>({

                            id:node.id,

                            position:{
                                x:
                                Math.random()*500,

                                y:
                                Math.random()*500,
                            },

                            data:{
                                label:
                                node.name,
                            },

                        })
                    )



                const graphEdges =
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


                setNodes(
                    graphNodes
                )


                setEdges(
                    graphEdges
                )

            }
        )


    },[])





    return (

        <div>

            <div
                style={{
                    height:'70vh',
                }}
            >

                <ReactFlow

                    nodes={
                        nodes
                    }


                    edges={
                        edges
                    }


                    onNodeClick={
                        (_, node)=>{


                            getImpactReport(
                                node.id
                            )
                            .then(
                                result=>
                                setImpact(
                                    result
                                )
                            )


                        }
                    }

                >

                    <Background />

                    <Controls />

                </ReactFlow>


            </div>



            <ImpactPanel
                report={impact}
            />


        </div>

    )

}
