from ariadne import gql


type_defs = gql("""
    type Mutation {
        createStage(input: StageInput!): State
        updateStage(input: StageInput!): State
        duplicateStage(id: ID!, name: String!): State
        deleteStage(id: ID!): CommonResponse
    }
                
    type CommonResponse {
        success: Boolean
        message: String           
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
        config: String
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
