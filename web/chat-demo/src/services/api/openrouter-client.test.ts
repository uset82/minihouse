import { describe, expect, it } from 'vitest'
import {
  assertFreeOpenRouterModel,
  fetchFreeOpenRouterModels,
  isFreeOpenRouterModel,
  resolveFreeModelId,
  streamOpenRouterMessage,
} from './openrouter-client.js'
import type { CreateMessageRequest, MessageStreamEvent } from './types.js'

describe('openrouter-client (@openrouter/sdk adapter)', () => {
  it('enforces zero-cost model IDs and blocks paid models', () => {
    expect(() => assertFreeOpenRouterModel('openrouter/free')).not.toThrow()
    expect(() => assertFreeOpenRouterModel('deepseek/deepseek-r1:free')).not.toThrow()
    expect(() => assertFreeOpenRouterModel('deepseek/deepseek-chat-v3-0324:free')).not.toThrow()
    expect(() => assertFreeOpenRouterModel('openai/gpt-4o')).toThrow(/Blocked non-free/)
    expect(() => assertFreeOpenRouterModel('deepseek/deepseek-chat')).toThrow(/Blocked non-free/)
  })

  it('maps legacy DeepSeek model names to OpenRouter free models', () => {
    expect(resolveFreeModelId('deepseek-flash', false)).toBe('openrouter/free')
    expect(resolveFreeModelId('deepseek-flash', true)).toBe('deepseek/deepseek-r1:free')
    expect(resolveFreeModelId('meta-llama/llama-3.3-70b-instruct:free', false)).toBe(
      'meta-llama/llama-3.3-70b-instruct:free'
    )
  })

  it('checks zero-cost pricing in OpenRouter model descriptors', () => {
    expect(
      isFreeOpenRouterModel({
        id: 'mistralai/mistral-small:free',
        pricing: { prompt: '0.001', completion: '0.001' },
      })
    ).toBe(true)
    expect(
      isFreeOpenRouterModel({
        id: 'custom/zero-cost-model',
        pricing: { prompt: '0', completion: '0', request: '0' },
      })
    ).toBe(true)
    expect(
      isFreeOpenRouterModel({
        id: 'openai/gpt-4o-mini',
        pricing: { prompt: '0.00000015', completion: '0.0000006' },
      })
    ).toBe(false)
  })

  it('fetches and filters live free models from OpenRouter /api/v1/models', async () => {
    const fakeFetch = async () =>
      new Response(
        JSON.stringify({
          data: [
            {
              id: 'nvidia/llama-3.1-nemotron-nano-8b-v1:free',
              name: 'NVIDIA Nemotron Nano 8B (free)',
              pricing: { prompt: '0', completion: '0' },
            },
            {
              id: 'openai/gpt-4.1',
              name: 'GPT-4.1 Paid',
              pricing: { prompt: '0.000002', completion: '0.000008' },
            },
          ],
        }),
        { status: 200 }
      )

    const models = await fetchFreeOpenRouterModels(fakeFetch as unknown as typeof fetch)
    const ids = models.map((m) => m.id)
    expect(ids).toContain('openrouter/free')
    expect(ids).toContain('nvidia/llama-3.1-nemotron-nano-8b-v1:free')
    expect(ids).not.toContain('openai/gpt-4.1')
  })

  it('converts @openrouter/sdk stream chunks into chat-demo MessageStreamEvent sequence', async () => {
    const mockSdk = {
      chat: {
        send: async () =>
          (async function* () {
            yield {
              choices: [{ delta: { reasoning: 'Checking 6x3m beam...' } }],
            }
            yield {
              choices: [{ delta: { content: 'Deflection is 24.63 mm [CONCEPTUAL].' } }],
              usage: { promptTokens: 25, completionTokens: 12 },
            }
          })(),
      },
    }

    const request: CreateMessageRequest = {
      model: 'deepseek/deepseek-r1:free',
      system: 'Base system prompt',
      messages: [{ role: 'user', content: 'What is the deflection of the 6x3m beam?' }],
      thinking: { type: 'enabled' },
      tools: [],
      safety_check: { level: 'high' },
      title: { enabled: true },
    }

    const controller = new AbortController()
    const events: MessageStreamEvent[] = []
    for await (const ev of streamOpenRouterMessage(
      'sk-or-v1-test',
      request,
      controller.signal,
      mockSdk
    )) {
      events.push(ev)
    }

    expect(events.map((e) => e.type)).toEqual([
      'message_start',
      'content_block_start',
      'content_block_delta',
      'content_block_stop',
      'content_block_start',
      'content_block_delta',
      'content_block_stop',
      'message_delta',
      'message_stop',
    ])

    const deltaEvent = events.find((e) => e.type === 'message_delta')
    expect(deltaEvent?.type === 'message_delta' && deltaEvent.delta.title).toContain(
      'What is the deflection'
    )
  })
})
