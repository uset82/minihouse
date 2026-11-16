import { translate, type TranslationMessage } from '../../i18n/index.js'
import {
  deleteLocalAttachment,
  storeLocalAttachment,
  streamOpenRouterMessage,
} from './openrouter-client.js'
import type {
  ApiErrorBody,
  CreateMessageRequest,
  FileObject,
  FilePurpose,
  MessageStreamEvent,
} from './types.js'

/** Build-time API origin, defaulting to https://openrouter.ai/api/v1 */
export const API_ORIGIN = __API_ORIGIN__

export type ApiErrorKind =
  /** 非 2xx 响应 */
  | 'http'
  /** 流中返回的错误帧（如等待生成超时），随后连接关闭 */
  | 'stream'
  /** 请求没有到达服务端（断网、跨域被拦截等） */
  | 'network'
  /** 流在 message_stop 之前结束 */
  | 'interrupted'
  /** 响应不符合协议（如非 SSE 响应） */
  | 'protocol'

export class ApiError extends Error {
  readonly localMessage?: TranslationMessage

  constructor(
    readonly kind: ApiErrorKind,
    message: string | TranslationMessage,
    readonly status?: number
  ) {
    super(typeof message === 'string' ? message : translate(message.key, message.params))
    this.name = 'ApiError'
    this.localMessage = typeof message === 'string' ? undefined : message
  }
}

const isErrorBody = (value: unknown): value is ApiErrorBody =>
  typeof value === 'object' &&
  value !== null &&
  'error' in value &&
  typeof (value as ApiErrorBody).error?.message === 'string'

const readErrorResponse = async (
  response: Response,
  kind: 'http' | 'protocol' = 'http',
  fallback = response.statusText
): Promise<ApiError> => {
  const text = await response.text().catch(() => '')
  let message = text || fallback
  try {
    const body: unknown = JSON.parse(text)
    if (isErrorBody(body)) {
      message = body.error.message
    }
  } catch {
    // 非 JSON 响应体直接展示原文
  }
  return new ApiError(kind, message, response.status)
}

export const request = async (url: string, init: RequestInit): Promise<Response> => {
  let response: Response
  try {
    response = await fetch(url, init)
  } catch (error) {
    if (init.signal?.aborted) {
      throw error
    }
    throw new ApiError('network', error instanceof Error ? error.message : String(error))
  }
  if (!response.ok) {
    throw await readErrorResponse(response)
  }
  return response
}

/** Validate OpenRouter API Key via GET /auth/key (zero-cost) */
export const verifyApiKey = async (apiKey: string, signal?: AbortSignal): Promise<void> => {
  await request(`${API_ORIGIN}/auth/key`, {
    method: 'GET',
    headers: { Authorization: `Bearer ${apiKey.trim()}` },
    signal,
  })
}

/**
 * Client-side attachment handler for OpenRouter Free API.
 * Reads text/Markdown/CSV/JSON files locally so they can be included in the prompt context
 * without requiring DeepSeek's proprietary /anthropic/v1/files endpoint.
 */
export const uploadFile = async (
  _apiKey: string,
  file: File,
  _purpose: FilePurpose | null,
  signal?: AbortSignal
): Promise<FileObject> => storeLocalAttachment(file, signal)

/** Remove client-side cached attachment */
export const deleteFile = async (_apiKey: string, fileId: string): Promise<void> => {
  deleteLocalAttachment(fileId)
}

/**
 * Stream chat completions via @openrouter/sdk using strictly zero-cost models (`openrouter/free` and `:free`).
 */
export async function* streamMessage(
  apiKey: string,
  body: CreateMessageRequest,
  signal: AbortSignal
): AsyncGenerator<MessageStreamEvent> {
  try {
    for await (const event of streamOpenRouterMessage(apiKey, body, signal)) {
      yield event
    }
  } catch (error) {
    if (signal.aborted) {
      throw error
    }
    if (error instanceof ApiError) {
      throw error
    }
    const msg = error instanceof Error ? error.message : String(error)
    const statusMatch = /status\s*(\d{3})|HTTP\s*(\d{3})/i.exec(msg)
    const status = statusMatch ? Number(statusMatch[1] ?? statusMatch[2]) : undefined
    throw new ApiError(status ? 'http' : 'stream', msg, status)
  }
}
