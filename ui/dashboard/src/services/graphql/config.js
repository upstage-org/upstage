import { gql } from "graphql-request";
import { createClient } from "./graphql";

const client = createClient('config_graphql')

export default {
  configs: () => client.request(gql`
    query {
      nginx {
        uploadLimit
      } 
    }
  `),
}