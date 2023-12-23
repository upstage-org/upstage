import { useAsyncState } from "@vueuse/core";
import { configClient } from "services/graphql";

export const settings = useAsyncState(
  () =>
    configClient.query({
      system: {
        __scalar: true,
      },
    }),
  {
    system: null,
  },
);
