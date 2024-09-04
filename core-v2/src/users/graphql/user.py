from ariadne import gql


type_defs = gql("""
    type Query {
        hello: String
    }
    
    type User {
        id: ID!
        dbId: Int
        username: String!
        firstName: String
        lastName: String
        displayName: String
        email: String
        active: Boolean
        createdOn: String
        role: Int
        uploadLimit: Int
        intro: String
    }

    input CreateUserInput {
        username: String!
        password: String!
        email: String
        firstName: String
        lastName: String
        intro: String
        token: String
    }

    type CreateUserPayload {
        user: User
    }

    type Mutation {
        createUser(inbound: CreateUserInput!): CreateUserPayload
    }  
      
    fragment userFragment on User {
        id
        dbId
        username
        firstName
        lastName
        displayName
        email
        active
        createdOn
        role
        uploadLimit
        intro
    }
""")
