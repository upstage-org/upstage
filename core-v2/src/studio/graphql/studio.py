from ariadne import gql


type_defs = gql("""
    type User {
        id: ID!
        username: String!
        password: String!
        email: String!
        binName: String
        role: String!
        firstName: String!
        lastName: String!
        displayName: String
        active: Boolean!
        createdOn: String!
        firebasePushnotId: String
        deactivatedOn: String
        uploadLimit: Int
        intro: String
        canSendEmail: Boolean
        lastLogin: String
        roleName: String
    }
                
    enum AdminPlayerSortEnum {
        USERNAME_ASC
        USERNAME_DESC
        CREATED_ON_ASC
        CREATED_ON_DESC
        LAST_LOGIN_ASC
        LAST_LOGIN_DESC
        ROLE_ASC
        ROLE_DESC
        EMAIL_ASC
        EMAIL_DESC
    }

    type AdminPlayerConnection {
        totalCount: Int!
        edges: [User!]!
    }
                
    type Query {
        hello: String
        whoami: User
        adminPlayers(
            first: Int,
            page: Int,
            sort: [AdminPlayerSortEnum],
            usernameLike: String,
            createdBetween: [String]
        ): AdminPlayerConnection        
    }
                
    input BatchUserInput {
        username: String!
        password: String!
        email: String!            
    }

    type Mutation { 
        batchUserCreation(users: [BatchUserInput]!, stageIds: [Int]): BatchUserCreationPayload
        uploadFile(base64: String!, filename: String!): File!
    }
                
    type BatchUserCreationPayload {
        users: [User!]!
    }
                
    fragment f1 on User {
        id
        username
        password
        email
        binName
        role
        firstName
        lastName
        displayName
        active
        createdOn
        firebasePushnotId
        deactivatedOn
        uploadLimit
        intro
        canSendEmail
        lastLogin
        roleName
    }
                
    type File {
        url: String!
    }
""")
