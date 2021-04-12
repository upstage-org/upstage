import { gql } from "graphql-request";
import { createClient } from "./graphql";

const client = createClient('config_graphql')

export default {
  configs: () => client.request(gql`
    query {
      nginx {
        uploadLimit
      }
      system {
        termsOfService
      }
    }
  `),
  updateTermsOfService: (variables) => client.request(gql`
    mutation UpdateTermsOfService($url: String!) {
      updateTermsOfService(url: $url) {
        url
      }
    }
  `, variables)
}
