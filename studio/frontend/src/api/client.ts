import type {
  CommandCollection,
  CommandSummary,
  ProjectPathResult,
  SystemStatus,
} from '../types/api'


const API_PREFIX = '/api/v1'


interface ApiErrorPayload {
  detail?: string
}



async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {

  const response = await fetch(
    `${API_PREFIX}${path}`,
    {
      ...options,

      headers: {
        'Content-Type':
          'application/json',

        ...options.headers,
      },
    },
  )


  if (!response.ok) {

    let message =
      `خطای ارتباط با سرور: ${response.status}`


    try {

      const payload =
        (
          await response.json()
        ) as ApiErrorPayload


      if (payload.detail) {

        message =
          payload.detail

      }


    } catch {

      // Non JSON response

    }


    throw new Error(
      message
    )
  }


  return (
    await response.json()
  ) as T
}





export function getSystemStatus():
Promise<SystemStatus> {

  return request<SystemStatus>(
    '/system/status'
  )
}





export function getCommands():
Promise<CommandCollection> {

  return request<CommandCollection>(
    '/commands'
  )
}





export function getCommand(
  commandName: string,
):
Promise<CommandSummary> {

  return request<CommandSummary>(
    `/commands/${encodeURIComponent(commandName)}`
  )
}





export function validateProjectPath(
  path: string,
):
Promise<ProjectPathResult> {

  return request<ProjectPathResult>(
    '/projects/validate-path',
    {
      method:'POST',

      body:JSON.stringify({
        path,
      }),
    },
  )
}



export type ImpactEntity = {

    id:string

    name:string

    kind:string

}



export type ImpactReport = {

    target_id:string

    affected_entities:ImpactEntity[]

    affected_files:number

    affected_modules:number

    affected_tests:number

    risk:string

}



export function getImpactReport(
    entityId:string,
):
Promise<ImpactReport> {

    return request<ImpactReport>(
        `/impact/${entityId}`
    )

}


export type KnowledgeSummary = {

  entities:number

  relations:number

  projects:number

  modules:number

  symbols:number

}


export type GraphNode = {

    id:string

    name:string

    kind:string

}



export type GraphEdge = {

    source:string

    target:string

    relation:string

}



export type GraphResponse = {

    nodes:GraphNode[]

    edges:GraphEdge[]

}


export type AssistantResponse = {

    answer: string

    data: Record<string, unknown>

}



export function askAssistant(
    question: string,
):
Promise<AssistantResponse> {

    return request<AssistantResponse>(
        '/assistant/ask',
        {
            method:'POST',

            body:JSON.stringify({
                question,
            }),
        },
    )

}


export function getProjectGraph():

Promise<GraphResponse> {

    return request<GraphResponse>(
        '/graph'
    )

}


export function getKnowledgeSummary():
Promise<KnowledgeSummary> {

  return request<KnowledgeSummary>(
    '/knowledge/summary'
  )

}





export function scanKnowledgeProject(
  path:string,
): Promise<KnowledgeSummary> {

  return request<KnowledgeSummary>(
    `/knowledge/scan?path=${encodeURIComponent(path)}`,
    {
      method:'POST',
    },
  )

}
