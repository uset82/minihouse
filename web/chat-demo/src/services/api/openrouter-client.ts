import { OpenRouter } from '@openrouter/sdk'
import type {
  AssistantBlockParam,
  CreateMessageRequest,
  FileObject,
  MessageParam,
  MessageStreamEvent,
} from './types.js'

/**
 * Default zero-cost models available on OpenRouter.
 * `openrouter/free` automatically routes to available free models supporting the requested capabilities.
 */
export const DEFAULT_FREE_MODELS = [
  {
    id: 'openrouter/free',
    label: 'OpenRouter Free Router (Auto Zero-Cost)',
  },
  {
    id: 'deepseek/deepseek-r1:free',
    label: 'DeepSeek R1 (Free · Reasoning)',
  },
  {
    id: 'deepseek/deepseek-chat-v3-0324:free',
    label: 'DeepSeek V3 0324 (Free · Chat)',
  },
  {
    id: 'deepseek/deepseek-chat:free',
    label: 'DeepSeek Chat (Free)',
  },
  {
    id: 'meta-llama/llama-3.3-70b-instruct:free',
    label: 'Llama 3.3 70B Instruct (Free)',
  },
  {
    id: 'qwen/qwen3-235b-a22b:free',
    label: 'Qwen 3 235B A22B (Free)',
  },
] as const

export type FreeModelOption = {
  id: string
  label: string
}

/**
 * MiniHouse System Prompt enforcing PROJECT.md and rules.md (especially Rule 3 & Rule 5).
 */
export const MINIHOUSE_SYSTEM_PROMPT = [
  'You are the MiniHouse Technical & Documentary Assistant, powered by OpenRouter Free API (@openrouter/sdk) and DeepSeek.',
  'MiniHouse is a transportable 6 × 3 m modular house built with a primary steel chassis and reclaimed wood envelope.',
  'CRITICAL PROJECT RULES (rules.md):',
  '1. Always distinguish verification states for any dimension, load, or calculation: [CONCEPTUAL], [CALCULADO], [ENSAYADO], or [LIBERADO PARA FABRICACIÓN].',
  '2. The 3,000 kg mass, q = 2.4525 kN/m per纵beam, and EI = 1.68 MN·m² values in the reference report (giving 24.63 mm deflection at ends and 1.49 mm with 1.2 m inset supports) are a HYPOTHETICAL NUMERICAL EXAMPLE ([CONCEPTUAL]), never the real approved mass or support layout.',
  '3. Use millimeters (mm) for workshop dimensions and declare coordinate axes, units, and assumptions explicitly.',
].join('\n')

/** Dynamic set of verified zero-cost model IDs synced from OpenRouter /api/v1/models */
const verifiedFreeModelIds = new Set<string>(DEFAULT_FREE_MODELS.map((m) => m.id))

/** Client-side in-memory store for uploaded attachment text/data URLs so free models can read attached files */
const localAttachmentStore = new Map<
  string,
  { filename: string; mimeType: string; content: string; isImage: boolean }
>()

export interface OpenRouterCatalogModel {
  id: string
  name?: string
  pricing?: {
    prompt?: string | number
    completion?: string | number
    request?: string | number
  }
}

/**
 * Returns true if and only if the model is `openrouter/free`, ends with `:free`,
 * or has explicit $0 prompt, completion, and request pricing.
 */
export const isFreeOpenRouterModel = (model: OpenRouterCatalogModel): boolean => {
  if (!model || typeof model.id !== 'string') {
    return false
  }
  if (model.id === 'openrouter/free' || model.id.endsWith(':free')) {
    return true
  }
  if (!model.pricing) {
    return false
  }
  const prompt = Number(model.pricing.prompt ?? NaN)
  const completion = Number(model.pricing.completion ?? NaN)
  const request = Number(model.pricing.request ?? 0)
  return (
    Number.isFinite(prompt) &&
    Number.isFinite(completion) &&
    prompt === 0 &&
    completion === 0 &&
    request === 0
  )
}

/**
 * Enforces that only free OpenRouter models can be called.
 * Throws if a paid model ID is passed.
 */
export const assertFreeOpenRouterModel = (
  modelId: string,
  extraAllowedIds?: ReadonlySet<string>
): void => {
  const allowed =
    modelId === 'openrouter/free' ||
    modelId.endsWith(':free') ||
    verifiedFreeModelIds.has(modelId) ||
    (extraAllowedIds?.has(modelId) ?? false)

  if (!allowed) {
    throw new Error(
      `Blocked non-free OpenRouter model "${modelId}". Only "openrouter/free" and ":free" zero-cost models are allowed.`
    )
  }
}

/**
 * Maps legacy DeepSeek model names (like `deepseek-flash` or `deepseek-v4-pro`) or user selection
 * to a verified free OpenRouter model ID.
 */
export const resolveFreeModelId = (requestedModel: string | undefined, thinking: boolean): string => {
  if (!requestedModel || requestedModel === 'deepseek-flash' || requestedModel === 'deepseek-v4-pro') {
    return thinking ? 'deepseek/deepseek-r1:free' : 'openrouter/free'
  }
  if (requestedModel === 'openrouter/free' && thinking) {
    return 'openrouter/free'
  }
  assertFreeOpenRouterModel(requestedModel)
  return requestedModel
}

/**
 * Fetches live free models from OpenRouter (`GET https://openrouter.ai/api/v1/models`)
 * and updates the verified free model registry.
 */
export const fetchFreeOpenRouterModels = async (
  fetchImpl: typeof fetch = fetch,
  signal?: AbortSignal
): Promise<FreeModelOption[]> => {
  const response = await fetchImpl('https://openrouter.ai/api/v1/models', {
    method: 'GET',
    headers: { Accept: 'application/json' },
    signal,
  })
  if (!response.ok) {
    throw new Error(`OpenRouter models request failed with HTTP ${response.status}`)
  }
  const json = (await response.json()) as { data?: OpenRouterCatalogModel[] }
  const rawModels = Array.isArray(json.data) ? json.data : []
  const freeModels = rawModels.filter(isFreeOpenRouterModel)

  const options: FreeModelOption[] = [...DEFAULT_FREE_MODELS]
  const seen = new Set(options.map((o) => o.id))

  for (const model of freeModels) {
    verifiedFreeModelIds.add(model.id)
    if (!seen.has(model.id)) {
      seen.add(model.id)
      options.push({
        id: model.id,
        label: model.name ? `${model.name} (${model.id})` : model.id,
      })
    }
  }
  return options
}

/**
 * Stores a file locally in memory so its text content can be injected into OpenRouter messages
 * without requiring DeepSeek's proprietary `/anthropic/v1/files` endpoint.
 */
export const storeLocalAttachment = async (
  file: File,
  signal?: AbortSignal
): Promise<FileObject> => {
  signal?.throwIfAborted()
  const id = `local_file_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`
  const mimeType = file.type || 'text/plain'
  const isImage = mimeType.startsWith('image/')

  let content = ''
  if (isImage) {
    content = `[Attached Image: ${file.name} (${mimeType}, ${file.size} bytes)]`
  } else {
    try {
      const rawText = await file.text()
      const maxChars = 32_000
      content =
        rawText.length > maxChars
          ? `${rawText.slice(0, maxChars)}\n... [truncated ${rawText.length - maxChars} chars]`
          : rawText
    } catch {
      content = `[Attached File: ${file.name} (${file.size} bytes)]`
    }
  }

  localAttachmentStore.set(id, {
    filename: file.name,
    mimeType,
    content,
    isImage,
  })

  return {
    id,
    type: 'file',
    size_bytes: file.size,
    created_at: new Date().toISOString(),
    filename: file.name,
    mime_type: mimeType,
  }
}

export const deleteLocalAttachment = (fileId: string): void => {
  localAttachmentStore.delete(fileId)
}

const assistantBlocksToText = (blocks: AssistantBlockParam[]): string =>
  blocks
    .map((block) => {
      if (block.type === 'text') {
        return block.text
      }
      return ''
    })
    .filter(Boolean)
    .join('\n\n')

export type OpenRouterSdkMessage = {
  role: 'system' | 'user' | 'assistant'
  content: string
}

/**
 * Converts `chat-demo` internal `MessageParam[]` into OpenRouter SDK `messages`.
 */
export const toOpenRouterMessages = (
  system: string,
  messages: MessageParam[]
): OpenRouterSdkMessage[] => {
  const result: OpenRouterSdkMessage[] = []
  const systemText = [MINIHOUSE_SYSTEM_PROMPT, system.trim()].filter(Boolean).join('\n\n')
  if (systemText) {
    result.push({ role: 'system', content: systemText })
  }

  let pendingReminder = ''
  for (const msg of messages) {
    if (msg.role === 'latest_reminder') {
      pendingReminder = msg.content.trim()
      continue
    }
    if (msg.role === 'user') {
      let userText = ''
      if (typeof msg.content === 'string') {
        userText = msg.content
      } else {
        const parts: string[] = []
        for (const block of msg.content) {
          if (block.type === 'text') {
            parts.push(block.text)
          } else if (block.type === 'document' || block.type === 'image') {
            const stored = localAttachmentStore.get(block.source.file_id)
            if (stored) {
              parts.push(
                stored.isImage
                  ? stored.content
                  : `--- File: ${stored.filename} ---\n${stored.content}\n--- End File ---`
              )
            }
          }
        }
        userText = parts.join('\n\n')
      }
      if (pendingReminder) {
        userText = `${pendingReminder}\n\n${userText}`
        pendingReminder = ''
      }
      result.push({ role: 'user', content: userText })
    } else if (msg.role === 'assistant') {
      const text = assistantBlocksToText(msg.content)
      if (text) {
        result.push({ role: 'assistant', content: text })
      }
    }
  }

  return result
}

const deriveTitleFromMessages = (messages: MessageParam[]): string | undefined => {
  for (const msg of messages) {
    if (msg.role === 'user') {
      const raw =
        typeof msg.content === 'string'
          ? msg.content
          : msg.content
              .filter((b): b is { type: 'text'; text: string } => b.type === 'text')
              .map((b) => b.text)
              .join(' ')
      const clean = raw.replace(/\s+/g, ' ').trim()
      if (clean) {
        return clean.length > 36 ? `${clean.slice(0, 36)}...` : clean
      }
    }
  }
  return undefined
}

export interface OpenRouterSdkLike {
  chat: {
    send: (
      request: {
        httpReferer?: string
        appTitle?: string
        chatRequest: {
          model: string
          messages: OpenRouterSdkMessage[]
          stream: true
          reasoning?: { enabled?: boolean }
        }
      },
      options?: { signal?: AbortSignal }
    ) => Promise<AsyncIterable<unknown>>
  }
}

/**
 * Streams a chat completion from OpenRouter using `@openrouter/sdk` and converts
 * the SSE chunks into `chat-demo` `MessageStreamEvent` objects.
 */
export async function* streamOpenRouterMessage(
  apiKey: string,
  body: CreateMessageRequest,
  signal: AbortSignal,
  sdkOverride?: OpenRouterSdkLike
): AsyncGenerator<MessageStreamEvent> {
  const thinkingEnabled = body.thinking?.type === 'enabled'
  const resolvedModel = resolveFreeModelId(body.model, thinkingEnabled)
  assertFreeOpenRouterModel(resolvedModel)

  const referer =
    typeof window !== 'undefined' && window.location?.origin
      ? window.location.origin
      : 'https://minihouse.local'
  const appTitle = 'MiniHouse 6x3m Web Assistant'

  const client: OpenRouterSdkLike =
    sdkOverride ??
    new OpenRouter({
      apiKey: apiKey.trim(),
      httpReferer: referer,
      appTitle,
    })

  const openRouterMessages = toOpenRouterMessages(body.system, body.messages)

  const stream = await client.chat.send(
    {
      httpReferer: referer,
      appTitle,
      chatRequest: {
        model: resolvedModel,
        messages: openRouterMessages,
        stream: true,
        ...(thinkingEnabled ? { reasoning: { enabled: true } } : {}),
      },
    },
    { signal }
  )

  const messageId = `or_${Date.now()}`
  yield {
    type: 'message_start',
    message: {
      id: messageId,
      model: resolvedModel,
      usage: {
        input_tokens: 0,
        cache_creation_input_tokens: 0,
        cache_read_input_tokens: 0,
        output_tokens: 0,
      },
    },
  }

  let currentBlockIndex = -1
  let activeBlockType: 'thinking' | 'text' | null = null
  let inputTokens = 0
  let outputTokens = 0

  for await (const rawChunk of stream) {
    if (signal.aborted) {
      break
    }

    const chunk = rawChunk as {
      error?: { message?: string; code?: number }
      choices?: Array<{
        delta?: {
          content?: string | null
          reasoning?: string | null
          reasoning_content?: string | null
          refusal?: string | null
        }
      }>
      usage?: {
        promptTokens?: number
        completionTokens?: number
        prompt_tokens?: number
        completion_tokens?: number
      }
    }

    if (chunk.error?.message) {
      throw new Error(chunk.error.message)
    }

    if (chunk.usage) {
      inputTokens = chunk.usage.promptTokens ?? chunk.usage.prompt_tokens ?? inputTokens
      outputTokens = chunk.usage.completionTokens ?? chunk.usage.completion_tokens ?? outputTokens
    }

    const delta = chunk.choices?.[0]?.delta
    if (!delta) {
      continue
    }

    const reasoningChunk = delta.reasoning ?? delta.reasoning_content
    if (typeof reasoningChunk === 'string' && reasoningChunk.length > 0) {
      if (activeBlockType !== 'thinking') {
        if (activeBlockType !== null) {
          yield { type: 'content_block_stop', index: currentBlockIndex }
        }
        currentBlockIndex += 1
        activeBlockType = 'thinking'
        yield {
          type: 'content_block_start',
          index: currentBlockIndex,
          content_block: {
            type: 'thinking',
            thinking: '',
            signature: messageId,
          },
        }
      }
      yield {
        type: 'content_block_delta',
        index: currentBlockIndex,
        delta: {
          type: 'thinking_delta',
          thinking: reasoningChunk,
        },
      }
    }

    if (typeof delta.content === 'string' && delta.content.length > 0) {
      if (activeBlockType !== 'text') {
        if (activeBlockType !== null) {
          yield { type: 'content_block_stop', index: currentBlockIndex }
        }
        currentBlockIndex += 1
        activeBlockType = 'text'
        yield {
          type: 'content_block_start',
          index: currentBlockIndex,
          content_block: {
            type: 'text',
            text: '',
          },
        }
      }
      yield {
        type: 'content_block_delta',
        index: currentBlockIndex,
        delta: {
          type: 'text_delta',
          text: delta.content,
        },
      }
    }
  }

  if (activeBlockType !== null) {
    yield { type: 'content_block_stop', index: currentBlockIndex }
  }

  const autoTitle = body.title?.enabled ? deriveTitleFromMessages(body.messages) : undefined

  yield {
    type: 'message_delta',
    delta: {
      stop_reason: 'end_turn',
      stop_sequence: null,
      ...(autoTitle ? { title: autoTitle } : {}),
    },
    usage: {
      input_tokens: inputTokens,
      cache_creation_input_tokens: 0,
      cache_read_input_tokens: 0,
      output_tokens: outputTokens,
    },
  }

  yield { type: 'message_stop' }
}
