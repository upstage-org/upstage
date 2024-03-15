import { genqlFetch } from "./fetcher";
import { createClient as createStudioClient } from "genql/studio";
import { createClient as createConfigClient } from "genql/config";
import userGraph from "./user";
import stageGraph from "./stage";
import configGraph from "./config";
import paymentGraph from "./payment";

export const studioClient = createStudioClient({
  fetch: genqlFetch,
});

export const configClient = createConfigClient({
  fetch: genqlFetch,
});

export { userGraph, stageGraph, configGraph, paymentGraph };