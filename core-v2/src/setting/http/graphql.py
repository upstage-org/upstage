from ariadne import gql


type_defs = gql("""
    type Query {
        nginx: NginxConfig!
        system: SystemConfig!
        foyer: FoyerConfig!
    }
    
    type Mutation {
        updateTermsOfService(url: String!): Config
        saveConfig(input: ConfigInput!): Config
        sendEmail(input: EmailInput!): CommonResponse
    }
                
    type NginxConfig {
        limit: Int!            
    }

    type CommonResponse {
        success: Boolean!
        message: String
    }
                   
    input EmailInput {
        subject: String!
        body: String!
        recipients: String!
        bcc: String
    }
                
    input ConfigInput {
        name: String!
        value: String!  
    }
                
    type Config{
        id: Int!
        name: String!
        value: String
        created_on: Date!
    }
                
    type SystemConfig {
        termsOfService: Config
        manual: Config
        esp: Config
        enableDonate: Config    
    }
                
    type FoyerConfig {
        title: Config
        description: Config
        menu: Config
        showRegistration: Config
    }
                
    scalar Date
              
""")
