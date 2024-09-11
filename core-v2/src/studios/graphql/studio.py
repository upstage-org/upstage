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
        media(input: MediaTableInput!): AssetConnection!  
        mediaList(mediaType: String, owner: String): [Asset!]!
    }      

    
    input MediaTableInput {
        page: Int
        limit: Int
        sort: [AssetSortEnum]
        name: String
        mediaTypes: [String]
        owners: [String]
        stages: [Int]
        tags: [String]
        createdBetween: [Date]
    }
                
    type Asset {
        id: ID!
        name: String
        src: String
        sign: String
        createdOn: Date
        size: Int!
        description: String
        assetType: AssetType
        owner: User
        stages: [Stage]
        tags: [String]
        copyrightLevel: Int
        permissions: [Permission]
        privilege: String
    }     

    type AssetConnection {
        totalCount: Int!
        edges: [Asset!]!
    }
                
    input BatchUserInput {
        username: String!
        password: String!
        email: String!            
    }
                
    type Permission {
        id: ID!
        userId: Int!
        assetId: Int!
        approved: Boolean!
        seen: Boolean!
        createdOn: Date!
        note: String
        user: User!
    }
                
    type AssetType {
        id: ID
        name: String!
    }

    type Stage {
        name: String!
        url: String!
        id: Int!
    }


    type Mutation { 
        batchUserCreation(users: [BatchUserInput]!, stageIds: [Int]): BatchUserCreationPayload
        uploadFile(base64: String!, filename: String!): File!
        saveMedia(input: SaveMediaInput!): SaveMediaPayload!
        deleteMedia(id: ID!): DeleteMediaPayload!
    }
                
    type BatchUserCreationPayload {
        users: [User!]!
    }
                
     fragment permissionFragment on Permission {
        id
        userId
        assetId
        approved
        seen
        createdOn
        note
        user {
            username
            displayName
        }
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
                
    input SaveMediaInput {
        id: ID
        name: String!
        mediaType: String!
        copyrightLevel: Int!
        owner: String!
        stageIds: [Int!]!
        userIds: [Int!]
        tags: [String!]
        w: Float!
        h: Float!
        note: String
        urls: [String!]!
        voice: VoiceInput
        link: LinkInput
    }

    input VoiceInput {
        voice: String
        variant: String
        pitch: Int
        speed: Int
        amplitude: Int
    }

    input LinkInput {
        url: String
        blank: Boolean
        effect: Boolean
    }

    type SaveMediaPayload {
        asset: Asset!
    }
                
    type DeleteMediaPayload {
        success: Boolean!
        message: String!
    }

    scalar Date

    enum AssetSortEnum {
        ASSET_TYPE_ID_ASC
        ASSET_TYPE_ID_DESC
        OWNER_ID_ASC
        OWNER_ID_DESC
        NAME_ASC
        NAME_DESC
        CREATED_ON_ASC
        CREATED_ON_DESC
    }
""")
