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
      foyer {
        title
        description
        menu
      }
    }
  `),
  updateTermsOfService: (variables) => client.request(gql`
    mutation UpdateTermsOfService($url: String!) {
      updateTermsOfService(url: $url) {
        url
      }
    }
  `, variables),
  saveConfig: (name, value) => client.request(gql`
    mutation SaveConfig($name: String!, $value: String!) {
      saveConfig(name: $name, value: $value) {
        success
      }
    }
  `, { name, value }),
}
