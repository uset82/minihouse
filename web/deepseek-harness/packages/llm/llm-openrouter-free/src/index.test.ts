import { describe, expect, it } from 'vitest'
import {
  assertFreeModelId,
  DshOpenRouterFreeProvider,
  fetchOpenRouterFreeCatalog,
  isZeroCostModel,
} from './index.js'

describe('@minihouse/dsh-llm-openrouter-free', () => {
  it('allows openrouter/free and :free models and blocks paid models', () => {
    expect(() => assertFreeModelId('openrouter/free')).not.toThrow()
    expect(() => assertFreeModelId('deepseek/deepseek-r1:free')).not.toThrow()
    expect(() => assertFreeModelId('deepseek/deepseek-chat')).toThrow(/Blocked non-free model/)
    expect(() => assertFreeModelId('openai/gpt-4o')).toThrow(/Blocked non-free model/)
  })

  it('correctly identifies zero-cost models from OpenRouter catalog objects', () => {
    expect(
      isZeroCostModel({
        id: 'google/gemma-3-27b-it',
        name: 'Gemma 3 27B (Zero Cost)',
        pricing: { prompt: '0', completion: '0', request: '0' },
      })
    ).toBe(true)

    expect(
      isZeroCostModel({
        id: 'deepseek/deepseek-chat',
        name: 'DeepSeek V3 Paid',
        pricing: { prompt: '0.00000014', completion: '0.00000028' },
      })
    ).toBe(false)
  })

  it('filters live OpenRouter catalog to strictly zero-cost models', async () => {
    const mockFetch = async () =>
      new Response(
        JSON.stringify({
          data: [
            {
              id: 'deepseek/deepseek-r1:free',
              name: 'DeepSeek R1 (free)',
              pricing: { prompt: '0', completion: '0' },
            },
            {
              id: 'anthropic/claude-3.7-sonnet',
              name: 'Claude 3.7 Sonnet',
              pricing: { prompt: '0.000003', completion: '0.000015' },
            },
          ],
        }),
        { status: 200 }
      )

    const catalog = await fetchOpenRouterFreeCatalog(mockFetch as unknown as typeof fetch)
    expect(catalog.map((m) => m.id)).toEqual(['openrouter/free', 'deepseek/deepseek-r1:free'])
  })

  it('streams reasoning and text deltas via @openrouter/sdk chat.send and injects MiniHouse rules', async () => {
    const provider = new DshOpenRouterFreeProvider({
      apiKey: 'sk-or-v1-test',
      defaultModel: 'deepseek/deepseek-r1:free',
    })

    let capturedRequest: unknown
    const mockSdk = {
      chat: {
        send: async (params: unknown) => {
          capturedRequest = params
          return (async function* () {
            yield {
              choices: [{ delta: { reasoning: 'Analizando viga 6x3 m...' } }],
            }
            yield {
              choices: [{ delta: { content: 'Estado: [CONCEPTUAL] flecha 24,63 mm.' } }],
              usage: { promptTokens: 42, completionTokens: 18 },
            }
          })()
        },
      },
    }

    const events = []
    for await (const ev of provider.streamChat(
      {
        messages: [{ role: 'user', content: '¿Cuál es la flecha del ejemplo?' }],
      },
      mockSdk
    )) {
      events.push(ev)
    }

    expect(events).toEqual([
      { type: 'thinking_delta', text: 'Analizando viga 6x3 m...' },
      { type: 'text_delta', text: 'Estado: [CONCEPTUAL] flecha 24,63 mm.' },
      {
        type: 'done',
        model: 'deepseek/deepseek-r1:free',
        usage: { inputTokens: 42, outputTokens: 18 },
      },
    ])

    const req = capturedRequest as { chatRequest: { messages: Array<{ role: string; content: string }> } }
    expect(req.chatRequest.messages[0]?.role).toBe('system')
    expect(req.chatRequest.messages[0]?.content).toContain('[CONCEPTUAL]')
  })
})
