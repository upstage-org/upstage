from ariadne import gql


type_defs = gql("""
    type Query {
        hello: String!
        access(path: String!): License!
    }
                
    type Mutation {
        createLicense(input: LicenseInput!): License!
        revokeLicense(id: ID!): String!
    }
    
    type License {
        id: ID!
        assetId: ID!
        createdOn: Date
        level: Int!
        permissions: String!
        assetPath: String
    }
                
    input LicenseInput {
        assetId: ID!
        level: Int!
        permissions: String!
    }

    scalar Date     
""")
