import {
  useCallback,
  useEffect,
  useState,
} from 'react'

interface AsyncState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

interface AsyncResult<T> extends AsyncState<T> {
  reload: () => void
}

export function useAsync<T>(
  operation: () => Promise<T>,
): AsyncResult<T> {
  const [reloadToken, setReloadToken] = useState(0)

  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    loading: true,
    error: null,
  })

  const reload = useCallback(() => {
    setReloadToken((value) => value + 1)
  }, [])

  useEffect(() => {
    let active = true

    setState((current) => ({
      ...current,
      loading: true,
      error: null,
    }))

    operation()
      .then((data) => {
        if (!active) {
          return
        }

        setState({
          data,
          loading: false,
          error: null,
        })
      })
      .catch((error: unknown) => {
        if (!active) {
          return
        }

        const message =
          error instanceof Error
            ? error.message
            : 'خطای ناشناخته در دریافت اطلاعات'

        setState({
          data: null,
          loading: false,
          error: message,
        })
      })

    return () => {
      active = false
    }
  }, [operation, reloadToken])

  return {
    ...state,
    reload,
  }
}
