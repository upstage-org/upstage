from ariadne import gql

type_defs = gql("""
    type Query {
        _empty: String
    }
                
    type GroupType {
        id: Int
        name: String
    }

    type TokenType {
        user_id: Int
        access_token: String
        refresh_token: String
        role: Int
        first_name: String
        groups: [GroupType]
        username: String
        title: String
    }

    input LoginInput {
        username: String!
        password: String!
    }
                
    type RefreshTokenResponse {
        access_token: String!
    }

    type Mutation {
        login(payload: LoginInput!): TokenType
        refresh_token: RefreshTokenResponse
        logout: String
    }
""")
