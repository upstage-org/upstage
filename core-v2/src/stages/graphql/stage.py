from ariadne import gql


type_defs = gql("""
    type Mutation {
        createStage(input: StageInput!): Stage
        updateStage(input: StageInput!): Stage
        duplicateStage(id: ID!, name: String!): Stage
        deleteStage(id: ID!): CommonResponse
        assignMedia(input: AssignMediaInput!): Asset
        uploadMedia(input: UploadMediaInput!): Asset
        updateMedia(input: UpdateMediaInput!): Asset
        deleteMedia(id: ID!): CommonResponse
        assignStages(input: AssignStagesInput!): Asset
    }
                
    input AssignStagesInput {
        id: ID!
        stageIds: [ID!]
    }
                
    type CommonResponse {
        success: Boolean
        message: String           
    }
                
    input UploadMediaInput {
        name: String!
        base64: String!
        mediaType: String!
        filename: String!
    }
                
    input AssignMediaInput {
        id: ID!
        mediaIds: [ID]
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
                
    type Stage {
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
        permission: String
        privilege: String
        assetLicense: AssetLicense
    } 
                
    type AssetLicense {
        id: ID!
        assetId: Int!
        playerAccess: String!
        level: Int!            
    }

    scalar Date   
                
    type AssetType {
        id: ID
        name: String!
    }
                        
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
                
    input UpdateMediaInput {
        id: ID!
        name: String!
        mediaType: String
        description: String
        fileLocation: String
        base64: String
        copyrightLevel: Int
        playerAccess: String
        uploadedFrames: [String]
    }
""")
