import { McpServer } from "@modelcontextprotocol/sdk/server/mcp";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio";
import { firecrawl, FirecrawlSchema } from "../../tools/firecrawl";

const server = new McpServer({ name: "firecrawl", version: "0.1.0" });

server.tool("crawl", FirecrawlSchema.shape, async (args) => {
  return await firecrawl(args);
});

const transport = new StdioServerTransport();
await server.connect(transport);
