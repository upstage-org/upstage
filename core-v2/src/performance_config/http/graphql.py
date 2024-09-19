
from ariadne import gql


type_defs = gql("""
    type Query {
        performanceCommunication:  [PerformanceCommunication!]!
        performanceConfig: [PerformanceConfig!]!
        scene: [Scene!]!
        parentStage: [ParentStage!]!
    }
                
    type PerformanceCommunication {
        id: ID!
        ownerId: Int!
        ipAddress: String!
        websocketPort: Int!
        webclientPort: Int!
        topicName: String!
        username: String!
        password: String!
        createdOn: String!
        expiresOn: String
        performanceConfigId: Int!
    }
                
    type PerformanceConfig {
        id: ID!
        name: String!
        ownerId: Int!
        description: String!
        splashScreenText: String
        splashScreenAnimationUrls: String
        createdOn: String!
        expiresOn: String
    }   

    type Scene {
        id: ID!
        name: String!
        ownerId: Int!
        description: String!
        splashScreenText: String
        splashScreenAnimationUrls: String
        createdOn: String!
        expiresOn: String
    }   
                
    type ParentStage {
        id: ID!
        stageId: Int!
        childAssetId: Int!
        stage: Stage!
        childAsset: Asset!
    }

    type Stage {
        id: ID!
        name: String!
        description: String!
        createdOn: String!
        expiresOn: String
        assets: [ParentStage!]!
    }

    type Asset {
        id: ID!
        name: String!
        type: String!
        createdOn: String!
        expiresOn: String
        stages: [ParentStage!]!
    }
""")