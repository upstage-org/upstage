from ariadne import gql


type_defs = gql("""
    type Mutation {
        createStage(input: StageInput!): State
    }
                
    input StageInput {
        id: ID
        fileLocation: String
        status: String
        visibility: Boolean
        cover: String
        name: String
        description: String
        playerAccess: String
    }
                
    type State {
        id: ID!
        name: String
        fileLocation: String
        status: String
        visibility: Boolean
        cover: String
        description: String
        playerAccess: String            
    }

    type Query {
        hello: String
    }
""")
