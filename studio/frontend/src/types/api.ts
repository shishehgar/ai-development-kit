export type SafetyLevel =
  | 'read-only'
  | 'writes-database'
  | 'confirmation-required'
  | 'unknown'

export interface SystemStatus {
  name: string
  version: string
  status: string
  api_prefix: string
  workspace_root: string
  command_count: number
}

export interface CommandSummary {
  name: string
  title_fa: string
  description: string
  description_fa: string
  category: string
  safety: SafetyLevel
  cli_equivalent: string
  available: boolean
}

export interface CommandCollection {
  count: number
  commands: CommandSummary[]
}

export interface ProjectPathResult {
  path: string
  exists: boolean
  is_directory: boolean
  is_git_repository: boolean
  allowed: boolean
  message: string
}
