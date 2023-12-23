import { genqlFetch } from "./fetcher";
import { createClient as createStudioClient } from "genql/studio";
import { createClient as createConfigClient } from "genql/config";

export const studioClient = createStudioClient({
  fetch: genqlFetch,
});

export const configClient = createConfigClient({
  fetch: genqlFetch,
});
