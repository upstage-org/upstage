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
        sweepStage(id: ID!): CommonResponse
        saveScene(input: SceneInput!): Scene
        deleteScene(id: ID!): CommonResponse
        updatePerformance(input: PerformanceInput!): CommonResponse
        deletePerformance(id: ID!): CommonResponse
        startRecording(input: RecordInput!): Performance
        saveRecording(id: ID!): Performance
        updateStatus(id: ID!): UpdateStageResponse
        updateVisibility(id: ID!): UpdateStageResponse   
        updateLastAccess(id: ID!): UpdateStageResponse   
    }
    
    type Performance {
        id: ID!
        name: String
        description: String
        stageId: ID!
        stage: Stage
        createdOn: Date
        savedOn: Date
        recording: Boolean
    }
                
    type UpdateStageResponse {
            result: String
    }
                
    input RecordInput {
        stageId: ID!
        name: String!
        description: String 
    }
                
    input PerformanceInput {
        id: ID!
        name: String!
        description: String
    }
    
    input SceneInput {
        name: String
        preview: String
        payload: String
        stageId: ID
    }
                
    type Scene {
        id: ID!
        name: String
        sceneOrder: Int
        scenePreview: String
        payload: String
        createdOn: Date 
        active: Boolean
        stageId: ID
        ownerId: ID
        owner: User
        stage: Stage
    }
                
    input AssignStagesInput {
        id: ID!
        stageIds: [ID!]
    }
                
    type SweepResponse {
        success: Boolean
        performanceId: ID
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
