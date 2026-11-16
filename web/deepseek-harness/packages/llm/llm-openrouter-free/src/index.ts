import { OpenRouter } from '@openrouter/sdk'

/**
 * Curated default free models on OpenRouter.
 * Includes the intelligent zero-cost router (`openrouter/free`) and `:free` DeepSeek/Llama variants.
 */
export const CURATED_FREE_MODELS = [
  'openrouter/free',
  'deepseek/deepseek-r1:free',
  'deepseek/deepseek-chat-v3-0324:free',
  'deepseek/deepseek-chat:free',
  'meta-llama/llama-3.3-70b-instruct:free',
  'qwen/qwen3-235b-a22b:free',
] as const

export interface OpenRouterModelDescriptor {
  id: string
  name: string
  context_length?: number
  pricing?: {
    prompt?: string | number
    completion?: string | number
    request?: string | number
    image?: string | number
  }
}

export interface DshOpenRouterFreeConfig {
  /** Environment variable holding the OpenRouter API key (default: OPENROUTER_API_KEY) */
  apiKeyEnv?: string
  /** Optional explicit API key override */
  apiKey?: string
  /** Default free model ID (default: 'openrouter/free') */
  defaultModel?: string
  /** HTTP-Referer header for OpenRouter app attribution */
  httpReferer?: string
  /** X-Title header for OpenRouter app attribution */
  appTitle?: string
  /** Inject MiniHouse traceability & structural status rules into system prompt */
  enforceMiniHouseRules?: boolean
}

export interface DshChatMessage {
  role: 'system' | 'user' | 'assistant'
  content: string
}

export interface DshStreamRequest {
  model?: string
  system?: string
  messages: DshChatMessage[]
  signal?: AbortSignal
}

export type DshStreamEvent =
  | { type: 'thinking_delta'; text: string }
  | { type: 'text_delta'; text: string }
  | { type: 'done'; model: string; usage?: { inputTokens: number; outputTokens: number } }

export const MINIHOUSE_HARNESS_SYSTEM_RULES = [
  'Eres el asistente de ingeniería y documentación del proyecto MiniHouse (módulo transportable de 6 × 3 m en acero y madera recuperada).',
  'Regla obligatoria (rules.md #5): Distingue siempre entre estado [CONCEPTUAL], [CALCULADO], [ENSAYADO] y [LIBERADO PARA FABRICACIÓN].',
  'El caso de 3 000 kg, q = 2,4525 kN/m y EI = 1,68 MN·m² del informe es un ejemplo numérico hipotético [CONCEPTUAL], nunca una masa o geometría aprobada.',
].join('\n')

/**
 * Checks whether an OpenRouter model entry is strictly zero-cost ($0 prompt and $0 completion).
 */
export function isZeroCostModel(model: OpenRouterModelDescriptor): boolean {
  if (model.id === 'openrouter/free' || model.id.endsWith(':free')) {
    return true
  }
  if (!model.pricing) {
    return false
  }
  const promptCost = Number(model.pricing.prompt ?? NaN)
  const completionCost = Number(model.pricing.completion ?? NaN)
  const requestCost = Number(model.pricing.request ?? 0)
  return (
    Number.isFinite(promptCost) &&
    Number.isFinite(completionCost) &&
    promptCost === 0 &&
    completionCost === 0 &&
    requestCost === 0
  )
}

/**
 * Throws an error if a requested model ID is not a verified zero-cost OpenRouter model.
 * Prevents accidental fallback or routing to paid models.
 */
export function assertFreeModelId(modelId: string, dynamicFreeCatalog?: ReadonlySet<string>): void {
  const allowed =
    modelId === 'openrouter/free' ||
    modelId.endsWith(':free') ||
    (dynamicFreeCatalog?.has(modelId) ?? false)

  if (!allowed) {
    throw new Error(
      `[dsh-llm-openrouter-free] Blocked non-free model "${modelId}". Only "openrouter/free" or ":free" zero-cost models are allowed.`
    )
  }
}

/**
 * Fetches the live OpenRouter model catalog and filters strictly for zero-cost models.
 */
export async function fetchOpenRouterFreeCatalog(
  fetchImpl: typeof fetch = fetch,
  signal?: AbortSignal
): Promise<OpenRouterModelDescriptor[]> {
  const response = await fetchImpl('https://openrouter.ai/api/v1/models', {
    method: 'GET',
    headers: { Accept: 'application/json' },
    signal,
  })
  if (!response.ok) {
    throw new Error(`Failed to fetch OpenRouter catalog: HTTP ${response.status}`)
  }
  const body = (await response.json()) as { data?: OpenRouterModelDescriptor[] }
  const models = Array.isArray(body.data) ? body.data : []
  const freeModels = models.filter(isZeroCostModel)

  const hasFreeRouter = freeModels.some((m) => m.id === 'openrouter/free')
  if (!hasFreeRouter) {
    freeModels.unshift({
      id: 'openrouter/free',
      name: 'OpenRouter: Free Models Router (Auto Zero-Cost)',
      pricing: { prompt: '0', completion: '0' },
    })
  }
  return freeModels
}

/**
 * DeepSeek Harness (Cordis-style) OpenRouter Free Provider Adapter powered by `@openrouter/sdk`.
 */
export class DshOpenRouterFreeProvider {
  readonly name = 'openrouter-free'
  private readonly config: Required<
    Pick<DshOpenRouterFreeConfig, 'apiKeyEnv' | 'defaultModel' | 'httpReferer' | 'appTitle' | 'enforceMiniHouseRules'>
  > & { apiKey?: string }
  private readonly verifiedFreeIds = new Set<string>(CURATED_FREE_MODELS)

  constructor(config: DshOpenRouterFreeConfig = {}) {
    this.config = {
      apiKeyEnv: config.apiKeyEnv ?? 'OPENROUTER_API_KEY',
      apiKey: config.apiKey,
      defaultModel: config.defaultModel ?? 'openrouter/free',
      httpReferer: config.httpReferer ?? 'https://minihouse.local',
      appTitle: config.appTitle ?? 'MiniHouse DeepSeek Harness (OpenRouter Free)',
      enforceMiniHouseRules: config.enforceMiniHouseRules ?? true,
    }
    assertFreeModelId(this.config.defaultModel, this.verifiedFreeIds)
  }

  resolveApiKey(): string {
    const key = this.config.apiKey ?? process.env[this.config.apiKeyEnv] ?? ''
    if (!key.trim()) {
      throw new Error(
        `[dsh-llm-openrouter-free] Missing OpenRouter API Key. Set ${this.config.apiKeyEnv} or pass apiKey in config.`
      )
    }
    return key.trim()
  }

  async syncFreeCatalog(fetchImpl: typeof fetch = fetch): Promise<OpenRouterModelDescriptor[]> {
    const models = await fetchOpenRouterFreeCatalog(fetchImpl)
    for (const model of models) {
      this.verifiedFreeIds.add(model.id)
    }
    return models
  }

  createSdkClient(apiKey?: string): OpenRouter {
    return new OpenRouter({
      apiKey: apiKey ?? this.resolveApiKey(),
      httpReferer: this.config.httpReferer,
      appTitle: this.config.appTitle,
    })
  }

  async *streamChat(
    request: DshStreamRequest,
    sdkOverride?: {
      chat: {
        send: (
          params: {
            httpReferer?: string
            appTitle?: string
            chatRequest: {
              model: string
              messages: DshChatMessage[]
              stream: true
            }
          },
          options?: { signal?: AbortSignal }
        ) => Promise<AsyncIterable<unknown>>
      }
    }
  ): AsyncGenerator<DshStreamEvent> {
    const model = request.model ?? this.config.defaultModel
    assertFreeModelId(model, this.verifiedFreeIds)

    const systemParts: string[] = []
    if (this.config.enforceMiniHouseRules) {
      systemParts.push(MINIHOUSE_HARNESS_SYSTEM_RULES)
    }
    if (request.system?.trim()) {
      systemParts.push(request.system.trim())
    }

    const messages: DshChatMessage[] = [
      ...(systemParts.length > 0
        ? [{ role: 'system' as const, content: systemParts.join('\n\n') }]
        : []),
      ...request.messages,
    ]

    const client = sdkOverride ?? this.createSdkClient()
    const stream = await client.chat.send(
      {
        httpReferer: this.config.httpReferer,
        appTitle: this.config.appTitle,
        chatRequest: {
          model,
          messages,
          stream: true,
        },
      },
      { signal: request.signal }
    )

    let inputTokens = 0
    let outputTokens = 0

    for await (const rawChunk of stream) {
      if (request.signal?.aborted) {
        break
      }
      const chunk = rawChunk as {
        choices?: Array<{
          delta?: {
            content?: string | null
            reasoning?: string | null
            reasoning_content?: string | null
          }
        }>
        usage?: {
          promptTokens?: number
          completionTokens?: number
          prompt_tokens?: number
          completion_tokens?: number
        }
      }

      if (chunk.usage) {
        inputTokens = chunk.usage.promptTokens ?? chunk.usage.prompt_tokens ?? inputTokens
        outputTokens = chunk.usage.completionTokens ?? chunk.usage.completion_tokens ?? outputTokens
      }

      const delta = chunk.choices?.[0]?.delta
      if (!delta) {
        continue
      }

      const reasoning = delta.reasoning ?? delta.reasoning_content
      if (typeof reasoning === 'string' && reasoning.length > 0) {
        yield { type: 'thinking_delta', text: reasoning }
      }
      if (typeof delta.content === 'string' && delta.content.length > 0) {
        yield { type: 'text_delta', text: delta.content }
      }
    }

    yield {
      type: 'done',
      model,
      usage: { inputTokens, outputTokens },
    }
  }
}

/**
 * Cordis plugin entry for DeepSeek Harness (`dsh`).
 */
export function apply(ctx: { provide?: (name: string, instance: unknown) => void }, config: DshOpenRouterFreeConfig = {}) {
  const provider = new DshOpenRouterFreeProvider(config)
  ctx.provide?.('llm.openrouter-free', provider)
  return provider
}
