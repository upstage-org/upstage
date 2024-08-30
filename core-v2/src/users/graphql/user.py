from ariadne import gql


type_defs = gql("""
    type Query {
        hello: String!
    }
    type Mutation {
        createUser(data: UserInput): UserResponse
    }
                
    input UserInput {
        username: String!
        status: String!
    }

    type UserResponse {
        username: String
        status: String
    }
""")
