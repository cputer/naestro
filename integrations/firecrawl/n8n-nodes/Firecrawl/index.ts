import type { IExecuteFunctions, INodeType, INodeTypeDescription } from 'n8n-workflow';
import { firecrawl } from '../../tools/firecrawl';

export class Firecrawl implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Firecrawl',
    name: 'firecrawl',
    group: ['transform'],
    version: 1,
    description: 'Interact with the Firecrawl API',
    defaults: { name: 'Firecrawl' },
    inputs: ['main'],
    outputs: ['main'],
    properties: [
      {
        displayName: 'Operation',
        name: 'operation',
        type: 'options',
        options: [{ name: 'Crawl', value: 'crawl' }],
        default: 'crawl',
      },
      {
        displayName: 'Options',
        name: 'options',
        type: 'json',
        default: '{}',
        description: 'All Firecrawl parameters as JSON object',
      },
    ],
  };

  async execute(this: IExecuteFunctions) {
    const items: Array<Record<string, any>> = [];
    const length = this.getInputData().length;

    for (let i = 0; i < length; i++) {
      const operation = this.getNodeParameter('operation', i) as string;
      const options = this.getNodeParameter('options', i, {}) as any;

      if (operation === 'crawl') {
        const result = await firecrawl(options);
        items.push(...(result.items ?? []));
      }
    }

    return [items];
  }
}
