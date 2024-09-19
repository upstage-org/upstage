from ariadne import gql


type_defs = gql("""
    type Query {
        hello: String!
    }
                
    type Mutation {
        createLicense(input: LicenseInput!): License!
    }
    
    type License {
        id: ID!
        assetId: ID!
        createdOn: Date
        level: Int!
        permissions: String!
    }
                
    input LicenseInput {
        assetId: ID!
        level: Int!
        permissions: String!
    }

    scalar Date     
""")
